from typing import List, Optional

from pydantic import BaseModel

from mi.utils import api, json_dump

__all__ = ['Chart', 'Local', 'Remote']


class Local(BaseModel):
    users: Optional[List[int]] = None


class Remote(BaseModel):
    users: Optional[List[int]] = None


class Chart(BaseModel):
    span: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    local: Optional[Local] = None
    remote: Optional[Remote] = None
