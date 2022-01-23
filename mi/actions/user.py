from __future__ import annotations

import asyncio
from typing import Optional, TYPE_CHECKING

from mi.api.chat import ChatManager
from mi.api.follow import FollowManager, FollowRequestManager
from mi.exception import NotExistRequiredData

if TYPE_CHECKING:
    from mi.state import ConnectionState
    from mi.http import HTTPClient
    from mi.user import User

__all__ = ['UserActions']


class UserActions:
    def __init__(
            self, state: 'ConnectionState',
            http: HTTPClient,
            loop: asyncio.AbstractEventLoop,
            *,
            user_id: Optional[str] = None,
            user: Optional[User] = None
    ):
        self.__state = state
        self.__http = http
        self.__loop = loop
        self.__user: User = user
        self.follow: FollowManager = FollowManager(state, http, loop, user_id=user_id)
        self.follow_request: FollowRequestManager = FollowRequestManager(state, http, loop, user_id=user_id)
        self.chat: ChatManager = ChatManager(state, http, loop, user_id=user_id)

    def get_mention(self, user: Optional[User] = None) -> str:
        user = user or self.__user

        if user is None:
            raise NotExistRequiredData('Required parameters: user')
        return f'@{user.name}@{user.host}' if user.instance else f'@{user.name}'

    def get_follow(self, user_id: str) -> FollowManager:
        return FollowManager(self.__state, self.__http, self.__loop, user_id=user_id)

    def get_follow_request(self, user_id: str) -> FollowRequestManager:
        return FollowRequestManager(self.__state, self.__http, self.__loop, user_id=user_id)
