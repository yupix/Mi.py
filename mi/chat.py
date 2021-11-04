from typing import List

from .abc.chat import AbstractChat
from .types.chat import Chat as ChatPayload
from .user import Author
from .utils import api, remove_dict_empty


class Chat(AbstractChat):

    def __init__(self, content: str, *, user_id: str = None, group_id: str = None, file_id: str = None):
        self.content = content
        self.user_id = user_id
        self.group_id = group_id
        self.file_id = file_id
        self.__payload = {
            'userId': self.user_id,
            'groupId': self.group_id,
            'text': self.content,
            'fileId': self.file_id
        }

    async def send(self):
        return api('/api/messaging/messages/create', remove_dict_empty(self.__payload), auth=True)

    def add_file(self, path: str = None, name: str = None, force: bool = False, is_sensitive: bool = False, url: str = None):
        pass


class ChatContent:
    def __init__(self, data: ChatPayload):
        self.id: str = data['id']
        self.created_at: str = data['created_at']
        self.content: str = data['content']
        self.user_id: str = data['user_id']
        self.author: Author = Author(data['author'])
        self.recipient_id: str = data['recipient_id']
        self.recipient: str = data['recipient']
        self.group_id: str = data['group_id']
        self.file_id: str = data['file_id']
        self.is_read: bool = data['is_read']
        self.reads: List = data['reads']
