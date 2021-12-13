from abc import ABC, abstractmethod


class AbstractChat(ABC):
    @abstractmethod
    async def send(self) -> 'AbstractChatContent':
        pass


class AbstractChatContent(ABC):
    @abstractmethod
    async def delete(self):
        pass
