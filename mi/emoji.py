from __future__ import annotations
from typing import List, TYPE_CHECKING, Optional
from mi.exception import NotExistRequiredData

from mi.types.emoji import Emoji as EmojiPayload

if TYPE_CHECKING:
    from mi import ConnectionState

__all__ = ('Emoji',)


class Emoji:
    def __init__(self, data: EmojiPayload, state: ConnectionState):
        self.id: Optional[str] = data.get('id')
        self.aliases: Optional[List[str]] = data.get('aliases')
        self.name: Optional[str] = data.get('name')
        self.category: Optional[str] = data.get('category')
        self.host: Optional[str] = data.get('host')
        self.url: Optional[str] = data.get('url')
        self._state: ConnectionState = state

    async def remove(self) -> bool:
        if not self.id:
            raise NotExistRequiredData('idが不足しています')
        return await self._state.remove_emoji(self.id)
