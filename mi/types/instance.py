from typing import Optional, TypedDict


class Instance(TypedDict):
    name: Optional[str]
    software_name: Optional[str]
    software_version: Optional[str]
    icon_url: Optional[str]
    favicon_url: Optional[str]
    theme_color: Optional[str]
