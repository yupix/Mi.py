from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class AbstractBotBase(ABC):
    @abstractmethod
    async def dispatch(self, event_name: Optional[str] = None, *args: tuple[Any], **kwargs: Dict[Any, Any]):
        pass

    @abstractmethod
    async def event_dispatch(self, event_name: Optional[str] = None, *args: tuple[Any], **kwargs: Dict[Any, Any]):
        pass
