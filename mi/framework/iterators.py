from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Optional

from mi.framework.models.user import User
from mi.framework.router import Route
from mi.utils import remove_dict_empty
from mi.wrapper.models.user import RawUser

if TYPE_CHECKING:
    from . import ConnectionState

__all__ = ('InstanceIterator',)


class InstanceIterator:
    def __init__(self, state: ConnectionState):
        self._state = state

    async def get_users(self, limit: int = 10,
                        *,
                        offset: int = 0,
                        sort: Optional[str] = None,
                        state: str = 'all',
                        origin: str = 'local',
                        username: Optional[str] = None,
                        hostname: Optional[str] = None,
                        get_all: bool = False
                        ) -> Generator[User]:
        """
        Parameters
        ----------
        limit: int
        offset:int
        sort:str
        state:str
        origin:str
        username:str
        hostname:str
        get_all:bool

        Returns
        -------
        Iterator[User]
        """
        args = remove_dict_empty({'limit': limit,
                                  'offset': offset,
                                  'sort': sort,
                                  'state': state,
                                  'origin': origin,
                                  'username': username,
                                  'hostname': hostname
                                  })
        res = await self._state.http.request(Route('POST', '/api/admin/show-users'), json=args, auth=True, lower=True)

        if get_all:
            while True:
                for i in res:
                    yield User(RawUser(i))
                args['offset'] = args['offset'] + len(res)
                res = await self._state.http.request(Route('POST', '/api/admin/show-users'), json=args, auth=True, lower=True)
                if len(res) == 0:
                    break
        else:
            for i in res:
                yield User(RawUser(i))
