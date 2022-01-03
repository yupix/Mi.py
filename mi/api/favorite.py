from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING

from mi.http import HTTPClient, Route

if TYPE_CHECKING:
    from mi.client import ConnectionState


class FavoriteManager:
    def __init__(self, client: 'ConnectionState', http: HTTPClient, loop: asyncio.AbstractEventLoop):
        self.client: 'ConnectionState' = client
        self.http: HTTPClient = http
        self.loop: asyncio.AbstractEventLoop = loop

    async def add(self, note_id: str) -> bool:
        data = {'noteId': note_id}
        return bool(await self.http.request(Route('POST', '/api/notes/favorites/create'), json=data, auth=True))

    async def remove(self, note_id: str) -> bool:
        data = {'noteId': note_id}
        return bool(await self.http.request(Route('POST', '/api/notes/favorites/delete'), json=data, auth=True))
