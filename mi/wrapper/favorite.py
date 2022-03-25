from __future__ import annotations

from typing import Optional

from mi.framework.http import HTTPSession
from mi.framework.router import Route


class FavoriteManager:
    def __init__(self, note_id: Optional[str] = None):
        self.__note_id = note_id

    async def add(self, note_id: Optional[str] = None) -> bool:
        note_id = note_id or self.__note_id
        data = {'noteId': note_id}
        return bool(await HTTPSession.request(Route('POST', '/api/notes/favorites/create'), json=data, auth=True))

    async def remove(self, note_id: Optional[str] = None) -> bool:
        note_id = note_id or self.__note_id
        data = {'noteId': note_id}
        return bool(await HTTPSession.request(Route('POST', '/api/notes/favorites/delete'), json=data, auth=True))
