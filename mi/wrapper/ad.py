from mi.framework.http import HTTPSession
from mi.framework.router import Route


class AdminAdvertisingManager:
    def __init__(self):
        pass

    @staticmethod
    async def create(url: str, memo: str, place: str, priority: str, ratio: str, expires_at: int, image_url: str):
        data = {
            'url': url,
            'memo': memo,
            'place': place,
            'priority': priority,
            'ratio': ratio,
            'expires_at': expires_at,
            'image_url': image_url
        }
        return await HTTPSession.request(Route('POST', '/api/ad/create'), json=data, auth=True, lower=True)
