from typing import Optional

from pydantic import BaseModel


class Instance(BaseModel):
    name: Optional[str] = None
    software_name: Optional[str] = None
    software_version: Optional[str] = None
    icon_url: Optional[str] = None
    favicon_url: Optional[str] = None
    theme_color: Optional[str] = None
