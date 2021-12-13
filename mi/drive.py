from typing import Any, Dict, Optional

from pydantic import BaseModel


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


class Drive(BaseModel):
    id: Optional[str] = None
    created_at: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    md5: Optional[str] = None
    size: Optional[int] = None
    url: Optional[str] = None
    folder_id: Optional[str] = None
    is_sensitive: Optional[bool] = False
    blurhash: Optional[str] = None

