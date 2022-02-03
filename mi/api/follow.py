from __future__ import annotations

import asyncio
from typing import List, Optional, TYPE_CHECKING

from mi.http import HTTPClient, Route
from mi.user import FollowRequest, User

if TYPE_CHECKING:
    from mi.state import ConnectionState

__all__ = ['FollowManager', 'FollowRequestManager']


class FollowManager:
    def __init__(self, client: ConnectionState, http: HTTPClient, loop: asyncio.AbstractEventLoop, *,
                 user_id: Optional[str] = None):
        self.__state: ConnectionState = client
        self.__http: 'HTTPClient' = http
        self.__loop: asyncio.AbstractEventLoop = loop
        self.__user_id: Optional[str] = user_id

    async def add(self, user_id: Optional[str] = None) -> tuple[bool, Optional[str]]:
        """
        ユーザーをフォローします

        Returns
        -------
        bool
            成功ならTrue, 失敗ならFalse
        str
            実行に失敗した際のエラーコード
        """

        user_id = user_id or self.__user_id

        data = {"userId": user_id}
        res = await self.__http.request(Route('POST', '/api/following/create'), json=data, auth=True, lower=True)
        if res.get("error"):
            code = res["error"]["code"]
            status = False
        else:
            code = None
            status = True
        return status, code

    async def remove(self, user_id: Optional[str] = None) -> bool:
        """
        ユーザーのフォローを解除します

        Returns
        -------
        bool
            成功ならTrue, 失敗ならFalse
        """

        user_id = user_id or self.__user_id

        data = {"userId": user_id}
        res = await self.__http.request(Route('POST', '/api/following/delete'), json=data, auth=True)
        return bool(res.status_code == 204 or 200)


class FollowRequestManager:
    def __init__(self, client: ConnectionState, http: HTTPClient, loop: asyncio.AbstractEventLoop, *,
                 user_id: Optional[str] = None):
        self.__state: ConnectionState = client
        self.__http: 'HTTPClient' = http
        self.__loop: asyncio.AbstractEventLoop = loop
        self.__user_id: Optional[str] = user_id

    async def get_all(self) -> List[FollowRequest]:
        """
        未承認のフォローリクエストを取得します
        """

        return [FollowRequest(i['follower'], state=self.__state) for i in
                await self.__http.request(Route('POST', '/api/following/requests/list'), auth=True, lower=True)]

    async def get_user(self, user_id: Optional[str] = None) -> User:
        """
        フォローリクエスト元のユーザーを取得します
        Parameters
        ----------
        user_id : Optional[str], default=None
            ユーザーID

        Returns
        -------
        User
            フォローリクエスト元のユーザー
        """

        user_id = user_id or self.__user_id

        return await self.__state.client.get_user(user_id)

    async def accept(self, user_id: Optional[str] = None) -> bool:
        """
        与えられたIDのユーザーのフォローリクエストを承認します
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        return bool(await self.__http.request(Route('POST', '/api/following/requests/accept'), json=data, auth=True))

    async def reject(self, user_id: Optional[str]) -> bool:
        """
        与えられたIDのユーザーのフォローリクエストを拒否します
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        return bool(await self.__http.request(Route('POST', '/api/following/requests/reject'), json=data, auth=True))
