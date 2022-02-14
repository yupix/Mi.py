__all__ = []

from mi.framework.http import HTTPSession, Route
from mi.wrapper.models.chart import RawActiveUsersChart


class ChartManager:
    @staticmethod
    async def get_active_user(span: str = 'day', limit: int = 30, offset: int = 0) -> RawActiveUsersChart:
        data = {
            'span': span,
            'limit': limit,
            'offset': offset
        }
        data = await HTTPSession.request(Route('POST', '/api/charts/active-users'), json=data, auth=True, lower=True)
        return RawActiveUsersChart(data)
