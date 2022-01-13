from __future__ import annotations

from typing import TYPE_CHECKING

from mi.models.drive import RawFile, RawFolder
from mi.models.user import RawUser
from mi.user import User

if TYPE_CHECKING:
    from .state import ConnectionState


class Properties:
    def __init__(self, data):
        self.width: int = data['width']
        self.height: int = data['height']
        self.avg_color: float = data['avg_color']


class Folder:
    def __init__(self, raw_data: RawFolder, state: ConnectionState):
        self.__raw_data = raw_data
        self.__state = state

    @property
    def id(self):
        return self.__raw_data.id

    @property
    def created_at(self):
        return self.__raw_data.created_at

    @property
    def name(self):
        return self.__raw_data.name

    @property
    def folders_count(self):
        return self.__raw_data.folders_count

    @property
    def parent_id(self):
        return self.__raw_data.parent_id

    @property
    def parent(self):
        return self.__raw_data.parent


class File:
    def __init__(self, raw_data: RawFile, state: ConnectionState):
        self.__raw_data = raw_data
        self.__state = state

    @property
    def id(self):
        return self.__raw_data.id

    @property
    def created_at(self):
        return self.__raw_data.created_at

    @property
    def name(self):
        return self.__raw_data.name

    @property
    def type(self):
        return self.__raw_data.type

    @property
    def md5(self):
        return self.__raw_data.md5

    @property
    def size(self):
        return self.__raw_data.size

    @property
    def is_sensitive(self):
        return self.__raw_data.is_sensitive

    @property
    def blurhash(self):
        return self.__raw_data.blurhash

    @property
    def properties(self):
        return self.__raw_data.properties

    @property
    def url(self):
        return self.__raw_data.url

    @property
    def thumbnail_url(self):
        return self.__raw_data.thumbnail_url

    @property
    def comment(self):
        return self.__raw_data.comment

    @property
    def folder_id(self):
        return self.__raw_data.folder_id

    @property
    def folder(self):
        return self.__raw_data.folder

    @property
    def user_id(self):
        return self.__raw_data.user_id

    @property
    def user(self):
        return User(RawUser(self.__raw_data.user), state=self.__state)


class Drive:
    def __init__(self, data, state: ConnectionState) -> None:
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.name: str = data['name']
        self.type: str = data['type']
        self.md5: str = data['md5']
        self.size: int = data['size']
        self.url: str = data['url']
        self.folder_id: str = data['folder_id']
        self.is_sensitive: bool = data['is_sensitive']
        self.blurhash: str = data['blurhash']
        self._state = state

    async def delete(self) -> bool:
        """
        ファイルを削除します。

        Returns
        -------
        bool
            削除に成功したかどうか
        """

        return await self._state.remove_file(self.id)
