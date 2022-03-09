from typing import List, TypedDict

from mi.types.user import UserPayload

__all__ = ('ChatPayload',)


class ChatPayload(TypedDict):
    id: str
    created_at: str
    text: str
    user_id: str
    user: UserPayload
    recipient_id: str
    recipient: str
    group_id: str
    file_id: str
    is_read: bool
    reads: List
