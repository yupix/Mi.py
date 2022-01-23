from __future__ import annotations

import asyncio
from typing import Optional, TYPE_CHECKING

from mi.api.chat import ChatManager
from mi.api.follow import FollowManager, FollowRequestManager

if TYPE_CHECKING:
    from mi.state import ConnectionState
    from mi.http import HTTPClient

__all__ = ['UserActions']


class UserActions:
    def __init__(
            self, client: 'ConnectionState',
            http: HTTPClient,
            loop: asyncio.AbstractEventLoop,
            *,
            user_id: Optional[str] = None
    ):
        self.client = client
        self.http = http
        self.loop = loop
        self.follow: FollowManager = FollowManager(client, http, loop, user_id=user_id)
        self.follow_request: FollowRequestManager = FollowRequestManager(client, http, loop, user_id=user_id)
        self.chat: ChatManager = ChatManager(client, http, loop, user_id=user_id)

    def get_follow(self, user_id: str) -> FollowManager:
        return FollowManager(self.client, self.http, self.loop, user_id=user_id)

    def get_follow_request(self, user_id: str) -> FollowRequestManager:
        return FollowRequestManager(self.client, self.http, self.loop, user_id=user_id)
