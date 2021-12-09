"""
Mi.pyのWebSocket部分
"""

import asyncio
import json
import sys
import uuid
from typing import Any, Dict, Optional

import websockets
import aiohttp
from websockets.legacy.client import WebSocketClientProtocol
from mi.gateway import MisskeyClientWebSocketResponse

from . import __version__, config
from mi.router import Router
from mi.types.bot import AbstractBotBase
from mi.utils import get_module_logger, upper_to_lower


class _MissingSentinel:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return '...'


MISSING: Any = _MissingSentinel()


class Route:
    def __init__(self, method: str, path: str, **parameters: Any):
        self.path: str = path
        self.method: str = method
        self.url = config.i.origin_uri + path


async def json_or_text(response: aiohttp.ClientResponse):
    text = await response.text(encoding='utf-8')
    try:
        if 'application/json' in response.headers['Content-Type']:
            return json.loads(text)
    except KeyError:
        pass

class HTTPClient:
    def __init__(self, connector: Optional[aiohttp.BaseConnector] = None) -> None:
        self.connector = connector
        user_agent = 'Misskey Bot (https://github.com/yupix/Mi.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
        self.__session: aiohttp.ClientSession = MISSING
        self.token: Optional[str] = None

    async def request(self, route: Route, *, files=None, form=None, **kwargs):
        headers: Dict[str, str] = {
            'User-Agent': self.user_agent,
        }

        if json in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = kwargs.pop('json')

        if kwargs.pop('auth'):
            if kwargs.get('json') is None:
                kwargs['json'] = {}
            kwargs['json']['i'] = self.token

        async with self.__session.request(route.method, route.url, **kwargs) as res:
            data = await json_or_text(res)
            return data

    async def static_login(self, token: str):
        self.token = token
        self.__session = aiohttp.ClientSession(connector=self.connector, ws_response_class=MisskeyClientWebSocketResponse)
        data = await self.request(Route('POST', '/api/i'), auth=True)
        print(data)
        return data



    async def ws_connect(self, url: str, *, compress: int = 0) -> Any:
        kwargs = {
            'autoclose': False,
            'max_msg_size': 0,
            'timeout': 30.0,
            'headers': {
                'User-Agent': self.user_agent
            },
            'compress': compress
        }
        return await self.__session.ws_connect(url, **kwargs)


class WebSocket:
    """Misskey APIとやり取りを行うWebSocket object"""

    __slots__ = ["web_socket", "cls", "router", "auth_i", "logger"]

    def __init__(self, cls: AbstractBotBase):
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

        await getattr(self.cls._connection, f"_parse_{base_type}")(message)
