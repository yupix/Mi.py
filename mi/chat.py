from __future__ import annotations
from typing import TYPE_CHECKING, List

from .abc.chat import AbstractChat, AbstractChatContent
from .types.chat import Chat as ChatPayload
from .user import User
from .utils import api, remove_dict_empty, upper_to_lower

__all__ = ['Chat', 'ChatContent']

if TYPE_CHECKING:
    from mi.state import ConnectionState

class Chat(AbstractChat):
    """
    チャットを行う際に使用するクラス
    """

    def __init__(
            self,
            content: str,
            *,
            user_id: str = None,
            group_id: str = None,
            file_id: str = None
    ):
        self.content = content
        self.user_id = user_id
        self.group_id = group_id
        self.file_id = file_id
        self.__payload = {
            "userId": self.user_id,
            "groupId": self.group_id,
            "text": self.content,
            "fileId": self.file_id,
        }

    async def send(self) -> "ChatContent":
        """
        チャットを投稿します

        Returns
        -------
        ChatContent
        """
        res = api(
            "/api/messaging/messages/create",
            remove_dict_empty(self.__payload),
            auth=True,
        ).json()
        return ChatContent(
            upper_to_lower(res,
                           replace_list={"user": "author", "text": "content"})
        )

    def add_file(
            self,
            path: str = None,
            name: str = None,
            force: bool = False,
            is_sensitive: bool = False,
            url: str = None,
    ):
        pass


class ChatContent(AbstractChatContent):
    """
    チャットオブジェクト
    """

    def __init__(self, data: ChatPayload, state: ConnectionState):
        self.id: str = data["id"]
        self.created_at: str = data["created_at"]
        self.content: str = data["text"]
        self.user_id: str = data["user_id"]
        self.author: User = User(data["user"])
        self.recipient_id: str = data["recipient_id"]
        self.recipient: str = data["recipient"]
        self.group_id: str = data["group_id"]
        self.file_id: str = data["file_id"]
        self.is_read: bool = data["is_read"]
        self.reads: List = data["reads"]
        self._state = state

    async def delete(self):
        """
        チャットを削除します（チャットの作者である必要があります）

        Returns
        -------
        bool:
            成功したか否か
        """
        res = await self._state._delete_chat(self.id)
        return res.status_code == 204
