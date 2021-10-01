__all__ = ['Command', 'command', 'GroupMixin']

import asyncio
import functools

from ._types import _BaseCommand
from ...exception import CommandError, CommandInvokeError, CommandRegistrationError


class _CaseInsensitiveDict(dict):
    def __contains__(self, k):
        return super().__contains__(k.casefold())

    def __delitem__(self, k):
        return super().__delitem__(k.casefold())

    def __getitem__(self, k):
        return super().__getitem__(k.casefold())

    def get(self, k, default=None):
        return super().get(k.casefold(), default)

    def pop(self, k, default=None):
        return super().pop(k.casefold(), default)

    def __setitem__(self, k, v):
        super().__setitem__(k.casefold(), v)


class GroupMixin:
    def __init__(self, *args, **kwargs):
        case_insensitive = kwargs.get('case_insensitive', False)
        self.all_commands = _CaseInsensitiveDict() if case_insensitive else {}
        self.case_insensitive = case_insensitive
        super().__init__(*args, **kwargs)

    @property
    def commands(self):
        """Set[:class:`.Command`]: A unique set of commands without aliases that are registered."""
        return set(self.all_commands.values())

    def recursively_remove_all_commands(self):
        for command in self.all_commands.copy().values():
            if isinstance(command, GroupMixin):
                command.recursively_remove_all_commands()
            self.remove_command(command.name)

    def add_command(self, command):
        """Adds a :class:`.Command` into the internal list of commands.

        This is usually not called, instead the :meth:`~.GroupMixin.command` or
        :meth:`~.GroupMixin.group` shortcut decorators are used instead.

        .. versionchanged:: 1.4
             Raise :exc:`.CommandRegistrationError` instead of generic :exc:`.ClientException`

        Parameters
        -----------
        command: :class:`Command`
            The command to add.

        Raises
        -------
        :exc:`.CommandRegistrationError`
            If the command or its alias is already registered by different command.
        TypeError
            If the command passed is not a subclass of :class:`.Command`.
        """

        if not isinstance(command, Command):
            raise TypeError('The command passed must be a subclass of Command')

        if isinstance(self, Command):
            command.parent = self

        if command.name in self.all_commands:
            raise CommandRegistrationError(command.name)

        self.all_commands[command.name] = command
        for alias in command.aliases:
            if alias in self.all_commands:
                self.remove_command(command.name)
                raise CommandRegistrationError(alias, alias_conflict=True)
            self.all_commands[alias] = command


def hooked_wrapped_callback(command, ctx, coro):
    @functools.wraps(coro)
    async def wrapped(*args, **kwargs):
        try:
            ret = await coro(ctx, *args, **kwargs)
        except CommandError:
            ctx.command_failed = True
            raise
        except asyncio.CancelledError:
            ctx.command_failed = True
            return
        except Exception as exc:
            ctx.command_failed = True
            raise CommandInvokeError(exc) from exc
        finally:
            await command.call_after_hooks(ctx)
        return ret

    return wrapped


class Command(_BaseCommand):  # TODO: 作る
    def __init__(self, func, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("関数は非同期である必要があります")
        self.name = name = kwargs.get('name') or func.__name__
        if not isinstance(name, str):
            raise TypeError('コマンドのネームスペースはstringである必要があります')

        self.callback = func
        self.enabled = kwargs.get('enabled', True)
        self.__original_kwargs__ = kwargs.copy()
        self.aliases = kwargs.get('aliases', [])

        try:
            checks = func.__commands_checks__
            checks.reverse()
        except AttributeError:
            checks = kwargs.get('checks', [])
        finally:
            self.checks = checks
        self.cog = None
        parent = kwargs.get('parent')
        self.parent = parent if isinstance(parent, _BaseCommand) else None

    @property
    def full_parent_name(self):
        """:class:`str`: Retrieves the fully qualified parent command name.

        This the base command name required to execute it. For example,
        in ``?one two three`` the parent name would be ``one two``.
        """
        entries = []
        command = self
        while command.parent is not None:
            command = command.parent
            entries.append(command.name)

        return ' '.join(reversed(entries))

    @property
    def qualified_name(self):
        """:class:`str`: Retrieves the fully qualified command name.

        This is the full parent name with the command name as well.
        For example, in ``?one two three`` the qualified name would be
        ``one two three``.
        """

        parent = self.full_parent_name
        if parent:
            return parent + ' ' + self.name
        else:
            return self.name

    async def call_after_hooks(self, ctx):
        # cog = self.cog
        # call the cog local hook if applicable:
        # if cog is not None:
        #    hook = Cog._get_overridden_method(cog.cog_after_invoke)
        #    if hook is not None:
        #        await hook(ctx)

        hook = ctx.bot._after_invoke
        if hook is not None:
            await hook(ctx)

    async def invoke(self, ctx):
        # terminate the invoked_subcommand chain.
        # since we're in a regular command (and not a group) then
        # the invoked subcommand is None.
        ctx.invoked_subcommand = None
        ctx.subcommand_passed = None
        injected = hooked_wrapped_callback(self, ctx, self.callback)
        await injected(ctx)

    def _ensure_assignment_on_copy(self, other):
        if self.checks != other.checks:
            other.checks = self.checks.copy()

        try:
            other.on_error = self.on_error
        except AttributeError:
            pass
        return other

    def copy(self):
        """Creates a copy of this command.

        Returns
        --------
        :class:`Command`
            A new instance of this command.
        """
        ret = self.__class__(self.callback, **self.__original_kwargs__)
        return self._ensure_assignment_on_copy(ret)

    def _update_copy(self, kwargs):
        if kwargs:
            kw = kwargs.copy()
            kw.update(self.__original_kwargs__)
            copy = self.__class__(self.callback, **kw)
            return self._ensure_assignment_on_copy(copy)
        else:
            return self.copy()


def command(name=None, cls=None, **attrs):
    """A decorator that transforms a function into a :class:`.Command`
    or if called with :func:`.group`, :class:`.Group`.

    By default the ``help`` attribute is received automatically from the
    docstring of the function and is cleaned up with the use of
    ``inspect.cleandoc``. If the docstring is ``bytes``, then it is decoded
    into :class:`str` using utf-8 encoding.

    All checks added using the :func:`.check` & co. decorators are added into
    the function. There is no way to supply your own checks through this
    decorator.

    Parameters
    -----------
    name: :class:`str`
        The name to create the command with. By default this uses the
        function name unchanged.
    cls
        The class to construct with. By default this is :class:`.Command`.
        You usually do not change this.
    attrs
        Keyword arguments to pass into the construction of the class denoted
        by ``cls``.

    Raises
    -------
    TypeError
        If the function is not a coroutine or is already a command.
    """
    if cls is None:
        cls = Command

    def decorator(func):
        if isinstance(func, Command):
            raise TypeError('Callback is already a command.')
        return cls(func, name=name, **attrs)

    return decorator