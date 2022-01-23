from typing import Optional

__all__ = ['RawInstance']

from mi.types import Instance


class RawInstance:
    def __init__(self, data: Instance):
        self.host: Optional[str] = data.get('host')
        self.name: Optional[str] = data.get('name')
        self.software_name: Optional[str] = data.get('software_version')
        self.software_version: Optional[str] = data.get('software_version')
        self.icon_url: Optional[str] = data.get('icon_url')
        self.favicon_url: Optional[str] = data.get('favicon_url')
        self.theme_color: Optional[str] = data.get('theme_color')
