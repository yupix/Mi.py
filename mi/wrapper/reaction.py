from __future__ import annotations

from typing import List, Optional

from mi.framework.http import HTTPSession
from mi.framework.models.emoji import Emoji
from mi.framework.models.note import NoteReaction
from mi.framework.router import Route
from mi.utils import remove_dict_empty
from mi.wrapper.models.emoji import RawEmoji
from mi.wrapper.models.reaction import RawNoteReaction


class ReactionManager:
    def __init__(self, note_id: Optional[str] = None):
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
        return await HTTPSession.request(Route('POST', '/api/notes/reactions/create'), json=data, auth=True,
                                         lower=True)

    async def remove(self, note_id: Optional[str] = None) -> bool:
        note_id = note_id or self.__note_id

        data = remove_dict_empty({"noteId": note_id})
        return bool(await HTTPSession.request(Route('POST', '/api/notes/reactions/delete'), json=data, auth=True,
                                              lower=True))

    async def get_reaction(self, reaction: str, note_id: Optional[str] = None, *, limit: int = 11) -> List[NoteReaction]:
        note_id = note_id or self.__note_id
        data = remove_dict_empty({"noteId": note_id, 'limit': limit, 'type': reaction})
        res = await HTTPSession.request(Route('POST', '/api/notes/reactions'), json=data, auth=True, lower=True)
        return [NoteReaction(RawNoteReaction(i)) for i in res]

    async def get_emoji_list(self) -> List[Emoji]:
        data = await HTTPSession.request(Route('GET', '/api/meta'), json={'detail': False}, auth=True)
        return [Emoji(RawEmoji(i)) for i in data['emojis']]
