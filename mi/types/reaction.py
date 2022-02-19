from typing import TypedDict

from mi.types import UserPayload


class NoteReactionPayload(TypedDict):
    id: str
    created_at: str
    user: UserPayload
    type: str
