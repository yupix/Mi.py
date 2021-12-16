from __future__ import annotations

import asyncio
import inspect
from typing import Any, AsyncIterator, Callable, Dict, Iterator, List, Optional, TYPE_CHECKING, Union

from aiocache import cached
from aiocache.factory import Cache

from mi import Instance, InstanceMeta, User
from mi.chat import Chat
from mi.drive import Drive
from mi.exception import ContentRequired, InvalidParameters, NotExistRequiredParameters
from mi.http import Route
from mi.iterators import InstanceIterator
from mi.note import Note, Poll, Reaction
from mi.user import Follower
from mi.utils import api, check_multi_arg, get_cache_key, get_module_logger, key_builder, remove_dict_empty, str_lower, \
    upper_to_lower

if TYPE_CHECKING:
    from mi import HTTPClient
    from mi.types import (Note as NotePayload, Chat as ChatPayload)


class ConnectionState:
    def __init__(self, dispatch: Callable[..., Any], http: HTTPClient, loop: asyncio.AbstractEventLoop):
        self.dispatch = dispatch
        self.http: HTTPClient = http
        self.logger = get_module_logger(__name__)
        self.loop: asyncio.AbstractEventLoop = loop
        self.parsers = parsers = {}
        for attr, func in inspect.getmembers(self):
            if attr.startswith('parse'):
                parsers[attr[6:].upper()] = func

    def parse_channel(self, message: Dict[str, Any]) -> None:
        """parse_channel is a function to parse channel event

        チャンネルタイプのデータを解析後適切なパーサーに移動させます

        Parameters
        ----------
        message : Dict[str, Any]
            Received message
        """
        base_msg = upper_to_lower(message['body'])
        channel_type = str_lower(base_msg.get('type'))
        self.logger.debug(f'ChannelType: {channel_type}')
        self.logger.debug(f'recv event type: {channel_type}')
        getattr(self, f'parse_{channel_type}')(base_msg['body'])

    def parse_read_all_announcements(self, message: Dict[str, Any]) -> None:
        pass  # TODO: 実装

    def parse_reply(self, message: NotePayload) -> None:
        """
        リプライ
        """
        self.dispatch('message', Note(message, state=self))

    def parse_follow(self, message: Dict[str, Any]) -> None:
        """
        ユーザーをフォローした際のイベントを解析する関数
        """

        #self.dispatch('follow', Follower(message, state=self))

    def parse_followed(self, message: Dict[str, Any]) -> None:
        """
        フォローイベントを解析する関数
        """
        #self.dispatch('follow', Follower(message, state=self))

    def parse_mention(self, message: Dict[str, Any]) -> None:
        """
        メンションイベントを解析する関数
        """

    def parse_drive_file_created(self, message: Dict[str, Any]) -> None:
        pass  # TODO: 実装

    def parse_read_all_unread_mentions(self, message: Dict[str, Any]) -> None:
        pass  # TODO:実装

    def parse_read_all_unread_specified_notes(self, message: Dict[str, Any]) -> None:
        pass  # TODO:実装

    def parse_read_all_channels(self, message: Dict[str, Any]) -> None:
        pass  # TODO:実装

    def parse_read_all_notifications(self, message: Dict[str, Any]) -> None:
        pass  # TODO:実装

    def parse_messaging_message(self, message: ChatPayload) -> None:
        """
        チャットが来た際のデータを処理する関数
        """
        self.dispatch('message', Chat(message, state=self))

    def parse_unread_messaging_message(self, message: Dict[str, Any]) -> None:
        """
        チャットが既読になっていない場合のデータを処理する関数
        """
        self.dispatch('message', Chat(message, state=self))

    def parse_notification(self, message: Dict[str, Any]) -> None:
        """
        通知イベントを解析する関数

        Parameters
        ----------
        message: Dict[str, Any]
            Received message

        Returns
        -------
        None
        """
        notification_type = str_lower(message['type'])
        getattr(self, f'parse_{notification_type}')(message)

    def parse_poll_vote(self, message: Dict[str, Any]) -> None:
        pass  # TODO: 実装

    def parse_unread_notification(self, message: Dict[str, Any]) -> None:
        """
        未読の通知を解析する関数

        Parameters
        ----------
        message : Dict[str, Any]
            Received message
        """
        notification_type = str_lower(message['type'])
        getattr(self, f'parse_{notification_type}')(message)

    def parse_reaction(self, message: Dict[str, Any]) -> None:
        """
        リアクションに関する情報を解析する関数
        """
        self.dispatch('reaction', Reaction(message, state=self))

    def parse_note(self, message: Dict[str, Any]) -> None:
        """
        ノートイベントを解析する関数
        """
        note = Note(message, state=self)
        # Router(self.http.ws).capture_message(note.id) TODO: capture message
        self.dispatch('message', note)

    @staticmethod
    def follow_user(user_id: str) -> tuple[bool, Optional[str]]:
        """
        与えられたIDのユーザーをフォローします

        Parameters
        ----------
        user_id : Optional[str] = None
            フォローしたいユーザーのID

        Returns
        -------
        status: bool = False
            成功ならTrue, 失敗ならFalse
        """
        data = {"userId": user_id}
        res = api("/api/following/create", json_data=data, auth=True)
        if res.json().get("error"):
            code = res.json()["error"]["code"]
            status = False
        else:
            code = None
            status = True
        return status, code

    @staticmethod
    def unfollow_user(user_id: str) -> bool:
        """
        Parameters
        ----------
        user_id :
            フォローを解除したいユーザーのID

        Returns
        -------
        status: bool = False
            成功したならTrue, 失敗したならFalse
        """
        data = {"userId": user_id}
        res = api("/api/following/delete", json_data=data, auth=True)
        return bool(res.status_code == 204 or 200)

    async def get_i(self) -> User:
        res = await self.http.request(Route('POST', '/api/i'), auth=True, lower=True)
        return User(res, state=self)

    def get_users(self,
                  limit: int = 10,
                  *,
                  offset: int = 0,
                  sort: Optional[str] = None,
                  state: str = 'all',
                  origin: str = 'local',
                  username: Optional[str] = None,
                  hostname: Optional[str] = None,
                  get_all: bool = False) -> Iterator[User]:
        return InstanceIterator(self).get_users(limit=limit, offset=offset, sort=sort, state=state, origin=origin,
                                                username=username, hostname=hostname, get_all=get_all)

    @staticmethod
    async def add_reaction(reaction: str, note_id: Optional[str] = None) -> bool:
        """
        指定したnoteに指定したリアクションを付与します（内部用

        Parameters
        ----------
        reaction : Optional[str]
            付与するリアクション名
        note_id : Optional[str]
            付与対象のノートID

        Returns
        -------
        status: bool
            成功したならTrue,失敗ならFalse
        """
        data = remove_dict_empty({"noteId": note_id, "reaction": reaction})
        res = api("/api/notes/reactions/create", json_data=data, auth=True)
        return res.status_code == 204

    async def delete_note(self, note_id: str) -> bool:
        data = {"noteId": note_id}
        res = await self.http.request(Route('POST', '/api/notes/delete'), json=data, auth=True)
        return bool(res)

    @cached(ttl=10, namespace='get_user', key_builder=key_builder)
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
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        dict:
            ユーザー情報
        """
        field = remove_dict_empty({"userId": user_id, "username": username, "host": host})
        data = await self.http.request(Route('POST', '/api/users/show'), json=field, auth=True)
        return User(upper_to_lower(data), state=self)

    async def post_chat(self, content: str, *, user_id: str = None, group_id: str = None, file_id=None) -> Chat:
        args = remove_dict_empty({'userId': user_id, 'groupId': group_id, 'text': content, 'fileId': file_id})
        return Chat(await self.http.request(Route('POST', '/api/messaging/messages/create'), json=args, auth=True, lower=True),
                    state=self)

    async def delete_chat(self, message_id: str) -> bool:
        args = {'messageId': f'{message_id}'}
        data = await self.http.request(Route('POST', '/api/messaging/messages/delete'), json=args, auth=True)
        return bool(data)

    @get_cache_key
    async def fetch_user(self, user_id: Optional[str] = None, username: Optional[str] = None,
                         host: Optional[str] = None, **kwargs) -> User:
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

        field = remove_dict_empty({"userId": user_id, "username": username, "host": host})
        data = await self.http.request(Route('POST', '/api/users/show'), json=field, auth=True)
        old_cache = Cache(namespace='get_user')
        await old_cache.delete(kwargs['cache_key'].format('get_user'))
        return User(upper_to_lower(data), state=self)

    async def post_note(self,
                        content: str,
                        *,
                        visibility: str = "public",
                        visible_user_ids: Optional[List[str]] = None,
                        cw: Optional[str] = None,
                        local_only: bool = False,
                        no_extract_mentions: bool = False,
                        no_extract_hashtags: bool = False,
                        no_extract_emojis: bool = False,
                        reply_id: Optional[str] = None,
                        renote_id: Optional[str] = None,
                        channel_id: Optional[str] = None,
                        file_ids=None,
                        poll: Optional[Poll] = None
                        ):
        if file_ids is None:
            file_ids = []
        field = {
            "visibility": visibility,
            "visibleUserIds": visible_user_ids,
            "text": content,
            "cw": cw,
            "localOnly": local_only,
            "noExtractMentions": no_extract_mentions,
            "noExtractHashtags": no_extract_hashtags,
            "noExtractEmojis": no_extract_emojis,
            "replyId": reply_id,
            "renoteId": renote_id,
            "channelId": channel_id
        }
        if not check_multi_arg(content, file_ids, renote_id, poll):
            raise ContentRequired("ノートの送信にはcontent, file_ids, renote_id またはpollのいずれか1つが無くてはいけません")

        if poll and len(poll.choices) > 0:
            field["poll"] = poll
        if file_ids:
            field["fileIds"] = file_ids
        field = remove_dict_empty(field)
        res = await self.http.request(Route('POST', '/api/notes/create'), json=field, auth=True, lower=True)
        return Note(res["created_note"], state=self)

    async def get_followers(
            self,
            user_id: Optional[str] = None,
            username: Optional[str] = None,
            host: Optional[str] = None,
            since_id: Optional[str] = None,
            until_id: Optional[str] = None,
            limit: int = 10,
            get_all: bool = False,
    ) -> AsyncIterator[Follower]:
        """
        与えられたユーザーのフォロワーを取得します
        Parameters
        ----------
        user_id : str, default=None
            ユーザーのid
        username : str, default=None
            ユーザー名
        host : str, default=None
            ユーザーがいるインスタンスのhost名
        since_id : str, default=None
        until_id : str, default=None
            前回の最後の値を与える(既に実行し取得しきれない場合に使用)
        limit : int, default=10
            取得する情報の最大数 max: 100
        get_all : bool, default=False
            全てのフォロワーを取得する
        Yields
        ------
        dict
            フォロワーの情報
        Raises
        ------
        InvalidParameters
            limit引数が不正な場合
        """
        if not check_multi_arg(user_id, username):
            raise NotExistRequiredParameters("user_id, usernameどちらかは必須です")

        if limit > 100:
            raise InvalidParameters("limit は100以上を受け付けません")

        data = remove_dict_empty(
            {
                "userId": user_id,
                "username": username,
                "host": host,
                "sinceId": since_id,
                "untilId": until_id,
                "limit": limit,
            }
        )
        if get_all:
            loop = True
            while loop:
                get_data = await self.http.request(Route('POST', '/api/users/followers'), json=data, auth=True, lower=True)
                if len(get_data) > 0:
                    data["untilId"] = get_data[-1]["id"]
                else:
                    break
                for i in [Follower(i, state=self) for i in get_data]:
                    yield i
        else:
            get_data = await self.http.request(Route('POST', '/api/users/followers'), json=data, auth=True, lower=True)
            for i in [Follower(i, state=self) for i in get_data]:
                yield i

    @cached(ttl=10, key_builder=key_builder, key='get_instance')
    async def get_instance(self, host: Optional[str] = None, detail: bool = False) -> Union[InstanceMeta, Instance]:
        if host is None:
            data = await self.http.request(Route('POST', '/api/meta'), json={'detail': detail}, auth=True, lower=True)
            return InstanceMeta(data, state=self)
        data = await self.http.request(Route('POST', '/api/federation/show-instance'), json={'host': host}, auth=True,
                                       lower=True)
        return Instance(data, state=self)

    @get_cache_key
    async def fetch_instance(self, host: Optional[str] = None, **kwargs):
        old_cache = Cache(namespace='get_instance')
        await old_cache.delete(kwargs['cache_key'].format('get_instance'))
        return await self.get_instance(host=host)

    async def remove_emoji(self, emoji_id: str) -> bool:
        return bool(await self.http.request(Route('POST', '/api/admin/emoji/remove'), json={'id': emoji_id}, auth=True))

    async def show_file(self, file_id: Optional[str], url: Optional[str]) -> Drive:
        data = remove_dict_empty({"fileId": file_id, "url": url})
        return Drive(await self.http.request(Route('POST', '/api/admin/drive/show-file'), json=data, auth=True, lower=True), state=self)

    async def remove_file(self, file_id: str) -> bool:
        return bool(await self.http.request(Route('POST', '/api/drive/files/delete'), json={'fileId': file_id}, auth=True))
