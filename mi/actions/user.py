from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from aiocache import Cache, cached
from mi.exception import NotExistRequiredData, NotExistRequiredParameters
from mi.framework.http import HTTPSession
from mi.framework.models.note import Note
from mi.framework.router import Route
from mi.utils import check_multi_arg, get_cache_key, key_builder, remove_dict_empty
from mi.wrapper.chat import ChatManager
from mi.wrapper.follow import FollowManager, FollowRequestManager
from mi.wrapper.models.note import RawNote
from mi.wrapper.models.user import RawUser
from mi.wrapper.note import NoteManager
from mi.wrapper.user import AdminUserManager

if TYPE_CHECKING:
    from mi.framework.models.user import User

__all__ = ['UserActions']


class UserActions:
    def __init__(
            self,
            user_id: Optional[str] = None,
            user: Optional[User] = None
    ):
        self.__user: User = user
        self.admin = AdminUserManager(user_id=user_id)
        self.note: NoteManager()
        self.follow: FollowManager = FollowManager(user_id=user_id)
        self.follow_request: FollowRequestManager = FollowRequestManager(user_id=user_id)
        self.chat: ChatManager = ChatManager(user_id=user_id)

    def _get_chat_instance(self, message_id: Optional[str] = None, user_id: Optional[str] = None) -> ChatManager:
        return ChatManager(user_id=self.__user.id, message_id=message_id)

    @cached(ttl=10, namespace='get_user', key_builder=key_builder)
    async def get(self, user_id: Optional[str] = None, username: Optional[str] = None, host: Optional[str] = None) -> User:
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
        User
            ユーザー情報
        """

        field = remove_dict_empty({"userId": user_id, "username": username, "host": host})
        data = await HTTPSession.request(Route('POST', '/api/users/show'), json=field, auth=True, lower=True)
        return User(RawUser(data))

    @get_cache_key
    async def fetch(self, user_id: Optional[str] = None, username: Optional[str] = None,
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
        User
            ユーザー情報
        """
        if not check_multi_arg(user_id, username):
            raise NotExistRequiredParameters("user_id, usernameどちらかは必須です")

        field = remove_dict_empty({"userId": user_id, "username": username, "host": host})
        data = await HTTPSession.request(Route('POST', '/api/users/show'), json=field, auth=True, lower=True)
        old_cache = Cache(namespace='get_user')
        await old_cache.delete(kwargs['cache_key'].format('get_user'))
        return User(RawUser(data))

    async def get_notes(
            self,
            user_id: Optional[str] = None,
            include_replies: bool = True,
            limit: int = 10,
            since_id: Optional[str] = None,
            until_id: Optional[str] = None,
            since_date: int = 0,
            until_date: int = 0,
            include_my_renotes: bool = True,
            with_files: bool = False,
            file_type: Optional[List[str]] = None,
            exclude_nsfw: bool = True
    ) -> List[Note]:
        user_id = user_id or self.__user.id
        data = {
            'userId': user_id,
            'includeReplies': include_replies,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
            'sinceDate': since_date,
            'untilDate': until_date,
            'includeMyRenotes': include_my_renotes,
            'withFiles': with_files,
            'fileType': file_type,
            'excludeNsfw': exclude_nsfw
        }
        res = await HTTPSession.request(Route('POST', '/api/users/notes'), json=data, auth=True, lower=True)
        return [Note(RawNote(i)) for i in res]

    def get_mention(self, user: Optional[User] = None) -> str:
        """
        Get mention name of user.
        
        Parameters
        ----------
        user : Optional[User], default=None
            メンションを取得したいユーザーのオブジェクト
        
        Returns
        -------
        str
            メンション
        """

        user = user or self.__user

        if user is None:
            raise NotExistRequiredData('Required parameters: user')
        return f'@{user.name}@{user.host}' if user.instance else f'@{user.name}'

    def get_follow(self, user_id: str) -> FollowManager:
        return FollowManager(user_id=user_id)

    def get_follow_request(self, user_id: str) -> FollowRequestManager:
        return FollowRequestManager(user_id=user_id)
