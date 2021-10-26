from typing import List, Optional

from pydantic import BaseModel

from mi.utils import api, json_dump


class ChartAction:
    def get_active_users(self) -> "Chart":
        """
        Chartクラスをもとにアクティブなユーザーの統計を取得します

        Returns
        -------
        Chart: Chart
        """
        data = json_dump(
            {"span": self.span, "limit": self.limit, "offset": self.offset}
        )
        res = api("/api/charts/active-users", data=data).json()
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
