from __future__ import annotations

import asyncio
from typing import Optional, TYPE_CHECKING

from mi.chat import Chat
from mi.http import HTTPClient, Route
from mi.models.chat import RawChat

if TYPE_CHECKING:
    from mi.client import ConnectionState


class ChatManager:
    def __init__(self, __state: 'ConnectionState', http: HTTPClient, loop: asyncio.AbstractEventLoop,
                 user_id: Optional[str] = None):
        self.__client = __state
        self.__http = http
        self.__loop = loop
        self.__user_id = user_id

    async def send(
            self,
            text: Optional[str] = None,
            *,
            file_id: Optional[str] = None,
            user_id: Optional[str] = None,
            group_id: Optional[str] = None
    ) -> Chat:
        user_id = user_id or self.__user_id
        data = {'userId': user_id, 'groupId': group_id, 'text': text, 'fileId': file_id}
        res = await self.__http.request(Route('POST', '/api/messaging/messages/create'), json=data, auth=True, lower=True)
        return Chat(RawChat(res), state=self.__client)
