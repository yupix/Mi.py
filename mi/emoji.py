from __future__ import annotations

from typing import TYPE_CHECKING

from mi.exception import NotExistRequiredData
from mi.models.emoji import RawEmoji

if TYPE_CHECKING:
    from mi import ConnectionState

__all__ = ('Emoji',)


class Emoji:
    def __init__(self, raw_data: RawEmoji, state: ConnectionState):
        self.__raw_data = raw_data
        self._state: ConnectionState = state

    @property
    def id(self):
        return self.__raw_data.id

    @property
    def aliases(self):
        return self.__raw_data.aliases

    @property
    def name(self):
        return self.__raw_data.name

    @property
    def category(self):
        return self.__raw_data.category

    @property
    def host(self):
        return self.__raw_data.host

    @property
    def url(self):
        return self.__raw_data.url

    async def remove(self) -> bool:
        if not self.id:
            raise NotExistRequiredData('idが不足しています')
        return await self._state.remove_emoji(self.id)
