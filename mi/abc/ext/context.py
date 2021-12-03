from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

class AbstractContext(ABC):
    @abstractmethod
    async def invoke(self, command, /, *args: Tuple[Any], **kwargs: Dict[Any, Any]):
        pass