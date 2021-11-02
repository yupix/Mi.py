from typing import List, Optional, TypedDict


class Emoji(TypedDict):
    name: Optional[str]
    url: Optional[str]
    host: Optional[str]
    aliases: Optional[List[str]]
