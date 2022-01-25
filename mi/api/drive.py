from __future__ import annotations

import asyncio
from typing import List, Optional, TYPE_CHECKING

from mi.drive import File, Folder
from mi.exception import InvalidParameters
from mi.http import HTTPClient, Route
from mi.models.drive import RawFile, RawFolder
from mi.utils import remove_dict_empty

if TYPE_CHECKING:
    from mi.client import ConnectionState


class FileManager:
    def __init__(self, __state: 'ConnectionState', http: HTTPClient, loop: asyncio.AbstractEventLoop,
                 file_id: Optional[str] = None):
        self.__state = __state
        self.__http = http
        self.__loop = loop
        self.__file_id = file_id

    async def show_file(self, file_id: Optional[str], url: Optional[str]) -> File:
        data = remove_dict_empty({"fileId": file_id, "url": url})
        res = await self.__http.request(Route('POST', '/api/admin/drive/show-file'), json=data, auth=True, lower=True)
        return File(RawFile(res), state=self.__state)

    async def remove_file(self, file_id: Optional[str] = None) -> bool:
        """
        指定したIDのファイルを削除します

        Parameters
        ----------
        file_id : Optional[str], default=None
            削除するファイルのID

        Returns
        -------
        bool
            削除に成功したかどうか
        """

        file_id = file_id or self.__file_id
        return bool(await self.__http.request(Route('POST', '/api/drive/files/delete'), json={'fileId': file_id}, auth=True))


class FolderManager:
    def __init__(self, __state: 'ConnectionState', http: HTTPClient, loop: asyncio.AbstractEventLoop,
                 folder_id: Optional[str] = None):
        self.__state = __state
        self.__http = http
        self.__loop = loop
        self.__folder_id = folder_id

    async def create(self, name: str, parent_id: Optional[str] = None) -> bool:
        parent_id = parent_id or self.__folder_id

        data = {'name': name, 'parent_id': parent_id}
        return bool(await self.__http.request(Route('POST', '/api/drive/folders/create'), json=data, lower=True, auth=True))

    async def delete(self, folder_id: Optional[str] = None) -> bool:
        folder_id = folder_id or self.__folder_id
        data = {'folderId': folder_id}
        return bool(await self.__http.request(Route('POST', '/api/drive/folders/delete'), json=data, lower=True, auth=True))

    async def get_files(self, limit: int = 10, since_id: Optional[str] = None, until_id: Optional[str] = None, folder_id: Optional[str] = None, file_type: Optional[str] = None) -> List[File]:

        if limit >= 100:
            raise InvalidParameters('limit must be less than 100')

        folder_id = folder_id or self.__folder_id
        data = {'limit': limit, 'sinceId': since_id, 'untilId': until_id, 'folderId': folder_id, 'Type': file_type}
        res = await self.__http.request(Route('POST', '/api/drive/files'), json=data, auth=True, lower=True)
        return [File(RawFile(i), state=self.__state) for i in res]


class DriveManager:
    def __init__(self, __state: 'ConnectionState', http: HTTPClient, loop: asyncio.AbstractEventLoop):
        self.__state = __state
        self.__http = http
        self.__loop = loop

    async def get_folders(self, limit: int = 100, since_id: Optional[str] = None, until_id: Optional[str] = None,
                          folder_id: Optional[str] = None) -> List[Folder]:
        data = {
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
            'folderId': folder_id
        }
        data = await self.__http.request(Route('POST', '/api/drive/folders'), json=data, lower=True, auth=True)
        print(data)
        return [Folder(RawFolder(i), state=self.__state) for i in data]
