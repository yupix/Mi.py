import asyncio
import importlib
import re
import sys
import traceback
from typing import Any, Callable, Coroutine

from mi import UserProfile, config
from mi.conn import Controller
from mi.http import WebSocket
from mi.user import UserAction
from mi.utils import get_module_logger


class BotBase:
    def __init__(self):
        self.extra_events = {}
        self.special_events = {}
        self.token = None
        self.origin_uri = None
        self.i: UserProfile = None
        self.logger = get_module_logger(__name__)

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

    async def _on_message(self, message):
        await self.dispatch("on_message", message)

    def add_listener(self, func, name=None):
        name = func.__name__ if name is None else name
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Listeners must be coroutines")

        if name in self.extra_events:
            self.extra_events[name].append(func)
        else:
            self.extra_events[name] = [func]

    async def event_dispatch(self, event_name, *args, **kwargs):
        ev = "on_" + event_name
        for event in self.special_events.get(ev, []):
            foo = importlib.import_module(event.__module__)
            coro = getattr(foo, ev)
            await self.schedule_event(coro, event, *args, **kwargs)

    async def dispatch(self, event_name, *args, **kwargs):
        ev = "on_" + event_name
        for event in self.extra_events.get(ev, []):
            foo = importlib.import_module(event.__module__)
            coro = getattr(foo, ev)
            await self.schedule_event(coro, event, *args, **kwargs)

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
                await self.__on_error(event_name, *args, **kwargs)
            except asyncio.CancelledError:
                pass

    async def __on_error(self, event_method: str) -> None:
        print(f"Ignoring exception in {event_method}", file=sys.stderr)
        traceback.print_exc()

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
        auth_i["instance"] = Controller.get_instance_meta()
        config.i = config.Config(**auth_i)
        asyncio.get_event_loop().run_until_complete(
            WebSocket(self).run(f"{uri}?i={token}")
        )


class Client(BotBase):
    pass
