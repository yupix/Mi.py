from dataclasses import dataclass
from typing import Optional

__all__ = ['RawInstance']


@dataclass
class RawInstance:
    host: Optional[str] = None
    name: Optional[str] = None
    software_name: Optional[str] = None
    software_version: Optional[str] = None
    icon_url: Optional[str] = None
    favicon_url: Optional[str] = None
    theme_color: Optional[str] = None
