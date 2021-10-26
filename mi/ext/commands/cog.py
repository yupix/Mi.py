import inspect
from typing import Any, ClassVar, Dict, List, Tuple

__all__ = ["Cog"]

from ._types import _BaseCommand


class CogMeta(type):
    """A metaclass for defining a cog.

    Note that you should probably not use this directly. It is exposed
    purely for documentation purposes along with making custom metaclasses to intermix
    with other metaclasses such as the :class:`abc.ABCMeta` metaclass.

    For example, to create an abstract cog mixin class, the following would be done.

    .. code-block:: python3

        import abc

        class CogABCMeta(commands.CogMeta, abc.ABCMeta):
            pass

        class SomeMixin(metaclass=abc.ABCMeta):
            pass

        class SomeCogMixin(SomeMixin, commands.Cog, metaclass=CogABCMeta):
            pass

    .. note::

        When passing an attribute of a metaclass that is documented below, note
        that you must pass it as a keyword-only argument to the class creation
        like the following example:

        .. code-block:: python3

            class MyCog(commands.Cog, name='My Cog'):
                pass

    Attributes
    -----------
    name: :class:`str`
        The cog name. By default, it is the name of the class with no modification.
    description: :class:`str`
        The cog description. By default, it is the cleaned docstring of the class.

        .. versionadded:: 1.6

    command_attrs: :class:`dict`
        A list of attributes to apply to every command inside this cog. The dictionary
        is passed into the :class:`Command` options at ``__init__``.
        If you specify attributes inside the command attribute in the class, it will
        override the one specified inside this attribute. For example:

        .. code-block:: python3

            class MyCog(commands.Cog, command_attrs=dict(hidden=True)):
                @commands.command()
                async def foo(self, ctx):
                    pass # hidden -> True

                @commands.command(hidden=False)
                async def bar(self, ctx):
                    pass # hidden -> False
    """

    def __new__(cls, *args, **kwargs):
        name, bases, attrs = args
        attrs["__cog_name__"] = kwargs.pop("name", name)
        attrs["__cog_settings__"] = kwargs.pop("command_attrs", {})

        description = kwargs.pop("description", None)
        if description is None:
            description = inspect.cleandoc(attrs.get("__doc__", ""))
        attrs["__cog_description__"] = description

        commands = {}
        listeners = {}
        no_bot_cog = "Commands or listeners must not start with cog_ or bot_ (in method {0.__name__}.{1})"

        new_cls = super().__new__(cls, name, bases, attrs, **kwargs)
        for base in reversed(new_cls.__mro__):
            for elem, value in base.__dict__.items():
                if elem in commands:
                    del commands[elem]  # commandsから消す
                if elem in listeners:
                    del listeners[elem]

                is_static_method = isinstance(value, staticmethod)
                if is_static_method:
                    value = value.__func__
                # value が重要
                if isinstance(value, _BaseCommand):
                    if is_static_method:
                        raise TypeError(
                            f"Command in method {base}.{elem!r} must not be staticmethod."
                        )
                    if elem.startswith(("cog_", "bot_")):
                        raise TypeError(no_bot_cog.format(base, elem))
                    commands[elem] = value
                elif inspect.iscoroutinefunction(value):
                    try:
                        getattr(value, "__cog_listener__")
                    except AttributeError:
                        continue
                    else:
                        if elem.startswith(("cog_", "bot_")):
                            raise TypeError(no_bot_cog.format(base, elem))
                        listeners[elem] = value

        new_cls.__cog_commands__ = list(
            commands.values()
        )  # this will be copied in Cog.__new__

        listeners_as_list = []
        for listener in listeners.values():
            for listener_name in listener.__cog_listener_names__:
                # I use __name__ instead of just storing the value so I can inject
                # the self attribute when the time comes to add them to the bot
                listeners_as_list.append((listener_name, listener.__name__))

        new_cls.__cog_listeners__ = listeners_as_list
        return new_cls

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

    @classmethod
    def qualified_name(cls):
        return cls.__cog_name__


class Cog(metaclass=CogMeta):
    __cog_name__ = ClassVar[str]
    __cog_settings__ = ClassVar[Dict[str, Any]]
    __cog_commands__: ClassVar[List]
    __cog_listeners__: ClassVar[List[Tuple[str, str]]]

    def __new__(cls, *args, **kwargs):
        # For issue 426, we need to store a copy of the command objects
        # since we modify them to inject `self` to them.
        # To do this, we need to interfere with the Cog creation process.
        self = super().__new__(cls)
        cmd_attrs = cls.__cog_settings__

        # Either update the command with the cog provided defaults or copy it.
        self.__cog_commands__ = tuple(
            c._update_copy(cmd_attrs) for c in cls.__cog_commands__
        )

        lookup = {cmd.qualified_name: cmd for cmd in self.__cog_commands__}

        # Update the Command instances dynamically as well
        for command in self.__cog_commands__:
            setattr(self, command.callback.__name__, command)
            parent = command.parent
            if parent is not None:
                # Get the latest parent reference
                parent = lookup[parent.qualified_name]

                # Update our parent's reference to our self
                parent.remove_command(command.name)
                parent.add_command(command)

        return self

    @classmethod
    def listener(cls, name=None):
        """A decorator that marks a function as a listener.

        This is the cog equivalent of :meth:`.Bot.listen`.

        Parameters
        ------------
        name: :class:`str`
            The name of the event being listened to. If not provided, it
            defaults to the function's name.

        Raises
        --------
        TypeError
            The function is not a coroutine function or a string was not passed as
            the name.
        """

        if name is not None and not isinstance(name, str):
            raise TypeError(
                f"Cog.listener expected str but received {name.__class__.__name__!r} instead."
            )

        def decorator(func):
            actual = func
            if isinstance(actual, staticmethod):
                actual = actual.__func__
            if not inspect.iscoroutinefunction(actual):
                raise TypeError("Listener function must be a coroutine function.")
            actual.__cog_listener__ = True
            to_assign = name or actual.__name__
            try:
                actual.__cog_listener_names__.append(to_assign)
            except AttributeError:
                actual.__cog_listener_names__ = [to_assign]
            # we have to return `func` instead of `actual` because
            # we need the type to be `staticmethod` for the metaclass
            # to pick it up but the metaclass unfurls the function and
            # thus the assignments need to be on the actual function
            return func

        return decorator

    def _inject(self, bot):
        cls = self.__class__

        # realistically, the only thing that can cause loading errors
        # is essentially just the command loading, which raises if there are
        # duplicates. When this condition is met, we want to undo all what
        # we've added so far for some form of atomic loading.
        for index, command in enumerate(self.__cog_commands__):
            command.cog = self
            if command.parent is None:
                try:
                    bot.add_command(command)
                except Exception as e:
                    # undo our additions
                    for to_undo in self.__cog_commands__[:index]:
                        if to_undo.parent is None:
                            bot.remove_command(to_undo.name)
                    raise e

        # while Bot.add_listener can raise if it's not a coroutine,
        # this precondition is already met by the listener decorator
        # already, thus this should never raise.
        # Outside of, memory errors and the like...
        for name, method_name in self.__cog_listeners__:
            bot.add_listener(getattr(self, method_name), name)

        return self
