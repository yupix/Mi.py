from __future__ import annotations

import asyncio
from typing import List, Optional, TYPE_CHECKING

from mi import Emoji
from mi.http import HTTPClient, Route
from mi.models.emoji import RawEmoji
from mi.models.reaction import RawNoteReaction
from mi.note import NoteReaction
from mi.utils import remove_dict_empty

if TYPE_CHECKING:
    from mi.state import ConnectionState


class ReactionManager:
    def __init__(self, client: ConnectionState, http: HTTPClient, loop: asyncio.AbstractEventLoop, *,
                 note_id: Optional[str] = None):
        self.client = client
        self.http = http
        self.loop = loop
        self.__note_id = note_id

    async def add(self, reaction: str, note_id: Optional[str] = None) -> bool:
        """
        指定したnoteに指定したリアクションを付与します（内部用

        Parameters
        ----------
        reaction : Optional[str]
            付与するリアクション名
        note_id : Optional[str]
            付与対象のノートID

        Returns
        -------
        bool
            成功したならTrue,失敗ならFalse
        """
        note_id = note_id or self.__note_id

        data = remove_dict_empty({"noteId": note_id, "reaction": reaction})
        return await self.http.request(Route('POST', '/api/notes/reactions/create'), json=data, auth=True, lower=True)

    async def remove(self, note_id: Optional[str] = None) -> bool:
        note_id = note_id or self.__note_id

        data = remove_dict_empty({"noteId": note_id})
        return bool(await self.http.request(Route('POST', '/api/notes/reactions/delete'), json=data, auth=True, lower=True))

    async def get_reaction(self, reaction: str, note_id: Optional[str] = None, *, limit: int = 11) -> List[NoteReaction]:
        note_id = note_id or self.__note_id
        data = remove_dict_empty({"noteId": note_id, 'limit': limit, 'type': reaction})
        res = await self.http.request(Route('POST', '/api/notes/reactions'), json=data, auth=True, lower=True)
        return [NoteReaction(RawNoteReaction(i), state=self.client) for i in res]

    async def get_emoji_list(self) -> List[Emoji]:
        data = await self.http.request(Route('GET', '/api/meta'), json={'detail': False}, auth=True)
        return [Emoji(RawEmoji(i), state=self.client) for i in data['emojis']]
