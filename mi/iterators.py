from __future__ import annotations

from typing import Iterator, Optional, TYPE_CHECKING

from . import User
from .utils import api, remove_dict_empty

if TYPE_CHECKING:
    from . import ConnectionState


class InstanceIterator:
    def __init__(self, state: ConnectionState):
        self._state = state

    def get_users(self, limit: int = 10,
                  *,
                  offset: int = 0,
                  sort: Optional[str] = None,
                  state: str = 'all',
                  origin: str = 'local',
                  username: Optional[str] = None,
                  hostname: Optional[str] = None,
                  get_all: bool = False
                  ) -> Iterator[User]:
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
        res = api('/api/admin/show-users', json_data=args, auth=True).json()

        if get_all:
            while True:
                for i in res:
                    yield User(i, self._state)
                args['offset'] = args['offset'] + len(res)
                res = api('/api/admin/show-users',
                          json_data=args, auth=True).json()
                if len(res) == 0:
                    break
        else:
            for i in res:
                yield User(i, self._state)
