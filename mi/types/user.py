from typing import List, Optional, TypedDict

from .instance import Instance


class Author(TypedDict):
    id: Optional[str]
    name: Optional[str]
    username: Optional[str]
    host: Optional[str]
    avatar_url: Optional[str]
    avatar_blurhash: Optional[str]
    avatar_color: Optional[str]
    is_admin: Optional[bool]
    is_bot: Optional[bool]
    is_cat: Optional[bool]
    is_lady: Optional[bool]
    emojis: Optional[List]
    online_status: Optional[str]
    instance: Optional[Instance]
