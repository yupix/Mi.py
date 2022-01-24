from __future__ import annotations

import asyncio
import importlib
import inspect
import re
import sys
import traceback
from typing import Any, AsyncIterator, Callable, Coroutine, Dict, List, Optional, TYPE_CHECKING, Tuple, Union

import aiohttp
from aiohttp import ClientWebSocketResponse

from mi import Instance, InstanceMeta, User, config
from mi.chat import Chat
from mi.http import HTTPClient
from mi.models.user import RawUser
from mi.note import Note
from mi.state import ClientActions, ConnectionState
from mi.utils import get_module_logger
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
        connector: Optional[aiohttp.BaseConnector] = options.pop('connector', None)
        self.http: HTTPClient = HTTPClient(connector=connector)
        self._connection: ConnectionState = self._get_state(**options)
        self.i: User = None
        self.logger = get_module_logger(__name__)
        self.ws: MisskeyWebSocket = None

    def _get_state(self, **options: Any) -> ConnectionState:
        return ConnectionState(dispatch=self.dispatch, http=self.http, loop=self.loop, client=self)

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

    async def progress_command(self, message):
        for cmd in self.all_commands:
            print(cmd)
            if cmd.cmd_type == 'regex':
                if re.search(cmd.key, message.content):
                    hit_list = re.findall(cmd.key, message.content)
                    if isinstance(hit_list, tuple):
                        hit_list = hit_list[0]
                    await cmd.func.invoke(message, *hit_list)
            elif message.content.find(cmd.key) != -1:
                await cmd.func.invoke(message)
            else:
                continue

    async def on_mention(self, message):
        await self.progress_command(message)

    async def on_error(self, err):
        await self.event_dispatch("error", err)

    # ここからクライアント操作

    @property
    def client(self) -> ClientActions:
        return self._connection.get_client_actions()

    async def post_chat(self, content: str, *, user_id: str = None, group_id: str = None, file_id: str = None) -> Chat:
        """
        チャットを送信します。

        Parameters
        ----------
        content : str
            テキスト
        user_id : str, optional
            送信対象のユーザーid, by default None
        group_id : str, optional
            送信対象のグループid, by default None
        file_id : str, optional
            添付するファイルid, by default None

        Returns
        -------
        None
        """

        return await self._connection.post_chat(content, user_id=user_id, group_id=group_id, file_id=file_id)

    async def delete_chat(self, message_id: str) -> bool:
        """
        指定されたIDのチャットを削除します。

        Parameters
        ----------
        message_id : str
            削除するメッセージのid

        Returns
        -------
        bool
            削除に成功したかどうか
        """

        return await self._connection.delete_chat(message_id=message_id)

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

    async def get_user(self, user_id: Optional[str] = None, username: Optional[str] = None,
                       host: Optional[str] = None) -> User:
        """
        ユーザーのプロフィールを取得します。一度のみサーバーにアクセスしキャッシュをその後は使います。
        fetch_userを使った場合はキャッシュが廃棄され再度サーバーにアクセスします。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
        host : str, default=None
            取得したいユーザーのユーザー名
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        dict
            ユーザー情報
        """

        return await self._connection.get_user(user_id=user_id, username=username, host=host)

    async def fetch_user(self, user_id: Optional[str] = None, username: Optional[str] = None,
                         host: Optional[str] = None) -> User:
        """
        サーバーにアクセスし、ユーザーのプロフィールを取得します。基本的には get_userをお使いください。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        dict
            ユーザー情報
        """

        return await self._connection.fetch_user(user_id=user_id, username=username, host=host)

    async def get_drive_folders(self, limit: int = 100, since_id: Optional[str] = None, until_id: Optional[str] = None,
                                folder_id: Optional[str] = None):
        return await self._connection.drive.action.get_folders(limit, since_id, until_id, folder_id)

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

    async def show_file(self, file_id: Optional[str] = None, url: Optional[str] = None) -> File:
        """
        ファイルの情報を取得します。

        Parameters
        ----------
        file_id : Optional[str], default=None
            ファイルのID
        url : Optional[str], default=None
            ファイルのURL

        Returns
        -------
        File
            ファイルの情報
        """

        return await self._connection.show_file(file_id=file_id, url=url)

    async def remove_file(self, file_id: str) -> bool:
        """
        指定したファイルIDのファイルを削除します
        
        Parameters
        ----------
        file_id:str
            削除したいファイルのID
        
        Returns
        -------
        bool
            削除に成功したかどうか
        """

        return await self._connection.remove_file(file_id=file_id)

    async def get_announcements(self, limit: int, with_unreads: bool, since_id: str, until_id: str):
        return await self._connection.get_announcements(limit=limit, with_unreads=with_unreads, since_id=since_id,
                                                        until_id=until_id)

    async def get_note(self, note_id: str) -> Note:
        """
        ノートを取得
        Parameters
        ----------
        note_id:str
            取得したいノートのID
        
        Returns
        -------
        Note
            取得したノート
        """

        return await self._connection.get_note(note_id=note_id)

    async def get_replies(self, note_id: str, since_id: Optional[str] = None, until_id: Optional[str] = None,
                          limit: int = 1) -> List[Note]:
        """
        ノートに対する返信を取得します
        
        Parameters
        ----------
        note_id : str
            返信を取得したいノートのID
        since_id: Optional[str], default=None
        until_id: Optional[str], default=None
            前回の最後のidから取得する場合
        limit: int, default=10
            取得する件数
        
        Returns
        -------
        List[Note]
            ノートに対する返信一覧
        """

        return await self._connection.get_replies(note_id=note_id, limit=limit, since_id=since_id, until_id=until_id)

    async def login(self, token):
        data = await self.http.static_login(token)
        self.i = User(RawUser(data), state=self._connection)

    async def connect(self, *, reconnect: bool = True, timeout: int = 60) -> None:

        coro = MisskeyWebSocket.from_client(self, timeout=timeout)
        try:
            self.ws = await asyncio.wait_for(coro, timeout=60)
        except asyncio.exceptions.TimeoutError:
            await self.connect(reconnect=reconnect, timeout=timeout)

        while True:
            await self.ws.poll_event()

    async def start(self, url: str, token: str, *, debug: bool = False, reconnect: bool = True, timeout: int = 60):
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
        await self.login(token)
        await self.connect(reconnect=reconnect, timeout=timeout)
