from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mi.actions.admin import AdminActions
from mi.actions.drive import DriveActions
from mi.actions.note import NoteActions
from mi.actions.user import UserActions
from mi.wrapper.chart import ChartManager
from mi.wrapper.chat import ChatManager
from mi.wrapper.reaction import ReactionManager

if TYPE_CHECKING:
    from mi.framework.models import User


class ClientActions:
    def __init__(self, *args, **kwargs):
        self.note: NoteActions = NoteActions(*args, **kwargs)
        self.chat: ChatManager = ChatManager(*args, **kwargs)
        self.admin: AdminActions = AdminActions(*args, **kwargs)
        self.user: UserActions = UserActions(*args, **kwargs)
        self.drive: DriveActions = DriveActions(*args, **kwargs)
        self.reaction: ReactionManager = ReactionManager(*args, **kwargs)
        self.chart: ChartManager = ChartManager(*args, **kwargs)

    def get_user_instance(self, user_id: Optional[str] = None, user: Optional[User] = None) -> UserActions:
        return UserActions(user_id=user_id, user=user)

    def get_note_instance(self, note_id: str) -> NoteActions:
        return NoteActions(note_id=note_id)
