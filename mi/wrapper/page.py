from typing import Optional

from mi.framework.http import HTTPSession
from mi.framework.router import Route


class PagesManager:
    @staticmethod
    async def get_pages(limit: int = 100, since_id: Optional[int] = None, until_id: Optional[int] = None):
        data = {
            'limit': limit,
            'since_id': since_id,
            'until_id': until_id
        }
        res = await HTTPSession.request(Route('POST', '/api/i/pages'), json=data, auth=True)
