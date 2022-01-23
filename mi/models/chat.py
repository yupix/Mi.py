from typing import List

from mi.types.chat import Chat as ChatPayload
from .user import RawUser


class RawChat:
    def __init__(self, data: ChatPayload):
        self.id: str = data["id"]
        self.created_at: str = data["created_at"]
        self.content: str = data["text"]
        self.user_id: str = data["user_id"]
        self.author: RawUser = RawUser(data["user"])
        self.recipient_id: str = data["recipient_id"]
        self.recipient: str = data["recipient"]
        self.group_id: str = data["group_id"]
        self.file_id: str = data["file_id"]
        self.is_read: bool = data["is_read"]
        self.reads: List = data["reads"]
