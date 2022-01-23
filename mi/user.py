from __future__ import annotations

from typing import Any, AsyncIterator, Dict, List, Optional, TYPE_CHECKING, Union

from mi.emoji import Emoji
from mi.instance import Instance
from mi.models.user import RawUser
from mi.types.user import (Channel as ChannelPayload, FieldContent as FieldContentPayload, PinnedNote as PinnedNotePayload,
                           PinnedPage as PinnedPagePayload)

if TYPE_CHECKING:
    from mi import ConnectionState
    from mi.api.follow import FollowRequestManager

__all__ = ['User', 'FollowRequest', 'Followee']


class Followee:
    def __init__(self, data, state: ConnectionState):
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.followee_id: str = data['followee_id']
        self.follower_id: str = data['follower_id']
        self.user: User = User(RawUser(data['follower']), state=state)
        self.__state = state


class FollowRequest:
    def __init__(self, data, state: ConnectionState):
        self.id = data['id']
        self.name = data['name']
        self.username = data['username']
        self.host = data['host']
        self.avatar_url = data['avatar_url']
        self.avatar_blurhash = data['avatar_blurhash']
        self.avatar_color = data['avatar_color']
        self.emojis = data['emojis']
        self.online_status = data['online_status']
        self.is_admin: bool = bool(data.get('is_admin'))
        self.is_bot: bool = bool(data.get('is_bot'))
        self.is_cat: bool = bool(data.get('is_cat'))
        self.__state: ConnectionState = state

    @property
    def action(self) -> FollowRequestManager:
        return self.__state.user.get_follow_request(self.id)

    async def get_profile(self) -> User:
        return await self.__state.get_user(user_id=self.id)


class Channel:
    def __init__(self, data: ChannelPayload):
        self.id: Optional[str] = data.get("id")
        self.created_at: Optional[str] = data.get("created_at")
        self.last_noted_at: Optional[str] = data.get("last_noted_at")
        self.name: Optional[str] = data.get("name")
        self.description: Optional[str] = data.get("description")
        self.banner_url: Optional[str] = data.get("banner_url")
        self.notes_count: Optional[int] = data.get("notes_count")
        self.users_count: Optional[int] = data.get("users_count")
        self.is_following: Optional[bool] = data.get("is_following")
        self.user_id: Optional[str] = data.get("user_id")


class PinnedNote:
    def __init__(self, data: PinnedNotePayload, state: ConnectionState):
        self.id: Optional[str] = data.get("id")
        self.created_at: Optional[str] = data.get("created_at")
        self.text: Optional[str] = data.get("text")
        self.cw: Optional[str] = data.get("cw")
        self.user_id: Optional[str] = data.get("user_id")
        self.user: Optional[User] = User(RawUser(data['user']), state=state) if data.get('user') else None
        self.reply_id: Optional[str] = data.get("reply_id")
        self.reply: Optional[Dict[str, Any]] = data.get("reply")
        self.renote: Optional[Dict[str, Any]] = data.get("renote")
        self.via_mobile: Optional[bool] = data.get("via_mobile")
        self.is_hidden: Optional[bool] = data.get("is_hidden")
        self.visibility: Optional[bool] = bool(data["visibility"]) if data.get("visibility") else None
        self.mentions: Optional[List[str]] = data.get("mentions")
        self.visible_user_ids: Optional[List[str]] = data.get("visible_user_ids")
        self.file_ids: Optional[List[str]] = data.get("file_ids")
        self.files: Optional[List[str]] = data.get("files")
        self.tags: Optional[List[str]] = data.get("tags")
        self.poll: Optional[List[str]] = data.get("poll")
        self.channel: Optional[Channel] = Channel(data["channel"]) if data.get("channel") else None
        self.local_only: Optional[bool] = data.get("local_only")
        self.emojis: Optional[List[Emoji]] = [Emoji(i, state=state) for i in data["emojis"]] if data.get("emojis") else None
        self.reactions: Optional[Dict[str, Any]] = data.get("reactions")
        self.renote_count: Optional[int] = data.get("renote_count")
        self.replies_count: Optional[int] = data.get("replies_count")
        self.uri: Optional[str] = data.get("uri")
        self.url: Optional[str] = data.get("url")
        self.my_reaction: Optional[Dict[str, Any]] = data.get("my_reaction")
        self.__state: ConnectionState = state


class PinnedPage:
    def __init__(self, data: PinnedPagePayload, state: ConnectionState):
        self.id: Optional[str] = data.get("id")
        self.created_at: Optional[str] = data.get("created_at")
        self.updated_at: Optional[str] = data.get("updated_at")
        self.title: Optional[str] = data.get("title")
        self.name: Optional[str] = data.get("name")
        self.summary: Optional[str] = data.get("summary")
        self.content: Optional[List] = data.get("content")
        self.variables: Optional[List] = data.get("variables")
        self.user_id: Optional[str] = data.get("user_id")
        self.author: Optional[Dict[str, Any]] = data.get("author")
        self.__state: ConnectionState = state


class FieldContent:
    def __init__(self, data: FieldContentPayload, state: ConnectionState):
        self.name: str = data["name"]
        self.value: str = data["value"]
        self.__state: ConnectionState = state


class User:
    def __init__(self, raw_user: RawUser, state: ConnectionState):
        self.__raw_user = raw_user
        self.__state = state

    @property
    def id(self):
        return self.__raw_user.id

    @property
    def name(self):
        return self.__raw_user.name

    @property
    def nickname(self):
        return self.__raw_user.nickname

    @property
    def host(self):
        return self.__raw_user.host

    @property
    def avatar_url(self):
        return self.__raw_user.avatar_url

    @property
    def is_admin(self):
        return self.__raw_user.is_admin

    @property
    def is_moderator(self):
        return self.__raw_user.is_moderator

    @property
    def is_bot(self):
        return self.__raw_user.is_bot

    @property
    def is_cat(self):
        return self.__raw_user.is_cat

    @property
    def is_lady(self):
        return self.__raw_user.is_lady

    @property
    def emojis(self):
        return self.__raw_user.emojis

    @property
    def online_status(self):
        return self.__raw_user.online_status

    @property
    def url(self):
        return self.__raw_user.url

    @property
    def uri(self):
        return self.__raw_user.uri

    @property
    def created_at(self):
        return self.__raw_user.created_at

    @property
    def updated_at(self):
        return self.__raw_user.updated_at

    @property
    def is_locked(self):
        return self.__raw_user.is_locked

    @property
    def is_silenced(self):
        return self.__raw_user.is_silenced

    @property
    def is_suspended(self):
        return self.__raw_user.is_suspended

    @property
    def description(self):
        return self.__raw_user.description

    @property
    def location(self):
        return self.__raw_user.location

    @property
    def birthday(self):
        return self.__raw_user.birthday

    @property
    def fields(self):
        return self.__raw_user.fields

    @property
    def followers_count(self):
        return self.__raw_user.followers_count

    @property
    def following_count(self):
        return self.__raw_user.following_count

    @property
    def notes_count(self):
        return self.__raw_user.notes_count

    @property
    def pinned_note_ids(self):
        return self.__raw_user.pinned_note_ids

    @property
    def pinned_notes(self):
        return self.__raw_user.pinned_notes

    @property
    def pinned_page_id(self):
        return self.__raw_user.pinned_page_id

    @property
    def pinned_page(self):
        return self.__raw_user.pinned_page

    @property
    def ff_visibility(self):
        return self.__raw_user.ff_visibility

    @property
    def is_following(self):
        return self.__raw_user.is_following

    @property
    def is_follow(self):
        return self.__raw_user.is_follow

    @property
    def is_blocking(self):
        return self.__raw_user.is_blocking

    @property
    def is_blocked(self):
        return self.__raw_user.is_blocked

    @property
    def is_muted(self):
        return self.__raw_user.is_muted

    @property
    def details(self):
        return self.__raw_user.details

    @property
    def instance(self) -> Union[Instance, None]:
        return Instance(self.__raw_user.instance, state=self.__state) if self.__raw_user.instance else None

    async def get_profile(self) -> "User":
        """
        ユーザーのプロフィールを取得します

        Returns
        -------
        User
            ユーザーのプロフィールオブジェクト
        """
        return await self.__state.get_user(user_id=self.__raw_user.id, username=self.__raw_user.name,
                                           host=self.__raw_user.host)

    def get_followers(self, until_id: Optional[str] = None, limit: int = 10, get_all: bool = False) -> AsyncIterator[Followee]:
        """
        ユーザーのフォロワー一覧を取得します

        Parameters
        ----------
        until_id : str, default=None
            前回のフォロワーの続きを取得する場合の起点とするユーザーid
        limit : int, default=10
            最大何人取得するか, max=100
        get_all : bool, default=False
            全てのフォロワーを取得するか否か

        Returns
        -------
        AsyncIterator[FollowRequest]
            ユーザーのフォロワー一覧
        """
        return self.__state.get_followers(username=self.__raw_user.name, host=self.__raw_user.host, until_id=until_id,
                                          limit=limit,
                                          get_all=get_all)

    @property
    def action(self):
        return self.__state.get_user_instance(self.__raw_user.id, self)
