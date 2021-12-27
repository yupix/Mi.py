from __future__ import annotations
from typing import Any, AsyncIterator, Dict, List, Optional, TYPE_CHECKING

from mi import Instance
from mi.emoji import Emoji
from mi.types.user import (User as UserPayload,
                           Channel as ChannelPayload,
                           PinnedNote as PinnedNotePayload,
                           PinnedPage as PinnedPagePayload,
                           FieldContent as FieldContentPayload)

if TYPE_CHECKING:
    from mi import ConnectionState

__all__ = ['User', 'UserDetails', 'Following']


class Follower:
    def __init__(self, data, state: ConnectionState):
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.followee_id: str = data['followee_id']
        self.follower_id: str = data['follower_id']
        self.user: User = User(data['follower'], state=state)
        self._state = state


class Following:
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
        self.is_admin = bool(data['is_admin'])
        self.is_bot = bool(data['is_bot'])
        self.is_cat = bool(data['is_cat'])
        self._state = state

    async def accept_request(self) -> bool:
        return await self._state.accept_following_request(self.id)

    async def reject_request(self) -> bool:
        return await self._state.reject_following_request(self.id)


class Channel:
    def __init__(self, data: ChannelPayload, state: ConnectionState):
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
        self._state = state


class PinnedNote:
    def __init__(self, data: PinnedNotePayload, state: ConnectionState):
        self.id: Optional[str] = data.get("id")
        self.created_at: Optional[str] = data.get("created_at")
        self.text: Optional[str] = data.get("text")
        self.cw: Optional[str] = data.get("cw")
        self.user_id: Optional[str] = data.get("user_id")
        self.user: Optional[User] = User(data["user"], state=state) if data.get('user') else None
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
        self.channel: Optional[Channel] = Channel(data["channel"], state=state) if data.get("channel") else None
        self.local_only: Optional[bool] = data.get("local_only")
        self.emojis: Optional[List[Emoji]] = [Emoji(i, state=state) for i in data["emojis"]] if data.get("emojis") else None
        self.reactions: Optional[Dict[str, Any]] = data.get("reactions")
        self.renote_count: Optional[int] = data.get("renote_count")
        self.replies_count: Optional[int] = data.get("replies_count")
        self.uri: Optional[str] = data.get("uri")
        self.url: Optional[str] = data.get("url")
        self.my_reaction: Optional[Dict[str, Any]] = data.get("my_reaction")
        self._state: ConnectionState = state


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
        self._state: ConnectionState = state


class FieldContent:
    def __init__(self, data: FieldContentPayload, state: ConnectionState):
        self.name: str = data["name"]
        self.value: str = data["value"]
        self._state: ConnectionState = state


class UserDetails:
    """
    ユーザー情報だが、一般的に使うか怪しいもの

    Attributes
    ----------
    avatar_blurhash: Optional[str]
        ユーザーのアバターのblurhash
    avatar_color: str
        ユーザーのアバターの色
    lang: str
        ユーザーの言語
    """

    def __init__(self, data) -> None:
        self.avatar_blurhash: Optional[str] = data.get("avatar_blurhash")
        self.avatar_color: Optional[str] = data.get("avatar_color")
        self.banner_url = data.get("banner_url")
        self.banner_blurhash = data.get("banner_blurhash")
        self.banner_color = data.get("banner_color")
        self.two_factor_enabled = data.get("two_factor_enabled", False)
        self.use_password_less_login = data.get("use_password_less_login", False)
        self.security_keys = data.get("security_keys", False)
        self.has_pending_follow_request_from_you = data.get("has_pending_follow_request_from_you", False)
        self.has_pending_follow_request_to_you = data.get("has_pending_follow_request_to_you", False)
        self.public_reactions = data.get("public_reactions", False)
        self.lang = data.get("lang")


class User:
    """
    Attributes
    ----------
    id: str
        ユーザーのid
    name: str
        ユーザーのニックネーム
    username: str
        ユーザーのアカウント名
    host: Optional[str]
        ユーザーのホスト名
    avatar_url: Optional[str]
        ユーザーのアバターのURL
    admin: bool
        ユーザーが管理者かどうか
    bot: bool
        ユーザーがbotかどうか
    emojis: list
        ユーザーが使用しているemoji
    online_status: Any
        ユーザーのオンライン状況
    url: str
        ユーザーのプロフィールへのURL
    uri: str
        謎
    created_at: str
        アカウントの作成日
    updated_at: str
        アカウントの更新日(ノートを投稿するなど)
    is_locked: bool
        アカウントがロックされているか
    is_silenced: bool
        アカウントがミュートされているか
    is_suspended: bool
        アカウントが凍結されているか
    description: str
        アカウントの概要
    location: str
        ユーザーが住んでいる場所
    birthday: str
        ユーザーの誕生日
    fields: list
        プロフィールのリンクフィールド
    followers_count: int
        フォロワーの数
    following_count: int
        フォローしている人の数
    notes_count: int
        投稿したノートの数
    pinned_note_ids: list
        ピン留めされたノートのidリスト
    pinned_page_id:str
        ピン留めされたページのid
    pinned_page: str
        ピン留めされたページ
    ff_visibility: str
        ノートの投稿範囲
    is_following: bool
        ユーザーがフォローしているかどうか
    is_follow: bool
        ユーザーのことをフォローしているかどうか
    is_blocking: bool
        ユーザーが自分のことをブロックしているかどうか
    is_blocked: bool
        ユーザーのことをブロックしているかどうか
    is_muted: bool
        ユーザーのことをミュートしているかどうか
    instance: Any
        ユーザーのインスタンス
    details: UserDetails
        ユーザーの詳細な情報
    """

    def __init__(self, data: UserPayload, state: ConnectionState):
        self.id: str = data["id"]
        self.name: Optional[str] = data.get("name")
        self.username: str = data["username"]
        self.host: Optional[str] = data.get("host")
        self.avatar_url: Optional[str] = data.get("avatar_url")
        self.admin: bool = bool(data.get("is_admin"))
        self.moderator: bool = bool(data.get("is_moderator"))
        self.bot: bool = bool(data.get("is_bot"))
        self.cat: bool = bool(data.get("is_cat", False))
        self.lady: bool = bool(data.get('is_lady', False))
        self.emojis: Optional[List[str]] = data.get("emojis")
        self.online_status = data.get("online_status", None)
        self.url: Optional[str] = data.get("url")
        self.uri: Optional[str] = data.get("uri")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")
        self.is_locked = data.get("is_locked", False)
        self.is_silenced = data.get("is_silenced", False)
        self.is_suspended = data.get("is_suspended", False)
        self.description = data.get("description")
        self.location = data.get("location")
        self.birthday = data.get("birthday")
        self.fields = data.get("fields", [])
        self.followers_count = data.get("followers_count", 0)
        self.following_count = data.get("following_count", 0)
        self.notes_count = data.get("notes_count", 0)
        self.pinned_note_ids = data.get("pinned_note_ids", [])
        self.pinned_notes = data.get("pinned_notes", [])
        self.pinned_page_id = data.get("pinned_page_id")
        self.pinned_page = data.get("pinned_page")
        self.ff_visibility: str = data.get("ff_visibility", 'public')
        self.is_following: bool = bool(data.get("is_following", False))
        self.is_follow: bool = bool(data.get("is_follow", False))
        self.is_blocking: bool = bool(data.get("is_blocking", False))
        self.is_blocked: bool = bool(data.get("is_blocked", False))
        self.is_muted: bool = bool(data.get("is_muted", False))
        self.details = UserDetails(data)
        self._state = state

        self.instance = (
            Instance(data["instance"], state) if data.get("instance") else Instance({}, state)
        )

    async def follow(self) -> tuple[bool, Optional[str]]:
        """
        ユーザーをフォローします

        Returns
        -------
        bool = False
            成功ならTrue, 失敗ならFalse
        str
            実行に失敗した際のエラーコード
        """

        return await self._state.follow_user(user_id=self.id)

    async def unfollow(self) -> bool:
        """
        ユーザーのフォローを解除します

        Returns
        -------
        status: bool = False
            成功ならTrue, 失敗ならFalse
        """

        return await self._state.unfollow_user(user_id=self.id)

    async def get_profile(self) -> "User":
        """
        ユーザーのプロフィールを取得します

        Returns
        -------
        User:
            ユーザーのプロフィールオブジェクト
        """
        return await self._state.get_user(user_id=self.id, username=self.username, host=self.host)

    def get_followers(self, until_id: Optional[str] = None, limit: int = 10, get_all: bool = False) -> AsyncIterator[Follower]:
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
        AsyncIterator[Follower]:
            ユーザーのフォロワー一覧
        """
        return self._state.get_followers(username=self.username, host=self.host, until_id=until_id, limit=limit,
                                         get_all=get_all)
