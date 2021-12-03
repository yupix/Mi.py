from __future__ import annotations
from typing import Any, Dict, Iterator, Optional, TYPE_CHECKING, Union

from .types.instance import Instance as InstancePayload
from .utils import remove_dict_empty, api

if TYPE_CHECKING:
    from .user import User

class Instance:
    def __init__(self, data: Union[Dict[Any, Any], InstancePayload]):
        self.host: Optional[str] = data.get("host")
        self.name: Optional[str] = data.get("name")
        self.software_name: Optional[str] = data.get("software_name")
        self.software_version: Optional[str] = data.get("software_version")
        self.icon_url: Optional[str] = data.get("icon_url")
        self.favicon_url: Optional[str] = data.get("favicon_url")
        self.theme_color: Optional[str] = data.get("theme_color")

    @staticmethod
    def get_users(limit: int = 10,
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
                    yield i
                args['offset'] = args['offset'] + len(res)
                res = api('/api/admin/show-users',
                          json_data=args, auth=True).json()
                if len(res) == 0:
                    break
        else:
            for i in res:
                yield i
