"""Mi.pyのWebSocket部分"""

import json
import sys
from typing import Any, Dict, Optional

import aiohttp
from mi import __version__, exception
from mi.framework.gateway import MisskeyClientWebSocketResponse
from mi.framework.router import Route
from mi.utils import remove_dict_empty, upper_to_lower

__all__ = ('HTTPClient', 'HTTPSession')


class _MissingSentinel:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return '...'


MISSING: Any = _MissingSentinel()


async def json_or_text(response: aiohttp.ClientResponse):
    text = await response.text(encoding='utf-8')
    try:
        if 'application/json' in response.headers['Content-Type']:
            return json.loads(text)
    except KeyError:
        pass


class HTTPClient:
    def __init__(self) -> None:
        user_agent = 'Misskey Bot (https://github.com/yupix/Mi.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format(__version__, sys.version_info, aiohttp.__version__)
        self.__session: aiohttp.ClientSession = MISSING
        self.token: Optional[str] = None

    async def request(self, route: Route, **kwargs) -> Any:
        headers: Dict[str, str] = {
            'User-Agent': self.user_agent,
        }

        is_lower = kwargs.pop('lower') if kwargs.get('lower') else False

        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['json'] = kwargs.pop('json')

        if kwargs.get('auth') and kwargs.pop('auth'):
            if 'json' in kwargs or 'data' not in kwargs:
                key = 'json'
            else:
                key = 'data'
            if not kwargs.get(key):
                kwargs[key] = {}
            kwargs[key]['i'] = self.token

        for i in ('json', 'data'):
            if kwargs.get(i):
                kwargs[i] = remove_dict_empty(kwargs[i])
        async with self.__session.request(route.method, route.url, **kwargs) as res:
            data = await json_or_text(res)
            if is_lower:
                if isinstance(data, list):
                    data = [upper_to_lower(i) for i in data]
                else:
                    data = upper_to_lower(data)
        errors = {
            400: {"raise": exception.ClientError, "description": "Client Error"},
            401: {
                "raise": exception.AuthenticationError,
                "description": "AuthenticationError",
            },
            403: {
                "raise": exception.AuthenticationError,
                "description": "AuthenticationError",
            },
            404: {
                'raise': exception.NotFoundError,
                'description': 'NotFoundError'
            },
            418: {"raise": exception.ImAi, "description": "I'm Ai"},
            500: {
                "raise": exception.InternalServerError,
                "description": "InternalServerError",
            },
        }
        if res.status in errors:
            error_base: Dict[str, Any] = errors[res.status]
            error = error_base["raise"](
                f"{error_base['description']} => {data['error']['message']}  \n {res.text}"
            )
            raise error

        if res.status == 204:
            return True

        if 300 > res.status >= 200:
            return data

    async def static_login(self, token: str):
        self.token = token
        self.__session = aiohttp.ClientSession(ws_response_class=MisskeyClientWebSocketResponse)
        data = await self.request(Route('POST', '/api/i'), auth=True)
        return data

    async def close_session(self):
        await self.__session.close()

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
        try:
            ws = await self.__session.ws_connect(url,**kwargs)
        except aiohttp.client_exceptions.ClientConnectorError:
            raise exception.ClientConnectorError()
        return ws


HTTPSession: HTTPClient = HTTPClient()
