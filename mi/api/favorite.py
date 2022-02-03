from __future__ import annotations

import asyncio
from typing import Optional, TYPE_CHECKING

from mi.http import HTTPClient, Route

if TYPE_CHECKING:
    from mi.client import ConnectionState


class FavoriteManager:
    def __init__(self, client: ConnectionState, http: HTTPClient, loop: asyncio.AbstractEventLoop,
                 note_id: Optional[str] = None):
        self.__state: ConnectionState = client
        self.__http: HTTPClient = http
        self.__loop: asyncio.AbstractEventLoop = loop
        self.__note_id = note_id

    async def add(self, note_id: Optional[str] = None) -> bool:
        note_id = note_id or self.__note_id
        data = {'noteId': note_id}
        return bool(await self.__http.request(Route('POST', '/api/notes/favorites/create'), json=data, auth=True))

    async def remove(self, note_id: Optional[str] = None) -> bool:
        note_id = note_id or self.__note_id
        data = {'noteId': note_id}
        return bool(await self.__http.request(Route('POST', '/api/notes/favorites/delete'), json=data, auth=True))
