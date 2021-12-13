from typing import List, TypedDict

from mi.types.user import User


class Chat(TypedDict):
    id: str
    created_at: str
    text: str
    user_id: str
    user: User
    recipient_id: str
    recipient: str
    group_id: str
    file_id: str
    is_read: bool
    reads: List
