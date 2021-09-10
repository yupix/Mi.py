from typing import List, Optional

from pydantic import BaseModel


class Emoji(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    host: Optional[str]
    aliases: Optional[List[str]]
