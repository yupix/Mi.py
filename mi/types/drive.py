from typing import Any, Dict, TypedDict


class Properties(TypedDict):
    """
    プロパティー情報
    """

    width: int
    height: int
    avgColor: str


class Folder(TypedDict):
    """
    フォルダーの情報
    """

    id: str
    created_at: str
    name: str
    folders_count: int
    files_count: int
    parent_id: str
    parent: Dict[str, Any]


class File(TypedDict):
    """
    ファイル情報
    """

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
