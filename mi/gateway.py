from __future__ import annotations

import json
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING

import aiohttp

from mi.utils import str_lower
from . import config

if TYPE_CHECKING:
    from .client import Client

__all__ = ('MisskeyWebSocket', 'MisskeyClientWebSocketResponse')


class MisskeyClientWebSocketResponse(aiohttp.ClientWebSocketResponse):
    async def close(self, *, code: int = 4000, message: bytes = b'') -> bool:
        return await super().close(code=code, message=message)


class MisskeyWebSocket:
    def __init__(self, socket):
        self.socket = socket
        self._dispatch = lambda *args: None
        self._connection = None
        self._misskey_parsers: Optional[Dict[str, Callable[..., Any]]] = None

    @classmethod
    async def from_client(cls, client: Client, *, timeout: int = 60):
        socket = await client.http.ws_connect(client.url + f'?i={config.i.token}')
        ws = cls(socket)
        ws._dispatch = client.dispatch
        ws._connection = client._connection
        ws._misskey_parsers = client._connection.parsers
        client.dispatch('ready', socket)
        await ws.poll_event(timeout=timeout)
        return ws

    async def received_message(self, msg, /):
        if type(msg) is bytes:
            msg = msg.decode()

        self._misskey_parsers[str_lower(msg['type']).upper()](msg)

    async def poll_event(self, *, timeout: int = 60):
        msg = await self.socket.receive(timeout=timeout)  # TODO: いつか変数に
        if msg.type is aiohttp.WSMsgType.TEXT:
            await self.received_message(json.loads(msg.data))
