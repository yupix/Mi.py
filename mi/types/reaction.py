from typing import TypedDict

from mi.types import User


class NoteReactionPayload(TypedDict):
    id: str
    created_at: str
    user: User
    type: str
