from typing import Any, Dict, Optional

from mi.types.drive import (File as FilePayload, Folder as FolderPayload, Properties as PropertiesPayload)


class RawProperties:
    def __init__(self, data: PropertiesPayload):
        self.width: int = data['width']
        self.height: int = data['height']
        self.avg_color: Optional[float] = data.get('avg_color')


class RawFolder:
    def __init__(self, data: FolderPayload):
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.name: str = data['name']
        self.folders_count: int = data['folders_count']
        self.parent_id: str = data['parent_id']
        self.parent: Dict[str, Any] = data['parent']


class RawFile:
    def __init__(self, data: FilePayload):
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.name: str = data['name']
        self.type: str = data['type']
        self.md5: str = data['md5']
        self.size: int = data['size']
        self.is_sensitive: bool = data['is_sensitive']
        self.blurhash: str = data['blurhash']
        self.properties: RawProperties = RawProperties(data['properties'])
        self.url: str = data['url']
        self.thumbnail_url: str = data['thumbnail_url']
        self.comment: str = data['comment']
        self.folder_id: str = data['folder_id']
        self.folder: Optional[RawFolder] = RawFolder(data['folder']) if data.get('folder') else None
        self.user_id: str = data['user_id']
        self.user: Dict[str, Any] = data['user']