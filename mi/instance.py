from __future__ import annotations

from typing import Iterator, Optional, TYPE_CHECKING

from .types.instance import Instance as InstancePayload

if TYPE_CHECKING:
    from .user import User
    from . import ConnectionState


class Instance:
    def __init__(self, data: InstancePayload, state: ConnectionState):
        """
        インスタンス情報
        
        Parameters
        ----------
        data : InstancePayload
            インスタンス情報の入った dict
        state: ConnectionState
            botのコネクション
        """

        self.host: Optional[str] = data.get("host")
        self.name: Optional[str] = data.get("name")
        self.software_name: Optional[str] = data.get("software_name")
        self.software_version: Optional[str] = data.get("software_version")
        self.icon_url: Optional[str] = data.get("icon_url")
        self.favicon_url: Optional[str] = data.get("favicon_url")
        self.theme_color: Optional[str] = data.get("theme_color")
        self._state = state

    def get_users(self,
                  limit: int = 10,
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
        return self._state.get_users(limit=limit, offset=offset, sort=sort, state=state, origin=origin, username=username,
                                     hostname=hostname, get_all=get_all)
