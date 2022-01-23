from __future__ import annotations

import asyncio
from typing import List, Optional, TYPE_CHECKING

from mi.exception import NotExistRequiredData
from mi.http import HTTPClient, Route

if TYPE_CHECKING:
    from mi.state import ConnectionState


class EmojiManager:
    def __init__(
            self, client: ConnectionState,
            http: HTTPClient,
            loop: asyncio.AbstractEventLoop,
            *,
            emoji_id: Optional[str] = None
    ):
        self.__client: 'ConnectionState' = client
        self.__http: HTTPClient = http
        self.__loop: asyncio.AbstractEventLoop = loop
        self.emoji_id: Optional[str] = emoji_id

    async def add(self, name: str, url: str, category: Optional[str] = None, aliases: Optional[List[str]] = None):
        data = {'name': name, 'url': url, 'category': category, 'aliases': aliases}

        return bool(await self.__http.request(Route('POST', '/api/admin/emoji/add'), json=data, lower=True, auth=True))

    async def remove(self, emoji_id: Optional[str] = None) -> bool:
        emoji_id = emoji_id or self.emoji_id

        if emoji_id is None:
            raise NotExistRequiredData('idが不足しています')

        return bool(await self.__http.request(Route('POST', '/api/admin/emoji/remove'), json={'id': emoji_id}, lower=True,
                                              auth=True))
