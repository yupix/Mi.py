from __future__ import annotations

from typing import List, Optional

__all__ = ['Chart', 'Local', 'Remote']


class Local:
    def __init__(self, data):
        self.users: Optional[List[int]] = data['users']


class Remote:
    def __init__(self, data):
        self.users: Optional[List[int]] = data['users']


class Chart:
    def __init__(self, data):
        self.span: str = data['span']
        self.limit: int = data['limit']
        self.offset: int = data['offset']
        self.local: Local = Local(data['local'])
        self.remote: Remote = Remote(data['remote'])
