from __future__ import annotations
from typing import List, TYPE_CHECKING

from mi.types.emoji import Emoji as EmojiPayload

if TYPE_CHECKING:
    from mi import ConnectionState


class Emoji:
    def __init__(self, data: EmojiPayload, state: ConnectionState):
        self.id: str = data.get('id')
        self.aliases: List[str] = data.get('aliases')
        self.name: str = data.get('name')
        self.category: str = data.get('category')
        self.host: str = data.get('host')
        self.url: str = data.get('url')
        self._state: ConnectionState = state

    async def remove(self) -> bool:
        return await self._state.remove_emoji(self.id)
