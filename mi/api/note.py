from __future__ import annotations

import asyncio
from typing import Optional, TYPE_CHECKING

from mi.http import HTTPClient, Route

if TYPE_CHECKING:
    from mi.state import ConnectionState


class NoteManager:
    def __init__(self, state: ConnectionState, http: HTTPClient, loop: asyncio.AbstractEventLoop, *, note_id: Optional[str]
    = None):
        self.__state = state
        self.__http = http
        self.__loop = loop
        self.__note_id = note_id

    async def get(self, local: bool = True, reply: bool = False, renote: bool = True, with_files: bool = False,
                  poll: bool = True, limit: int = 10, since_id: Optional[str] = None, until_id: Optional[str] = None):
        data = {
            'local': local,
            'reply': reply,
            'renote': renote,
            'withFiles': with_files,
            'poll': poll,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id
        }
        await self.__http.request(Route('POST', '/api/notes'), json=data, auth=True, lower=True)
