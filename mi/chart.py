import json
from typing import List, Optional

from pydantic import BaseModel

from mi import config
from mi.utils import api, json_dump


class ChartAction:
    def get_active_users(self):
        data = json_dump({'span': self.span, 'limit': self.limit, 'offset': self.offset})
        res = api(config.i.origin_uri, '/api/charts/active-users', data).json()
        return Chart(**res)


class Local(BaseModel):
    users: Optional[List[int]] = None


class Remote(BaseModel):
    users: Optional[List[int]] = None


class Chart(BaseModel, ChartAction):
    span: Optional[str] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    local: Optional[Local] = None
    remote: Optional[Remote] = None
