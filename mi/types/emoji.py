from typing import List, Optional, TypedDict


class Emoji(TypedDict):
    id: Optional[str]
    aliases: Optional[List[str]]
    name: Optional[str]
    category: Optional[str]
    host: Optional[str]
    url: Optional[str]
