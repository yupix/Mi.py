from __future__ import annotations

import asyncio
from typing import Optional, TYPE_CHECKING

from mi.drive import Folder
from mi.http import HTTPClient, Route
from mi.models.drive import RawFolder

if TYPE_CHECKING:
    from mi.client import ConnectionState


class FolderManager:
    def __init__(self, client: 'ConnectionState', http: HTTPClient, loop: asyncio.AbstractEventLoop,
                 folder_id: Optional[str] = None):
        self.client = client
        self.http = http
        self.loop = loop
        self.__folder_id = folder_id

    async def create(self, name: str, parent_id: Optional[str] = None) -> bool:
        parent_id = parent_id or self.__folder_id

        data = {'name': name, 'parent_id': parent_id}
        return bool(await self.http.request(Route('POST', '/api/drive/folders/create'), json=data, lower=True, auth=True))

    async def delete(self, folder_id: Optional[str] = None) -> bool:
        folder_id = folder_id or self.__folder_id
        data = {'folderId': folder_id}
        return bool(await self.http.request(Route('POST', '/api/drive/folders/delete'), json=data, lower=True, auth=True))


class DriveManager:
    def __init__(self, client: 'ConnectionState', http: HTTPClient, loop: asyncio.AbstractEventLoop):
        self.client = client
        self.http = http
        self.loop = loop

    async def get_folders(self, limit: int = 100, since_id: Optional[str] = None, until_id: Optional[str] = None,
                          folder_id: Optional[str] = None):
        data = {
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
            'folderId': folder_id
        }
        data = await self.http.request(Route('POST', '/api/drive/folders'), json=data, lower=True, auth=True)
        print(data)
        return [Folder(RawFolder(i), state=self.client) for i in data]
