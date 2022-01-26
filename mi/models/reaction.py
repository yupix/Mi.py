from mi.types import UserPayload
from mi.types.reaction import NoteReactionPayload

__all__ = ['RawNoteReaction']


class RawNoteReaction:
    def __init__(self, data: NoteReactionPayload):
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.user: UserPayload = data['user']
        self.reaction: str = data['type']
