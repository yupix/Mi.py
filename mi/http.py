"""
Mi.pyのWebSocket部分
"""

import asyncio
import json
import uuid
from typing import Any

import websockets
from websockets.legacy.client import WebSocketClientProtocol

from mi.router import Router
from mi.types.bot import AbstractBotBase
from mi.utils import get_module_logger, upper_to_lower


class WebSocket:
    """Misskey APIとやり取りを行うWebSocket object"""

    __slots__ = ["web_socket", "cls", "router", "auth_i", "logger"]

    def __init__(self, cls:AbstractBotBase):
        self.logger = get_module_logger(__name__)
        self.web_socket = None
        self.cls = cls
        self.router: Router

    async def run(self, uri: str) -> None:
        """
        WebSocketを起動してMisskeyインスタンスのセッションを確立します

        Parameters
        ----------
        uri : str

        Returns
        -------
        None
        """

        try:
            async with websockets.connect(uri) as web_socket:
                asyncio.create_task(self.on_ready(web_socket))
                while True:
                    await web_socket.send(
                        json.dumps(
                            {
                                "type": "connect",
                                "body": {
                                    "channel": "main",
                                    "id": f"{uuid.uuid4()}",
                                    "params": {"some": "thing"},
                                },
                            },
                            ensure_ascii=False,
                        )
                    )
                    recv = await web_socket.recv()
                    asyncio.create_task(self.recv(web_socket, recv))
        except Exception as err:
            asyncio.create_task(self.cls.__on_error(err))

    async def on_ready(self, web_socket: WebSocketClientProtocol) -> None:
        """
        Botの起動準備が完了した際にイベントを実行する関数

        Parameters
        ----------
        web_socket

        Returns
        -------
        None
        """

        self.router = Router(web_socket)
        await self.cls.event_dispatch("ready", web_socket)

    async def recv(self, web_socket: Any, message: Any):
        """
        WebSocketで受け取ったデータをparseして各イベントに分担する関数

        Parameters
        ----------
        web_socket :
        message :
        """
        message = upper_to_lower(json.loads(message))
        base_type = message.get('type')
        self.logger.debug(f"received: {message}")
        self.logger.debug(f'BaseType: parse_{base_type}')

        await getattr(self.cls._connection , f"_parse_{base_type}")(message)

