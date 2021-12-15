from __future__ import annotations
from typing import TYPE_CHECKING, Any, Dict

from pydantic import BaseModel

if TYPE_CHECKING:
    from .state import ConnectionState

class Properties(BaseModel):
    width: int
    height: int
    avgColor: str


class Folder(BaseModel):
    id: str
    createdAt: str
    name: str
    foldersCount: int
    filesCount: int
    parentId: str
    parent: Dict[str, Any]


class File(BaseModel):
    id: str
    createdAt: str
    name: str
    type: str
    md5: str
    size: int
    isSensitive: bool
    blurhash: str
    properties: Properties
    url: str
    thumbnailUrl: str
    comment: str
    folderId: str
    folder: Folder
    userId: str
    user: Dict[str, Any]


class Drive:
    def __init__(self, data, state: ConnectionState) -> None:
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.name: str = data['name']
        self.type: str=  data['type']
        self.md5: str = data['md5']
        self.size: int = data['size']
        self.url: str = data['url']
        self.folder_id: str = data['folder_id']
        self.is_sensitive: bool = data['is_sensitive']
        self.blurhash: str = data['blurhash']
        self._state = state

