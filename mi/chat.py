from __future__ import annotations

from typing import List, TYPE_CHECKING

from .abc.chat import AbstractChatContent
from .types.chat import Chat as ChatPayload
from .user import User

__all__ = ['Chat']

if TYPE_CHECKING:
    from mi.state import ConnectionState


class Chat(AbstractChatContent):
    """
    チャットオブジェクト
    """

    def __init__(self, data: ChatPayload, state: ConnectionState):
        self.id: str = data["id"]
        self.created_at: str = data["created_at"]
        self.content: str = data["text"]
        self.user_id: str = data["user_id"]
        self.author: User = User(data["user"], state=state)
        self.recipient_id: str = data["recipient_id"]
        self.recipient: str = data["recipient"]
        self.group_id: str = data["group_id"]
        self.file_id: str = data["file_id"]
        self.is_read: bool = data["is_read"]
        self.reads: List = data["reads"]
        self._state = state

    async def delete(self) -> bool:
        """
        チャットを削除します（チャットの作者である必要があります）

        Returns
        -------
        bool:
            成功したか否か
        """
        res = await self._state.delete_chat(message_id=self.id)
        return bool(res)
