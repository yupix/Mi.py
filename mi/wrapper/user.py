from mi import config
from mi.exception import NotSupportedError
from mi.framework.http import HTTPSession, Route
from mi.framework.models.user import User
from mi.wrapper import RawUser


class AdminUserManager:
    def __init__(self):
        pass

    @staticmethod
    async def create_account(username: str, password: str) -> User:
        if config.is_ayuskey:
            raise NotSupportedError("Ayuskeyではサポートされていません")
        data = {'username': username, 'password': password}
        res = await HTTPSession.request(Route('POST', '/api/admin/accounts/create'), json=data, auth=True, lower=True)
        return User(RawUser(res))

    @staticmethod
    async def delete_account(user_id: str) -> bool:
        data = {'userId': user_id}
        res = await HTTPSession.request(Route('POST', '/api/admin/accounts/delete'), json=data, auth=True, lower=True)
        return bool(res)
