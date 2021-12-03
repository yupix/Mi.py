import asyncio
import functools
from typing import Any, Callable, Coroutine, Dict, Optional, Tuple, TypeVar, Union
from typing_extensions import Concatenate

from ._types import _BaseCommand
from mi.exception import CommandError, CommandInvokeError, CommandRegistrationError
from ...abc.ext.core import AbstractCommand, AbstractGroup


class GroupMixin:
    def __init__(self, *args: tuple[Any], **kwargs: Dict[Any, Any]):
        # TODO: case_insensitiveの実態調査してから実装するか考慮する
        case_insensitive = kwargs.get("case_insensitive", False)
        self.all_commands: Dict[str, Command] = {}
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

    def add_command(self, command: AbstractCommand):
        if not isinstance(command, Command):
            raise TypeError(f'{command} passed must be a subclass of Command')

        if isinstance(self, Command):
            command.parent = self

        if command.name is self.all_commands:
            raise CommandRegistrationError(command.name)

        self.all_commands[command.name] = command
        for alias in command.aliases:
            if alias in self.all_commands:
                self.remove_command(command.name)
                raise CommandRegistrationError(alias, alias_conflict=True)
            self.all_commands[alias] = command

    def remove_command(self, name: str):
        command = self.all_commands.pop(name, None)
        if command is None:
            return None

        if name in command.aliases:
            return command

        for alias in command.aliases:
            cmd = self.all_commands.pop(alias, None)
            if cmd is not None and cmd != command:
                self.all_commands[alias] = cmd
        return command

    def command(self, name: Optional[str] = None, cls=None, *args: Tuple[Any], **kwargs: Dict[Any, Any]):
        def decorator(func: Callable[..., Any]):  # TODO:ここやる
            kwargs.setdefault('parent', self)
            result = command(name=name, cls=cls, *args, **kwargs)(func)
            return result

        return decorator


def hooked_wrapped_callback(command: 'Command', ctx, coro):
    @functools.wraps(coro)
    async def wrapped(*args: Tuple[Any], **kwargs: Dict[Any, Any]):
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


class Command(_BaseCommand, AbstractCommand):
    def __init__(self, func: Callable[..., Coroutine[Any, Any, Any]], **kwargs: Any):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError('func must be a coroutine')
        self.name = name = kwargs.get('name') or func.__name__
        if not isinstance(name, str):
            raise TypeError('name must be a string')

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
        self.parent = parent if isinstance(parent, _BaseCommand) else None  # TODO: parentの型調べる

    @property
    def full_parent_name(self) -> str:
        entries = []
        command = self
        while command.parent is not None:
            command = command.parent
            entries.append(command.name)
        return ' '.join(reversed(entries))

    @property
    def qualified_name(self) -> str:
        parent = self.full_parent_name
        if parent:
            return parent + ' ' + self.name
        return self.name

    async def call_after_hooks(self, ctx):
        hook = ctx.bot._after_invoke
        if hook is not None:
            await hook(ctx)

    async def invoke(self, ctx, *args: Tuple[Any], **kwargs: Dict[Any, Any]):
        ctx.invoked_subcommand = None
        ctx.subcommand_passed = None
        injected = hooked_wrapped_callback(self, ctx, self.callback)
        await injected(ctx, *args, **kwargs)

    def _ensure_assignment_on_copy(self, other: 'Command') -> 'Command':
        if self.checks != other.checks:
            other.checks = self.checks.copy()

        try:
            other.on_error = self.on_error
        except AttributeError:
            pass
        return other

    def copy(self) -> 'Command':
        ret = self.__class__(self.callback, **self.__original_kwargs__)
        return self._ensure_assignment_on_copy(ret)

    def _update_copy(self, kwargs: Dict[Any, Any]) -> 'Command':
        if kwargs:
            kw = kwargs.copy()
            kw.update(self.__original_kwargs__)
            copy = self.__class__(self.callback, **kw)
            return self._ensure_assignment_on_copy(copy)
        return self.copy()


class Group(GroupMixin, Command, AbstractGroup):
    def __init__(self, *args: tuple[Any], **attrs: Any):
        self.invoke_without_command: bool = attrs.pop('invoke_without_command', False)
        super().__init__(*args, **attrs)


def group(name: Optional[str] = None, **attrs: Any):
    """group decorator

    サブコマンドを作成する際に使用します。

    Parameters
    ----------
    name : Optional[str], optional
        コマンド名, by default None
    """
    attrs.setdefault("cls", Group)
    return command(name=name, cls=Group)


def command(name: Optional[str] = None, cls: Any = None, **attrs: Dict[str, Any]):
    """command Decorator

    コマンドの作成に用います。

    Parameters
    ----------
    name : Optional[str], optional
        コマンドの名前, by default None
    cls : Any, optional
        自前のクラスを使用する場合, by default None

    Returns
    -------
    Command
        コマンドクラス

    Raises
    ------
    TypeError
        Callback is already a command.
    """
    if cls is None:
        cls = Command

    def decorator(func: Callable[..., Coroutine[Any, Any, Any]]):
        if isinstance(func, Command):
            raise TypeError('Callback is already a command.')
        return cls(func, name=name, **attrs)

    return decorator
