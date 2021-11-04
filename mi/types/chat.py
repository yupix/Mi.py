from typing import List, TypedDict

from mi.types.user import Author


class Chat(TypedDict):
    id: str
    created_at: str
    content: str
    user_id: str
    author: Author
    recipient_id: str
    recipient: str
    group_id: str
    file_id: str
    is_read: bool
    reads: List
