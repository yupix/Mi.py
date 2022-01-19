from typing import Any, Dict, Optional, TypedDict


class Properties(TypedDict):
    """
    プロパティー情報
    """

    width: int
    height: int
    avg_color: Optional[str]


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
    created_at: str
    name: str
    type: str
    md5: str
    size: int
    is_sensitive: bool
    blurhash: str
    properties: Properties
    url: str
    thumbnail_url: str
    comment: str
    folder_id: str
    folder: Folder
    user_id: str
    user: Dict[str, Any]
