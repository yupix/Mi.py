"""Commands FrameWork用のCore部分"""

from __future__ import annotations
import asyncio
import importlib
import inspect
import sys
import traceback
from types import ModuleType
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Dict, List, Optional, Tuple, Union

from mi import Client, User, utils
from mi.abc.ext.bot import AbstractBotBase
from mi.exception import (
    CheckFailure,
    CogNameDuplicate,
    CommandError,
    ExtensionAlreadyLoaded,
    ExtensionFailed,
    ExtensionNotFound,
    InvalidCogPath,
    NoEntryPointError,
)
from mi.ext.commands.context import Context
from mi.ext.commands.core import GroupMixin
from mi.ext.commands.view import StringView
from mi.utils import get_module_logger

if TYPE_CHECKING:
    from aiohttp.client_ws import ClientWebSocketResponse

__all__ = ["BotBase", "Bot"]


class BotBase(GroupMixin, AbstractBotBase):
    def __init__(self, command_prefix: str, **options: Dict[Any, Any]):
        super().__init__(**options)
        self.command_prefix = command_prefix
        self.extra_events: Dict[str, Any] = {}
        self.special_events: Dict[str, Any] = {}
        self._check_once: List[Any] = []  # TODO: いつか確認する
        self._checks: List[Any] = []  # TODO: いつか確認する
        self._after_invoke = None
        self.token: Optional[str] = None
        self.origin_uri: Optional[str] = None
        self.__extensions: Dict[str, Any] = {}
        self.i: User = None
        self.__cogs: Dict[str, str] = {}
        self.strip_after_prefix = options.get("strip_after_prefix", False)
        self.logger = get_module_logger(__name__)
        self.loop = asyncio.get_event_loop()

    async def can_run(self, ctx: Context, *, call_once: bool = False) -> bool:
        data = self._check_once if call_once else self._checks

        if len(data) == 0:
            return True

        return await utils.async_all(f(ctx) for f in data)

    async def invoke(self, ctx: Context, *args: Tuple[Any], **kwargs: Dict[Any, Any]):
        if ctx.command is None:
            return False
        try:
            if not await self.can_run(ctx, call_once=True):
                raise CheckFailure("")
            await ctx.command.invoke(ctx, *args, **kwargs)
            return True
        except CommandError as exc:
            await ctx.command.dispatch_error(ctx, exc)

    async def get_context(self, message, *, cls=Context):
        ctx = cls(bot=self, message=message)
        if message.content is None:
            return ctx
        view = StringView(message.content)
        if view.skip_string(self.command_prefix) is False:  # prefixがテキストに含まれているか確認
            return ctx
        invoker = view.get_word()
        if not self.all_commands.get(invoker):
            self.dispatch("missing_command", invoker)
        ctx.message.content = message.content.replace(
            self.command_prefix + invoker, ""
        ).strip(" ")
        ctx.command = self.all_commands.get(invoker)
        return ctx

    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        if ctx.message.content:
            await self.invoke(ctx, *ctx.message.content.split(" "))
        else:
            await self.invoke(ctx)

        self.dispatch("message", message)

    async def _on_message(self, message):
        await self.process_commands(message)

    async def on_ready(self, ws: ClientWebSocketResponse):
        """
        on_readyのデフォルト処理

        Parameters
        ----------
        ws : ClientWebSocketResponse
        """

    def event(self, name: Optional[str] = None):
        def decorator(func: Coroutine[Any, Any, Any]):
            self.add_event(func, name)
            return func

        return decorator

    def add_event(self, func: Coroutine[Any, Any, Any], name: Optional[str] = None):
        name = func.__name__ if name is None else name
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Listeners must be coroutines")

        if name in self.extra_events:
            self.special_events[name].append(func)
        else:
            self.special_events[name] = [func]

    def listen(self, name: Optional[str] = None):
        def decorator(func: Coroutine[Any, Any, Any]):
            self.add_listener(func, name)
            return func

        return decorator

    def add_listener(self, func: Union[Coroutine[Any, Any, Any], Callable[..., Any]], name: Optional[str] = None):
        name = func.__name__ if name is None else name
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Listeners must be coroutines")

        if name in self.extra_events:
            self.extra_events[name].append(func)
        else:
            self.extra_events[name] = [func]

    async def event_dispatch(self, event_name: str, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> bool:
        """
        on_ready等といった

        Parameters
        ----------
        event_name :
        args :
        kwargs :

        Returns
        -------

        """
        ev = "on_" + event_name
        for event in self.special_events.get(ev, []):
            foo = importlib.import_module(event.__module__)
            coro = getattr(foo, ev)
            await self.schedule_event(coro, event, *args, **kwargs)
        if ev in dir(self):
            await self.schedule_event(getattr(self, ev), ev, *args, **kwargs)
        return ev in dir(self)

    def dispatch(self, event_name: str, *args: tuple[Any], **kwargs: Dict[Any, Any]):
        ev = "on_" + event_name
        for event in self.extra_events.get(ev, []):
            if inspect.ismethod(event):
                coro = event
                event = event.__name__
            else:
                foo = importlib.import_module(event.__module__)
                coro = getattr(foo, ev)
            self.schedule_event(coro, event, *args, **kwargs)
        if ev in dir(self):
            self.schedule_event(getattr(self, ev), ev, *args, **kwargs)

    def add_cog(self, cog, override: bool = False) -> None:
        cog_name = cog.__cog_name__
        existing = self.__cogs.get(cog_name)
        if existing is not None:
            if not override:
                raise CogNameDuplicate()
            self.remove_cog(cog_name)  # TODO: 作る

        cog = cog._inject(self)
        self.__cogs[cog_name] = cog

    def remove_cog(self, name: str):  # TODO: Optional[Cog]を返すように
        """Cogを削除します"""
        cog = self.__cogs.get(name)
        if cog is None:
            return

        cog._eject(self)

        return cog

    def _load_from_module(self, spec: ModuleType, key: str) -> None:
        try:
            setup = spec.setup
        except AttributeError:
            raise NoEntryPointError(f"{key} にsetupが存在しません")

        try:
            setup(self)
        except Exception as e:
            raise ExtensionFailed(key, e) from e
        else:
            self.__extensions[key] = spec

    @staticmethod
    def _resolve_name(name: str, package: Optional[str]) -> str:
        try:
            return importlib.util.resolve_name(name, package)
        except ImportError:
            raise ExtensionNotFound(name)

    def load_extension(self, name: str, *,
                       package: Optional[str] = None) -> None:
        """拡張をロードする

        Parameters
        ----------
        name : str
            [description]
        package : Optional[str], optional
            [description], by default None
        """
        name = self._resolve_name(name, package)
        if name in self.__extensions:
            raise ExtensionAlreadyLoaded
        try:
            module = importlib.import_module(name)
        except ModuleNotFoundError:
            raise InvalidCogPath(f"cog: {name} へのパスが無効です")
        self._load_from_module(module, name)

    def schedule_event(
            self,
            coro: Callable[..., Coroutine[Any, Any, Any]],
            event_name: str,
            *args: tuple[Any],
            **kwargs: Dict[Any, Any],
    ) -> asyncio.Task[Any]:
        return asyncio.create_task(
            self._run_event(coro, event_name, *args, **kwargs),
            name=f"MI.py: {event_name}",
        )

    async def _run_event(
            self,
            coro: Callable[..., Coroutine[Any, Any, Any]],
            event_name: str,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            try:
                await self.__on_error(event_name)
            except asyncio.CancelledError:
                pass

    @staticmethod
    async def __on_error(event_method: str) -> None:
        print(f"Ignoring exception in {event_method}", file=sys.stderr)
        traceback.print_exc()

    async def on_error(self, err):
        await self.event_dispatch("error", err)


class Bot(BotBase, Client):
    pass
