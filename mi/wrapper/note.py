from __future__ import annotations

from typing import Optional

from mi.framework.http import HTTPSession


class NoteManager:
    """User behavior for notes"""

    def __init__(self, note_id: Optional[str] = None):
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
        await HTTPSession.request(Route('POST', '/api/notes'), json=data, auth=True, lower=True)
