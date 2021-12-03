from __future__ import annotations
import asyncio
import importlib
import inspect
import re
import sys
import traceback
from functools import cache
from typing import Any, Callable, Coroutine, Dict, Iterator, List, Optional, TYPE_CHECKING, Tuple, Union

import requests
from websockets.legacy.client import WebSocketClientProtocol

from mi import config
from mi.exception import InvalidParameters, NotExistRequiredParameters
from mi.http import WebSocket
from mi.next_utils import check_multi_arg
from mi.note import NoteContent
from mi.state import ConnectionState
from mi.utils import api, get_module_logger, remove_dict_empty, upper_to_lower

if TYPE_CHECKING:
    from . import UserProfile

class Client:
    def __init__(self, **options: Dict[Any, Any]):
        super().__init__(**options)
        self.extra_events: Dict[str, Any] = {}
        self.special_events: Dict[str, Any] = {}
        self.token: Optional[str] = None
        self.origin_uri: Optional[str] = None
        self._connection:ConnectionState = ConnectionState(self.dispatch)
        self.i: UserProfile = None
        self.logger = get_module_logger(__name__)
        self.loop = asyncio.get_event_loop()

    async def on_ready(self, ws: WebSocketClientProtocol):
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

    async def event_dispatch(self, event_name: str, *args: Tuple[Any], **kwargs: Dict[Any, Any]) -> bool:
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

    async def dispatch(self, event_name: str, *args: tuple[Any], **kwargs: Dict[Any, Any]):
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

    async def schedule_event(
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

    async def _on_message(self, message):
        await self.dispatch("message", message)

    @staticmethod
    async def __on_error(event_method: str) -> None:
        print(f"Ignoring exception in {event_method}", file=sys.stderr)
        traceback.print_exc()

    async def on_error(self, err):
        await self.event_dispatch("error", err)

    # ここからクライアント操作

    @staticmethod
    async def delete_chat(message_id: str) -> requests.models.Response:
        args = {"messageId": f"{message_id}"}
        return api(
            '/api/messaging/messages/delete',
            json_data=args,
            auth=True
        )

    @staticmethod
    def get_user_notes(
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
            file_type: list = None,
            since_date: int = 0,
            until_data: int = 0
    ) -> Iterator[NoteContent]:
        if limit > 100:
            raise InvalidParameters("limit は100以上を受け付けません")

        args = remove_dict_empty(
            {
                "userId": user_id,
                "includeReplies": include_replies,
                "limit": limit,
                "sinceId": since_id,
                "untilId": until_id,
                "sinceDate": since_date,
                "untilDate": until_data,
                "includeMyRenotes": include_my_renotes,
                "withFiles": with_files,
                "fileType": file_type,
                "excludeNsfw": exclude_nsfw
            }
        )
        if get_all:
            loop = True
            while loop:
                get_data = api("/api/users/notes", json_data=args,
                               auth=True).json()
                if len(get_data) <= 0:
                    break
                args["untilId"] = get_data[-1]["id"]
                for data in get_data:
                    yield NoteContent(upper_to_lower(data,
                                                     replace_list={"user": "author",
                                                                   "text": "content"}))
        else:
            get_data = api("/api/users/notes", json_data=args,
                           auth=True).json()
            for data in get_data:
                yield NoteContent(upper_to_lower(data,
                                                 replace_list={"user": "author",
                                                               "text": "content"}))

    @staticmethod
    @cache
    def get_instance_meta() -> Dict[str, Tuple[str, List[str], Dict[str, Any]]]:
        """
        BOTのアカウントがあるインスタンス情報をdictで返します。一度実行するとキャッシュされます。

        Returns
        -------
        dict:
            インスタンス情報
        """
        return api("/api/meta").json()

    @staticmethod
    def fetch_instance_meta() -> dict:
        """
        BOTのアカウントがある最新のインスタンス情報をdictで返します

        Returns
        -------
        dict:
            インスタンス情報
        """
        Client.get_instance_meta.cache_clear()
        return api("/api/meta").json()

    @staticmethod
    @cache
    def get_user(user_id: Optional[str] = None, username: Optional[str] = None,
                 host: Optional[str] = None) -> Dict[str, Tuple[str, List[Any], Dict[str, Any]]]:
        """
        ユーザーのプロフィールを取得します。一度のみサーバーにアクセスしキャッシュをその後は使います。
        fetch_userを使った場合はキャッシュが廃棄され再度サーバーにアクセスします。

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
        dict:
            ユーザー情報
        """
        return Client.fetch_user(user_id, username, host)

    @staticmethod
    def fetch_user(user_id: Optional[str] = None, username: Optional[str] = None,
                   host: Optional[str] = None) -> Dict[str, Tuple[str, List[Any], Dict[str, Any]]]:
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
        dict:
            ユーザー情報
        """
        if not check_multi_arg(user_id, username):
            raise NotExistRequiredParameters("user_id, usernameどちらかは必須です")

        data = remove_dict_empty(
            {"userId": user_id, "username": username, "host": host})
        Client.get_user.cache_clear()
        return UserProfile(**upper_to_lower(api("/api/users/show", json_data=data, auth=True).json()))

    @staticmethod
    def file_upload(
            name: Optional[str] = None,
            to_file: Optional[str] = None,
            to_url: Optional[str] = None,
            *,
            force: bool = False,
            is_sensitive: bool = False,
    ) -> dict:
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
        Drive: Drive
            upload後のレスポンスをDrive型に変更して返します
        """

        if to_file and to_url is None:  # ローカルからアップロードする
            with open(to_file, "rb") as f:
                file = f.read()
            args = {"isSensitive": is_sensitive, "force": force,
                    "name": f"{name}"}
            file = {"file": file}
            res = api(
                "/api/drive/files/create", json_data=args, files=file,
                auth=True
            ).json()
        elif to_file is None and to_url:  # URLからアップロードする
            args = {"url": to_url, "force": force, "isSensitive": is_sensitive}
            res = api("/api/drive/files/upload-from-url", json_data=args,
                      auth=True).json()
        else:
            raise InvalidParameters("path または url のどちらかは必須です")
        return res

    @staticmethod
    def get_announcements(limit: int, with_unreads: bool, since_id: str,
                          until_id: str):
        """

        Parameters
        ----------
        limit: int
            最大取得数
        with_unreads: bool
            既読済みか否か
        since_id: str
        until_id: str
            前回の最後の値を与える(既に実行し取得しきれない場合に使用)

        Returns
        -------

        """

        if limit > 100:
            raise InvalidParameters("limit は100以上を受け付けません")

        args = {
            "limit": limit,
            "withUnreads": with_unreads,
            "sinceId": since_id,
            "untilId": until_id,
        }
        return api("/api/announcements", args, auth=True)

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
        auth_i: Dict[str, Any] = {
            "token": self.token,
            "origin_uri": self.origin_uri,
        }
        config.i = config.Config(**auth_i)
        config.debug = debug
        self.i = self._connection._get_i()
        auth_i["profile"] = self.i
        auth_i["instance"] = self.get_instance_meta()
        config.i = config.Config(**auth_i)
        asyncio.get_event_loop().run_until_complete(
            WebSocket(self).run(f"{uri}?i={token}")
        )
