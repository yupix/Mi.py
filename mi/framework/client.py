from __future__ import annotations

import asyncio
import importlib
import inspect
import re
import sys
import traceback
from typing import TYPE_CHECKING, Any, AsyncIterator, Callable, Coroutine, Dict, List, Optional, Tuple, Union
from mi.exception import WebSocketRecconect

import mi.framework.http
import mi.framework.manager as manager
from aiohttp import ClientWebSocketResponse
from mi import config
from mi.framework.models.chat import Chat
from mi.framework.models.instance import Instance, InstanceMeta
from mi.framework.models.note import Note
from mi.framework.models.user import User
from mi.framework.state import ConnectionState
from mi.utils import get_module_logger
from mi.wrapper.models.user import RawUser

from .gateway import MisskeyWebSocket

if TYPE_CHECKING:
    from . import File


class Client:
    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None, **options: Dict[Any, Any]):
        super().__init__(**options)
        self.url = None
        self.extra_events: Dict[str, Any] = {}
        self.special_events: Dict[str, Any] = {}
        self.token: Optional[str] = None
        self.origin_uri: Optional[str] = None
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.http = mi.framework.http.HTTPSession
        self._connection: ConnectionState = self._get_state(**options)
        self.user: User = None
        self.logger = get_module_logger(__name__)
        self.ws: MisskeyWebSocket = None

    def _get_state(self, **options: Any) -> ConnectionState:
        return ConnectionState(dispatch=self.dispatch, loop=self.loop, client=self)

    async def on_ready(self, ws: ClientWebSocketResponse):
        """
        on_readyのデフォルト処理

        Parameters
        ----------
        ws : WebSocketClientProtocol
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

    def event_dispatch(self, event_name: str, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> bool:
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
            self.schedule_event(coro, event, *args, **kwargs)
        if ev in dir(self):
            self.schedule_event(getattr(self, ev), ev, *args, **kwargs)
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

    def schedule_event(
            self,
            coro: Callable[..., Coroutine[Any, Any, Any]],
            event_name: str,
            *args: tuple[Any],
            **kwargs: Dict[Any, Any],
    ) -> asyncio.Task[Any]:
        return self.loop.create_task(
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
        self.event_dispatch("error", err)

    # ここからクライアント操作

    @property
    def client(self) -> manager.ClientActions:
        return manager.ClientActions()

    async def get_user_notes(
            self,
            user_id: str,
            *,
            since_id: Optional[str] = None,
            include_my_renotes: bool = True,
            include_replies: bool = True,
            with_files: bool = False,
            until_id: Optional[str] = None,
            limit: int = 10,
            get_all: bool = False,
            exclude_nsfw: bool = True,
            file_type: Optional[List[str]] = None,
            since_date: int = 0,
            until_data: int = 0
    ) -> AsyncIterator[Note]:
        return self._connection.get_user_notes(user_id=user_id, since_id=since_id, include_my_renotes=include_my_renotes,
                                               include_replies=include_replies, with_files=with_files,
                                               until_id=until_id, limit=limit, get_all=get_all, exclude_nsfw=exclude_nsfw,
                                               file_type=file_type, since_date=since_date, until_data=until_data)

    async def get_instance(self, host: Optional[str] = None) -> Union[Instance, InstanceMeta]:
        """
        BOTのアカウントがあるインスタンス情報をdictで返します。一度実行するとキャッシュされます。

        Returns
        -------
        Union[Instance, InstanceMeta]
            インスタンス情報
        """

        return await self._connection.get_instance(host=host)

    async def fetch_instance(self, host: Optional[str] = None) -> Union[Instance, InstanceMeta]:
        """
        BOTのアカウントがある最新のインスタンス情報をdictで返します

        Returns
        -------
        Union[Instance, InstanceMeta]
            インスタンス情報
        """

        return await self._connection.fetch_instance(host=host)

    async def get_i(self) -> User:
        """
        BOTアカウントの情報を取得します
        """

        return await self._connection.get_i()

    async def file_upload(
            self,
            name: Optional[str] = None,
            to_file: Optional[str] = None,
            to_url: Optional[str] = None,
            *,
            force: bool = False,
            is_sensitive: bool = False,
    ) -> File:
        """
        Parameters
        ----------
        is_sensitive : bool
            この画像がセンシティブな物の場合Trueにする
        force : bool
            Trueの場合同じ名前のファイルがあった場合でも強制的に保存する
        to_file : str
            そのファイルまでのパスとそのファイル.拡張子(/home/test/test.png)
        name: str
            ファイル名(拡張子があるなら含めて)
        to_url : str
            アップロードしたいファイルのURL

        Returns
        -------
        Drive: File
            upload後のレスポンスをDrive型に変更して返します
        """

        return await self._connection.file_upload(name=name, to_file=to_file, to_url=to_url, force=force,
                                                  is_sensitive=is_sensitive)

    async def login(self, token):
        data = await mi.framework.http.HTTPSession.static_login(token)
        self.user = User(RawUser(data))

    async def connect(self, *, reconnect: bool = True, timeout: int = 60, event_name: str='ready') -> None:

        coro = MisskeyWebSocket.from_client(self, timeout=timeout, event_name=event_name)
        try:
            self.ws = await asyncio.wait_for(coro, timeout=60)
        except asyncio.exceptions.TimeoutError:
            await self.connect(reconnect=reconnect, timeout=timeout)

        while True:
            try:
                await self.ws.poll_event()
            except WebSocketRecconect:
                await self.connect(event_name='reconnect')


    async def start(self, url: str, token: str, *, debug: bool = False, reconnect: bool = True, timeout: int = 60,
                    is_ayuskey: bool = False):
        """
        Starting Bot

        Parameters
        ----------
        url: str
            Misskey Instance Websocket URL (wss://example.com)
        token: str
            User Token
        debug: bool, default False
            debugging mode
        reconnect: bool, default True
            coming soon...
        timeout: int, default 60
            Time until websocket times out
        """

        self.token = token
        if _origin_uri := re.search(r"wss?://(.*)/streaming", url):
            origin_uri = (
                _origin_uri.group(0)
                    .replace("wss", "https")
                    .replace("ws", "http")
                    .replace("/streaming", "")
            )
        else:
            origin_uri = url
        self.origin_uri = origin_uri[:-1] if url[-1] == "/" else origin_uri
        self.url = url
        auth_i: Dict[str, Any] = {
            "token": self.token,
            "origin_uri": self.origin_uri,
        }
        config.i = config.Config(**auth_i)
        config.debug = debug
        config.is_ayuskey = is_ayuskey
        await self.login(token)
        await self.connect(reconnect=reconnect, timeout=timeout)
