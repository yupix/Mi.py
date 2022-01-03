from __future__ import annotations
import asyncio

from typing import TYPE_CHECKING

from mi.http import HTTPClient, Route

if TYPE_CHECKING:
    from mi.state import ConnectionState

class FollowManager:
    def __init__(self, client: ConnectionState, http: HTTPClient, loop: asyncio.AbstractEventLoop):
        self.client:'ConnectionState' = client
        self.http:'HTTPClient' = http
        self.loop: asyncio.AbstractEventLoop = loop
    
    async def accept(self, user_id: str) -> bool:
        data = {'userId': user_id}
        return bool(await self.http.request(Route('POST', '/api/following/requests/accept'), json=data, auth=True))

    async def reject(self, user_id: str) -> bool:
        data = {'userId': user_id}
        return bool(await self.http.request(Route('POST', '/api/following/requests/reject'), json=data, auth=True))