from __future__ import annotations
from typing import Any, AsyncIterator, Dict, List, Optional, TYPE_CHECKING

from pydantic import BaseModel

from mi import Instance
from mi.drive import File
from mi.types.user import (User as UserPayload)

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
    def __init__(self, data, state:ConnectionState):
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
    

class Channel(BaseModel):
    id: Optional[str] = None
    createdAt: Optional[str] = None
    lastNotedAt: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    bannerUrl: Optional[str] = None
    notesCount: Optional[int] = 0
    usersCount: Optional[int] = 0
    isFollowing: Optional[bool] = False
    userId: Optional[str] = None


class PinnedNote(BaseModel):
    id: Optional[str] = None
    createdAt: Optional[str] = None
    text: Optional[str] = None
    cw: Optional[str] = None
    userId: Optional[str] = None
    user: Optional[Dict[str, Any]] = {}
    replyId: Optional[str] = None
    renoteId: Optional[str] = None
    reply: Optional[Dict[str, Any]] = {}
    renote: Optional[Dict[str, Any]] = {}
    viaMobile: Optional[bool] = False
    isHidden: Optional[bool] = False
    visibility: Optional[str] = None
    mentions: Optional[List[str]] = []
    visibleUserIds: Optional[List[str]] = []
    fileIds: Optional[List[str]] = []
    files: Optional[List[File]] = []
    tags: Optional[List[str]] = []
    poll: Optional[Dict[str, Any]] = {}
    channelId: Optional[str] = None
    channel: Optional[Channel] = Channel()
    localOnly: Optional[bool] = False
    # emojis: Optional[List[Emoji]] # TODO: 2021 修正
    reactions: Optional[Dict[str, Any]] = {}
    renoteCount: Optional[int] = 0
    repliesCount: Optional[int] = 0
    uri: Optional[str] = None
    url: Optional[str] = None
    myReaction: Optional[Dict[str, Any]] = {}


class PinnedPage(BaseModel):
    id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    title: Optional[str] = None
    name: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[List] = []
    variables: Optional[List] = []
    user_id: Optional[str] = None
    author: Optional[Dict[str, Any]] = {}


class FieldContent(BaseModel):
    name: str
    value: str


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
    locked: bool
        アカウントがロックされているか
    silienced: bool
        アカウントがミュートされているか
    suspended: bool
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
    following: bool
        ユーザーがフォローしているかどうか
    followed: bool
        ユーザーのことをフォローしているかどうか
    blocking: bool
        ユーザーが自分のことをブロックしているかどうか
    blocked: bool
        ユーザーのことをブロックしているかどうか
    muted:bool
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
        self.locked = data.get("is_locked", False)
        self.silenced = data.get("is_silenced", False)
        self.suspended = data.get("is_suspended", False)
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
        self.following: bool = bool(data.get("is_following", False))
        self.followed: bool = bool(data.get("is_follow", False))
        self.blocking: bool = bool(data.get("is_blocking", False))
        self.blocked: bool = bool(data.get("is_blocked", False))
        self.muted: bool = bool(data.get("is_muted", False))
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
