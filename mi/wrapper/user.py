"""Modules for the administrator's users"""

from typing import Optional

from mi import config
from mi.exception import NotSupportedError
from mi.framework.http import HTTPSession
from mi.framework.models.user import User
from mi.framework.router import Route
from mi.wrapper.models.user import RawUser


class AdminUserManager:
    def __init__(self, user_id: Optional[str] = None):
        self.__user_id = user_id

    @staticmethod
    async def create_account(username: str, password: str) -> User:
        """
        Create a new account.

        Parameters
        ----------
        username : str
            User's name
        password : str
            User's password

        Returns
        -------
        User
            Created user
        """

        if config.is_ayuskey:
            raise NotSupportedError("Ayuskeyではサポートされていません")
        data = {'username': username, 'password': password}
        res = await HTTPSession.request(Route('POST', '/api/admin/accounts/create'), json=data, auth=True, lower=True)
        return User(RawUser(res))

    async def delete_account(self, user_id: Optional[str] = None) -> bool:
        """
        Deletes the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be deleted
        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res = await HTTPSession.request(Route('POST', '/api/admin/accounts/delete'), json=data, auth=True, lower=True)
        return bool(res)

    async def show_user(self, user_id: Optional[str] = None) -> User:
        """
        Shows the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be shown

        Returns
        -------
        User
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await HTTPSession.request(Route('GET', '/api/admin/show-user'), json=data, auth=True, lower=True)
        return User(RawUser(res))

    async def suspend(self, user_id: Optional[str] = None) -> bool:
        """
        Suspends the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be suspended

        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await HTTPSession.request(Route('POST', '/api/admin/suspend-user'), json=data, auth=True, lower=True)
        return bool(res)

    async def unsuspend(self, user_id: Optional[str] = None) -> bool:
        """
        Unsuspends the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be unsuspended

        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await HTTPSession.request(Route('POST', '/api/admin/unsuspend-user'), json=data, auth=True, lower=True)
        return bool(res)
