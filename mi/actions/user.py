from __future__ import annotations

import asyncio
from typing import List, Optional, TYPE_CHECKING

from mi.api.chat import ChatManager
from mi.api.follow import FollowManager, FollowRequestManager
from mi.api.note import NoteManager
from mi.exception import NotExistRequiredData
from mi.http import HTTPClient, Route
from mi.models.note import RawNote
from mi.note import Note

if TYPE_CHECKING:
    from mi.state import ConnectionState
    from mi.user import User

__all__ = ['UserActions']


class UserActions:
    def __init__(
            self, state: ConnectionState,
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
        self.note: NoteManager(state, http, loop, user_id=user_id)
        self.follow: FollowManager = FollowManager(state, http, loop, user_id=user_id)
        self.follow_request: FollowRequestManager = FollowRequestManager(state, http, loop, user_id=user_id)
        self.chat: ChatManager = ChatManager(state, http, loop, user_id=user_id)

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
        res = await self.__http.request(Route('POST', '/api/users/notes'), json=data, auth=True, lower=True)
        return [Note(RawNote(i), state=self.__state) for i in res]

    def get_mention(self, user: Optional[User] = None) -> str:
        user = user or self.__user

        if user is None:
            raise NotExistRequiredData('Required parameters: user')
        return f'@{user.name}@{user.host}' if user.instance else f'@{user.name}'

    def get_follow(self, user_id: str) -> FollowManager:
        return FollowManager(self.__state, self.__http, self.__loop, user_id=user_id)

    def get_follow_request(self, user_id: str) -> FollowRequestManager:
        return FollowRequestManager(self.__state, self.__http, self.__loop, user_id=user_id)
