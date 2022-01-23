from __future__ import annotations

from typing import TYPE_CHECKING

from mi.models.emoji import RawEmoji

if TYPE_CHECKING:
    from mi import ConnectionState

__all__ = ('Emoji',)


class Emoji:
    def __init__(self, raw_data: RawEmoji, state: ConnectionState):
        self.__raw_data = raw_data
        self.__state: ConnectionState = state

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

    @property
    def action(self):
        return self.__state.emoji
