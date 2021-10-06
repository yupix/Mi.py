import json
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from mi import Emoji, Instance, conn
from mi.drive import File
from mi.utils import api, upper_to_lower


class UserAction(object):
    @staticmethod
    def get_i():
        res = api('/api/i', auth=True)
        return UserProfile(**upper_to_lower(json.loads(res.text)))

    @staticmethod
    def follow(user_id: Optional[str]) -> tuple[bool, str]:
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
        data = {'userId': user_id}
        res = api('/api/following/create', json_data=data, auth=True)
        if res.json().get('error'):
            code = res.json()['error']['code']
            status = False
        else:
            code = None
            status = True
        return status, code

    @staticmethod
    def unfollow(user_id: str) -> bool:
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
        data = {'userId': user_id}
        res = api('/api/following/delete', json_data=data, auth=True)
        return bool(res.status_code == 204 or 200)


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
    emojis: Optional[List[Emoji]]
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


class UserProfile(BaseModel):
    id: Optional[str] = None
    username: Optional[str] = None
    name: Optional[str] = None
    url: Optional[str] = None
    avatar_url: Optional[str] = None
    avatar_blurhash: Optional[str] = None
    banner_url: Optional[str] = None
    banner_blurhash: Optional[str] = None
    emojis: Optional[List[Emoji]] = None
    host: Optional[str] = None
    description: Optional[str] = None
    birthday: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    location: Optional[str] = None
    followers_count: Optional[int] = 0
    following_count: Optional[int] = 0
    notes_count: Optional[int] = 0
    is_bot: Optional[bool] = False
    pinned_note_ids: Optional[List[str]] = []
    pinned_notes: Optional[List[PinnedNote]] = None
    is_cat: Optional[bool] = False
    is_lady: Optional[bool] = False
    is_admin: Optional[bool] = False
    is_moderator: Optional[bool] = False
    is_verified: Optional[bool] = False
    is_locked: Optional[bool] = False
    has_unread_specified_notes: Optional[bool] = False
    has_unread_mentions: Optional[bool] = False
    avatar_color: Optional[str] = None
    banner_color: Optional[str] = None
    is_suspended: Optional[bool] = False
    fields: Optional[List[FieldContent]] = None
    pinned_page_id: Optional[str] = None
    pinned_page: Optional[PinnedPage] = None
    two_factor_enabled: Optional[bool] = False
    use_password_less_login: Optional[bool] = False
    security_keys: Optional[bool] = False
    avatar_id: Optional[str] = None
    banner_id: Optional[str] = None
    auto_watch: Optional[bool] = False
    inject_featured_note: Optional[bool] = False
    always_mark_nsfw: Optional[bool] = False
    careful_bot: Optional[bool] = False
    auto_accept_followed: Optional[bool] = False
    has_unread_announcement: Optional[bool] = False
    has_unread_antenna: Optional[bool] = False
    has_unread_channel: Optional[bool] = False
    has_unread_messaging_message: Optional[bool] = False
    has_unread_notification: Optional[bool] = False
    has_pending_received_follow_request: Optional[bool] = False
    integrations: Optional[Dict[str, Any]] = {}
    muted_words: Optional[List] = None
    muting_notification_types: Optional[List] = None
    is_following: Optional[bool] = False
    has_pending_follow_request_from_you: Optional[bool] = False
    has_pending_follow_request_to_you: Optional[bool] = False
    is_followed: Optional[bool] = False
    is_blocking: Optional[bool] = False
    is_blocked: Optional[bool] = False
    is_muted: Optional[bool] = False
    __user_action: UserAction = UserAction()

    class Config:
        arbitrary_types_allowed = True

    def follow(self, user_id: Optional[str] = None) -> bool:
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

        if user_id is None:
            user_id = self.id
        return self.__user_action.follow(user_id)

    def unfollow(self, user_id: Optional[str] = None) -> bool:
        """
        与えられたIDのユーザーのフォローを解除します

        Parameters
        ----------
        user_id : Optional[str] = None
            フォローを解除したいユーザーのID

        Returns
        -------
        status: bool = False
            成功ならTrue, 失敗ならFalse
        """
        if user_id is None:
            user_id = self.id
        return self.__user_action.unfollow(user_id)


class Author(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None
    host: Optional[str] = None
    avatar_url: Optional[str] = None
    avatar_blurhash: Optional[str] = None
    avatar_color: Optional[str] = None
    is_admin: Optional[bool] = False
    is_bot: Optional[bool] = False
    is_cat: Optional[bool] = False
    is_lady: Optional[bool] = False
    emojis: Optional[List] = None
    online_status: Optional[str] = None
    instance: Optional[Instance] = Instance()
    __user_action: UserAction = UserAction()

    class Config:
        arbitrary_types_allowed = True

    def follow(self, user_id: Optional[str] = None) -> bool:
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

        if user_id is None:
            user_id = self.id
        return self.__user_action.follow(user_id)

    def unfollow(self, user_id: Optional[str] = None) -> bool:
        """
        与えられたIDのユーザーのフォローを解除します

        Parameters
        ----------
        user_id : Optional[str] = None
            フォローを解除したいユーザーのID

        Returns
        -------
        status: bool = False
            成功ならTrue, 失敗ならFalse
        """
        if user_id is None:
            user_id = self.id
        return self.__user_action.unfollow(user_id)

    def get_profile(self) -> 'UserProfile':
        """
        ユーザーのプロフィールを取得します

        Returns
        -------
        UserProfile:
            ユーザーのプロフィールオブジェクト
        """
        return UserProfile(**upper_to_lower(conn.get_user(user_id=self.id, username=self.username, host=self.host)))

    def get_followers(self, until_id: str = None, limit: int = 10, get_all: bool = False):
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
        return conn.get_followers(
            user_id=self.id,
            username=self.username,
            host=self.host,
            limit=limit,
            until_id=until_id,
            get_all=get_all
        )
