from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

class Context(ABC):
    @abstractmethod
    async def invoke(self, command, /, *args: Tuple[Any], **kwargs: Dict[Any, Any]):
        pass