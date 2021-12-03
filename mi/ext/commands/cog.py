import inspect
from typing import Any, Callable, ClassVar, Coroutine, Dict, List, Optional, Tuple, Union
from mi.abc.ext.bot import AbstractBotBase

from mi.ext.commands.core import Command
from mi.ext.commands._types import _BaseCommand


class CogMeta(type):
    def __new__(cls, *args: Tuple[Any], **kwargs: Dict[str, Any]):
        name, bases, attrs = args
        attrs['__cog_name__'] = kwargs.pop("name", name)
        attrs['__cog_settings__'] = kwargs.pop("command_attrs", {})
        commands = {}
        listeners = {}
        no_bot_cog = "Commands or listeners must not start with cog_ or bot_ (in method {0.__name__}.{1})"
        new_cls = super().__new__(cls, name, bases, attrs, **kwargs)

        for base in reversed(new_cls.__mro__):  # 多重継承を確認 !コマンドを登録
            for elem, value in base.__dict__.items():
                if elem in commands:
                    del commands[elem]  # commandsから削除
                if elem in listeners:
                    del listeners[elem]  # listenersから削除

                is_static_method = isinstance(value, staticmethod)

                if is_static_method:  # staticmethodか確認
                    value = value.__func__  # 関数をvalueに !valueが重要

                if isinstance(value, _BaseCommand):
                    if is_static_method:
                        raise TypeError(
                            f"Command in method {base}.{elem!r} must not be staticmethod."
                        )
                    if elem.startswith(("cog", "bot_")):
                        raise TypeError(no_bot_cog.format(base, elem))
                    commands[elem] = value
                elif inspect.iscoroutinefunction(value):
                    try:
                        value.__cog_listener__
                    except AttributeError:
                        continue
                    else:
                        if elem.startswith(("cog", "bot_")):
                            raise TypeError(no_bot_cog.format(base, elem))
                        listeners[elem] = value

        new_cls.__cog_commands__ = list(commands.values())

        listeners_as_list: List[tuple[str, Any]] = []

        for listener in listeners.values():
            for listener_name in listener.__cog_listener_names__:
                listeners_as_list.append((listener_name, listener))

        new_cls.__cog_listeners__ = listeners_as_list
        return new_cls

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]):
        super().__init__(*args, **kwargs)


class Cog(metaclass=CogMeta):
    __cog_name__ = ClassVar[str]
    __cog_settings__: Dict[str, Any] = {}
    __cog_commands__: List[Command] = []
    __cog_listeners__: ClassVar[List[Tuple[str, str]]]

    def __new__(cls, *args: tuple[Any], **kwargs: Dict[str, Any]):
        self = super().__new__(cls)
        cmd_attrs = cls.__cog_settings__
        self.__cog_commands__ = tuple(c._update_copy(cmd_attrs) for c in cls.__cog_commands__)

        lookup = {cmd.qualified_name: cmd for cmd in self.__cog_commands__}

        for command in self.__cog_commands__:
            setattr(self, command.callback.__name__, command)
            parent = command.parent
            if parent:
                parent = lookup[parent.qualified_name]

                parent.remove_command(command.name)
                parent.add_command(command)
        return self

    @classmethod
    def listener(cls, name: Optional[str] = None):
        if name is not None:
            raise TypeError(f'Cog.listener expected str but received {name.__clsss__.__name__!r} instead.')

        def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
            actual = func
            if isinstance(actual, staticmethod):
                actual = actual.__func__
            if not inspect.iscoroutinefunction(actual):
                raise TypeError('Listener function must be a coroutine function.')
            actual.__cog_listener__ = True
            to_assign = name or actual.__name__
            try:
                actual.__cog_listener_names__.append(to_assign)
            except AttributeError:
                actual.__cog_listener_names__ = [to_assign]
            return func

        return decorator

    def _inject(self, bot: AbstractBotBase):
        cls = self.__class__
        for index, command in enumerate(self.__cog_commands__):
            if command.parent is None:
                try:
                    bot.add_command(command)
                except Exception as e:
                    for to_undo in self.__cog_commands__[:index]:
                        if to_undo.parent is None:
                            bot.remove_command(to_undo.name)
                        raise e
        for name, method_name in self.__cog_listeners__:
            bot.add_listener(getattr(self, method_name), name)

        return self
