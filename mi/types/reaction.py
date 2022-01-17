from typing import TypedDict

from mi.types import User


class NoteReaction(TypedDict):
    id: str
    created_at: str
    user: User
    type: str
