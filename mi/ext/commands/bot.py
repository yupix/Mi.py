"""Commands FrameWork用のCore部分"""

import asyncio
import importlib
import inspect
import re
import sys
import traceback
from types import ModuleType
from typing import Any, Callable, Coroutine, Dict, Optional

import rich

from mi import UserProfile, config, utils
from mi.conn import get_instance_meta
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
from mi.http import WebSocket
from mi.user import UserAction

__all__ = ["BotBase", "Bot"]

from mi.utils import get_module_logger


class BotBase(GroupMixin):
    def __init__(self, command_prefix, **options):
        super().__init__(**options)
        self.command_prefix = command_prefix
        self.extra_events = {}
        self.special_events = {}
        self._check_once = []
        self._checks = []
        self._after_invoke = None
        self.token = None
        self.origin_uri = None
        self.__extensions: Dict[str, Any] = {}
        self.i: UserProfile = None
        self.__cogs: Dict[str] = {}
        self.strip_after_prefix = options.get("strip_after_prefix", False)
        self.logger = get_module_logger(__name__)

    async def can_run(self, ctx, *, call_once=False):
        data = self._check_once if call_once else self._checks

        if len(data) == 0:
            return True

        return await utils.async_all(f(ctx) for f in data)

    async def invoke(self, ctx, *args, **kwargs) -> bool:
        if not ctx.command:
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
            await self.dispatch("missing_command", invoker)
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

        await self.dispatch("message", message)

    async def _on_message(self, message):
        await self.process_commands(message)

    def event(self, name=None):
        def decorator(func):
            self.add_event(func, name)
            return func

        return decorator

    def add_event(self, func, name=None):
        name = func.__name__ if name is None else name
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Listeners must be coroutines")

        if name in self.extra_events:
            self.special_events[name].append(func)
        else:
            self.special_events[name] = [func]

    def listen(self, name=None):
        def decorator(func):
            self.add_listener(func, name)
            return func

        return decorator

    def add_listener(self, func, name=None):
        name = func.__name__ if name is None else name
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Listeners must be coroutines")

        if name in self.extra_events:
            self.extra_events[name].append(func)
        else:
            self.extra_events[name] = [func]

    async def event_dispatch(self, event_name, *args, **kwargs) -> bool:
        """on_ready等といった

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

    async def dispatch(self, event_name, *args, **kwargs):
        ev = "on_" + event_name
        for event in self.extra_events.get(ev, []):
            if inspect.ismethod(event):
                coro = event
                event = event.__name__
            else:
                foo = importlib.import_module(event.__module__)
                coro = getattr(foo, ev)
            await self.schedule_event(coro, event, *args, **kwargs)
        if ev in dir(self):
            await self.schedule_event(getattr(self, ev), ev, *args, **kwargs)

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

    def load_extension(self, name: str, *, package: Optional[str] = None) -> None:
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

    async def schedule_event(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        event_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> asyncio.Task:
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

    def run(self, uri: str, token: str, debug: bool = False) -> None:
        """
        Launch the bot.
        Parameters
        ----------
        uri : str
            websocket url of the Misskey instance to connect to
        token : str
            Misskey account token
        debug : bool
            Debug Mode

        Examples
        --------

        When inheriting from a class: ::

            class MyBot(Bot):
                async def on_message(self, ws, message):
                    pass
            bot = MyBot()
            bot.run(uri, token)

        When using a listener: ::

            bot = Bot()

            @bot.event()
            async def on_message(ws, message):
                pass

            bot.run(uri, token)

        Returns
        -------
        None: None
        """
        self.token = token
        if _origin_uri := re.search(r"wss?://(.*)/streaming", uri):
            origin_uri = (
                _origin_uri.group(0)
                .replace("wss", "https")
                .replace("ws", "http")
                .replace("/streaming", "")
            )
        else:
            origin_uri = uri
        self.origin_uri = origin_uri[:-1] if uri[-1] == "/" else origin_uri
        auth_i = {
            "token": self.token,
            "origin_uri": self.origin_uri,
        }
        config.i = config.Config(**auth_i)
        config.debug = debug
        self.i = UserAction().get_i()
        auth_i["profile"] = self.i
        auth_i["instance"] = get_instance_meta()
        config.i = config.Config(**auth_i)
        asyncio.get_event_loop().run_until_complete(
            WebSocket(self).run(f"{uri}?i={token}")
        )


class Bot(BotBase):
    pass
