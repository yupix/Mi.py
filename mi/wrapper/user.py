from typing import Optional

from mi import config
from mi.exception import NotSupportedError
from mi.framework.http import HTTPSession, Route
from mi.framework.models.user import User
from mi.wrapper import RawUser


class AdminUserManager:
    def __init__(self, user_id: Optional[str] = None):
        self.__user_id = user_id

    @staticmethod
    async def create_account(username: str, password: str) -> User:
        if config.is_ayuskey:
            raise NotSupportedError("Ayuskeyではサポートされていません")
        data = {'username': username, 'password': password}
        res = await HTTPSession.request(Route('POST', '/api/admin/accounts/create'), json=data, auth=True, lower=True)
        return User(RawUser(res))

    async def delete_account(self, user_id: Optional[str] = None) -> bool:
        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res = await HTTPSession.request(Route('POST', '/api/admin/accounts/delete'), json=data, auth=True, lower=True)
        return bool(res)

    async def show(self, user_id: Optional[str] = None) -> User:
        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await HTTPSession.request(Route('GET', '/api/admin/show-user'), json=data, auth=True, lower=True)
        return User(RawUser(res))

    async def suspend(self, user_id: Optional[str] = None) -> bool:
        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await HTTPSession.request(Route('POST', '/api/admin/suspend-user'), json=data, auth=True, lower=True)
        return bool(res)

    async def unsuspend(self, user_id: Optional[str] = None) -> bool:
        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await HTTPSession.request(Route('POST', '/api/admin/unsuspend-user'), json=data, auth=True, lower=True)
        return bool(res)
