import typing

from mi import config
from mi.exception import InvalidParameters, NotExistRequiredParameters
from mi.utils import api, check_multi_arg, remove_dict_empty


def get_user(user_id: str = None, username: str = None, host: str = None) -> dict:
    """
    Parameters
    ----------
    user_id : str
        取得したいユーザーのユーザーID
    username : str
        取得したいユーザーのユーザー名
    host : str, default=None
        取得したいユーザーがいるインスタンスのhost

    Returns
    -------
    dict:
        ユーザー情報
    """
    if not check_multi_arg(user_id, username):
        raise NotExistRequiredParameters('user_id, usernameどちらかは必須です')

    data = {'userId': user_id, 'username': username, 'host': host}
    return api(config.i.origin_uri, '/api/users/show', json_data=data).json()
