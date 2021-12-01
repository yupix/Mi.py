from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Union


class AbstractGroupMixin(ABC):
    @property
    @abstractmethod
    def command(self):
        pass

    @abstractmethod
    def add_command(self, command: "AbstractCommand"):
        pass

    @abstractmethod
    def remove_command(self, name:str):
        pass

class AbstractCommand(ABC):
    @property
    @abstractmethod
    def full_parent_name(self) -> str:
        pass

    @property
    @abstractmethod
    def qualified_name(self) -> str:
        pass

    @abstractmethod
    def _ensure_assignment_on_copy(self, other: 'AbstractCommand') -> 'AbstractCommand':
        pass

    @abstractmethod
    def copy(self) -> 'AbstractCommand':
        pass

    @abstractmethod
    def _update_copy(self, kwargs: Dict[Any, Any]) -> 'AbstractCommand':
        pass


class AbstractGroup(ABC):
    pass