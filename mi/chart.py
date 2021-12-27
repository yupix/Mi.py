from typing import List, Optional

from mi.state import ConnectionState

__all__ = ['Chart', 'Local', 'Remote']


class Local:
    def __init__(self, data, state: ConnectionState):
        self.users: Optional[List[int]] = data['users']
        self._state = state


class Remote:
    def __init__(self, data, state: ConnectionState):
        self.users: Optional[List[int]] = data['users']
        self._state = state


class Chart:
    def __init__(self, data, state: ConnectionState):
        self.span: str = data['span']
        self.limit: int = data['limit']
        self.offset: int = data['offset']
        self.local: Local = Local(data['local'], state=state)
        self.remote: Remote = Remote(data['remote'], state=state)
        self._state = state
