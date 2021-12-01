from abc import ABC, abstractmethod
import asyncio
from types import ModuleType
from typing import Any, Callable, Coroutine, Dict, Optional, Tuple

from websockets.legacy.client import WebSocketClientProtocol

from mi.abc.ext.core import AbstractGroupMixin

from .context import Context


class AbstractBotBase(AbstractGroupMixin):
    @abstractmethod
    async def can_run(self, ctx: Context, *, call_once: bool = False):
        pass

    @abstractmethod
    async def invoke(self, ctx: Context, *args: Tuple[Any], **kwargs: Dict[Any, Any]):
        pass

    @abstractmethod
    async def get_context(self, message, *, cls: Any = Context):
        pass

    @abstractmethod
    async def process_commands(self, message):
        pass

    @abstractmethod
    async def _on_message(self, message):
        pass

    @abstractmethod
    async def on_ready(self, ws: WebSocketClientProtocol):
        pass

    @abstractmethod
    def event(self, name: Optional[str] = None):
        pass

    @abstractmethod
    def add_event(self, func, name: Optional[str] = None):
        pass

    @abstractmethod
    def listen(self, name: Optional[str] = None):
        pass

    @abstractmethod
    def add_listener(self, func, name: Optional[str] = None):
        pass

    @abstractmethod
    async def event_dispatch(self, event_name: str, *args: Tuple[Any], **kwargs: Dict[Any, Any]):
        pass

    @abstractmethod
    async def dispatch(self, event_name: str, *args: Tuple[Any], **kwargs: Dict[Any, Any]):
        pass

    @abstractmethod
    def add_cog(self, cog, override: bool = False) -> None:
        pass

    @abstractmethod
    def remove_cog(self, name: str) -> None:
        pass

    @abstractmethod
    def _load_from_module(self, spec: ModuleType, key: str) -> None:
        pass

    @staticmethod
    @abstractmethod
    def _resolve_name(name: str, package: Optional[str]) -> str:
        pass

    @abstractmethod
    def load_extension(self, name: str, package: Optional[str] = None) -> None:
        pass

    @abstractmethod
    async def schedule_event(
            self,
            coro: Callable[..., Coroutine[Any, Any, Any]],
            event_name: str,
            *args: tuple[Any],
            **kwargs: Dict[Any, Any],
    ) -> asyncio.Task[Any]:
        pass

    @abstractmethod
    async def _run_event(
            self,
            coro: Callable[..., Coroutine[Any, Any, Any]],
            event_name: str,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        pass

    @staticmethod
    @abstractmethod
    async def __on_error(event_method: str) -> None:
        pass

    @abstractmethod
    async def on_error(self, err):
        pass

    @abstractmethod
    def run(self, uri: str, token: str, debug: bool = False) -> None:
        pass
