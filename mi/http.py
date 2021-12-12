"""
Mi.pyのWebSocket部分
"""

import json
import sys
from typing import Any, Dict, Optional, Union

import aiohttp

from mi.gateway import MisskeyClientWebSocketResponse
from mi.utils import upper_to_lower
from . import __version__, config, exception


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

    async def request(self, route: Route, *, files=None, form=None, **kwargs) -> Union[Union[bool, dict[str, Any]], Any]:
        headers: Dict[str, str] = {
            'User-Agent': self.user_agent,
        }

        if json in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = kwargs.pop('json')
        is_lower = kwargs.pop('lower') if kwargs.get('lower') else False

        if kwargs.pop('auth'):
            if kwargs.get('json') is None:
                kwargs['json'] = {}
            kwargs['json']['i'] = self.token
        async with self.__session.request(route.method, route.url, **kwargs) as res:
            data = await json_or_text(res)
            if is_lower:
                data = upper_to_lower(data)
            if res.status == 204:
                return True
            if 300 > res.status >= 200:
                return data

        errors = {
            400: {"raise": exception.ClientError, "description": "Client Error"},
            401: {
                "raise": exception.AuthenticationError,
                "description": "AuthenticationError",
            },
            418: {"raise": exception.ImAi, "description": "I'm Ai"},
            500: {
                "raise": exception.InternalServerError,
                "description": "InternalServerError",
            },
        }
        if res.status in [400, 401, 418, 500]:
            error_base: Dict[str, Any] = errors[res.status]
            error = error_base["raise"](
                f"{error_base['description']} => {data['error']['message']}  \n {res.text}"
            )
            raise error

    async def static_login(self, token: str):
        self.token = token
        self.__session = aiohttp.ClientSession(connector=self.connector, ws_response_class=MisskeyClientWebSocketResponse)
        data = await self.request(Route('POST', '/api/i'), auth=True)
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
