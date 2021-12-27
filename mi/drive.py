from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from .types.drive import (File as FilePayload, Folder as FolderPayload)

if TYPE_CHECKING:
    from .state import ConnectionState


class Properties:
    def __init__(self, data):
        self.width: int = data['width']
        self.height: int = data['height']
        self.avg_color: float = data['avg_color']


class Folder:
    def __init__(self, data: FolderPayload, state: ConnectionState):
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.name: str = data['name']
        self.folders_count: int = data['folders_count']
        self.parent_id: str = data['parent_id']
        self.parent: Dict[str, Any] = data['parent']
        self._state = state


class File:
    def __init__(self, data: FilePayload, state: ConnectionState):
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.name: str = data['name']
        self.type: str = data['type']
        self.md5: str = data['md5']
        self.size: int = data['size']
        self.is_sensitive: bool = data['is_sensitive']
        self.blurhash: str = data['blurhash']
        self.properties: Properties = Properties(data['properties'])
        self.url: str = data['url']
        self.thumbnail_url: str = data['thumbnail_url']
        self.comment: str = data['comment']
        self.folder_id: str = data['folder_id']
        self.folder: Folder = Folder(data['folder'], state=state)
        self.user_id: str = data['user_id']
        self.user: Dict[str, Any] = data['user']


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
