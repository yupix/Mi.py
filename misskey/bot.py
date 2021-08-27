import asyncio
import importlib
import sys
import traceback
from typing import Any, Callable, Coroutine

from misskey.http import WebSocket


class BotBase(WebSocket):
    def __init__(self, **options):
        self.extra_events = {}
        self.special_events = {}
        super().__init__(self)

    def event(self, name=None):
        def decorator(func):
            self.add_event(func, name)
            return func

        return decorator

    def add_event(self, func, name=None):
        name = func.__name__ if name is None else name
        if not asyncio.iscoroutinefunction(func):
            raise TypeError('Listeners must be coroutines')

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
            raise TypeError('Listeners must be coroutines')

        if name in self.extra_events:
            self.extra_events[name].append(func)
        else:
            self.extra_events[name] = [func]

    async def event_dispatch(self, event_name, *args, **kwargs):
        ev = 'on_' + event_name
        for event in self.special_events.get(ev, []):
            foo = importlib.import_module(event.__module__)
            coro = getattr(foo, ev)
            await self.schedule_event(coro, event, *args, **kwargs)

    async def dispatch(self, event_name, *args, **kwargs):
        ev = 'on_' + event_name
        for event in self.extra_events.get(ev, []):
            foo = importlib.import_module(event.__module__)
            coro = getattr(foo, ev)
            await self.schedule_event(coro, event, *args, **kwargs)

    async def schedule_event(self, coro: Callable[..., Coroutine[Any, Any, Any]], event_name: str, *args: Any,
                             **kwargs: Any) -> asyncio.Task:
        return asyncio.create_task(self._run_event(coro, event_name, *args, **kwargs), name=f'MI.py: {event_name}')

    async def _run_event(self, coro: Callable[..., Coroutine[Any, Any, Any]], event_name: str, *args: Any,
                         **kwargs: Any) -> None:
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
        print(f'Ignoring exception in {event_method}', file=sys.stderr)
        traceback.print_exc()

    async def on_error(self, err):
        await self.event_dispatch('error', err)

    async def on_message(self, ws, message):
        """デフォルト処理"""
        await self.dispatch('message', ws, message)

    async def on_response(self, ws, message):
        await self.dispatch('response', ws, message)

    async def on_ready(self, ws):
        await self.event_dispatch('ready', ws)

    async def on_reacted(self, ws, message):
        await self.dispatch('reaction', ws, message)

    async def on_deleted(self, ws, message):
        await self.dispatch('deleted', ws, message)

    def run(self, uri: str, token: str) -> None:
        """
        Launch the bot.
        Parameters
        ----------
        uri : str
            websocket url of the Misskey instance to connect to
        token : str
            Misskey account token

        None

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
        """

        asyncio.get_event_loop().run_until_complete(self._run(f'{uri}?i={token}'))


class Bot(BotBase):
    pass
