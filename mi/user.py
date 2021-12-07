from __future__ import annotations
from typing import Any, Dict, Iterator, List, Optional, TYPE_CHECKING

from pydantic import BaseModel

from mi import Instance
from mi.drive import File
from mi.exception import InvalidParameters, NotExistRequiredParameters
from mi.types.user import (Author as UserPayload)
from mi.utils import api, check_multi_arg, remove_dict_empty, upper_to_lower

if TYPE_CHECKING:
    from mi import ConnectionState

__all__ = ['User', 'UserDetails']


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
    id_: Optional[str] = None
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
        self.name: str = data["name"]
        self.username: str = data["username"]
        self.host: Optional[str] = data.get("host")
        self.avatar_url: Optional[str] = data.get("avatar_url")
        self.admin: bool = data.get("is_admin", False)
        self.moderator: bool = data.get("is_moderator", False)
        self.bot: bool = data.get("is_bot", False)
        self.cat: bool = data.get("is_cat", False)
        self.lady: bool = data.get('is_lady', False)
        self.emojis: List[str] = data.get("emojis")
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
        self.ff_visibility = data.get("ff_visibility", 'public')
        self.following = data.get("is_following", False)
        self.followed = data.get("is_follow", False)
        self.blocking = data.get("is_blocking", False)
        self.blocked = data.get("is_blocked", False)
        self.muted = data.get("is_muted", False)
        self.details = UserDetails(data)
        self._state = state

        self.instance = (
            Instance(data["instance"], state) if data.get("instance") else Instance({}, state)
        )

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def _get_followers(
            user_id: Optional[str] = None,
            username: Optional[str] = None,
            host: Optional[str] = None,
            since_id: Optional[str] = None,
            until_id: Optional[str] = None,
            limit: int = 10,
            get_all: bool = False,
    ) -> Iterator[Dict[str, Any]]:
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
            謎
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
                get_data = api("/api/users/followers", json_data=data,
                               auth=True).json()
                if len(get_data) > 0:
                    data["untilId"] = get_data[-1]["id"]
                else:
                    break
                yield get_data
        else:
            get_data = api("/api/users/followers", json_data=data,
                           auth=True).json()
            yield get_data

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

        return self._state.follow_user(self.id)

    async def unfollow(self) -> bool:
        """
        ユーザーのフォローを解除します

        Returns
        -------
        status: bool = False
            成功ならTrue, 失敗ならFalse
        """

        return self._state.unfollow_user(self.id)

    async def get_profile(self) -> "User":
        """
        ユーザーのプロフィールを取得します

        Returns
        -------
        User:
            ユーザーのプロフィールオブジェクト
        """
        return User(
            **upper_to_lower(
                self._state._get_user(user_id=self.id, username=self.username,
                                     host=self.host)
            )
        )

    async def get_followers(self, until_id: Optional[str] = None, limit: int = 10, get_all: bool = False) -> Iterator[
        Dict[str, Any]]:
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

        """
        return self._state._get_followers(
            user_id=self.id,
            username=self.username,
            host=self.host,
            limit=limit,
            until_id=until_id,
            get_all=get_all,
        )
