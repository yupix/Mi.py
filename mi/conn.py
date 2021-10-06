import typing

from mi.exception import InvalidParameters, NotExistRequiredParameters
from mi.utils import api, check_multi_arg, remove_dict_empty


def get_user(user_id: str = None, username: str = None, host: str = None) -> dict:
    """
    ユーザーのプロフィールを返します

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

    data = remove_dict_empty({'userId': user_id, 'username': username, 'host': host})
    return api('/api/users/show', json_data=data, auth=True).json()


def get_followers(user_id: str = None,
                  username: str = None,
                  host: str = None,
                  since_id: str = None,
                  until_id: str = None,
                  limit: int = 10,
                  get_all: bool = False) -> typing.Iterator[dict]:
    """
    与えられたユーザーのフォロワーを取得します

    Parameters
    ----------
    user_id : str, default=None
        ユーザーのid
    username : str, default=None
        ユーザー名
    host : str, default=None
        ユーザーがいるインスタンスのhost名
    since_id : str, default=None
    until_id : str, default=None
        前回の最後の値を与える(既に実行し取得しきれない場合に使用)
    limit : int, default=10
        取得する情報の最大数 max: 100
    get_all : bool, default=False
        全てのフォロワーを取得する

    Yields
    ------
    dict
        フォロワーの情報

    Raises
    ------
    InvalidParameters
        limit引数が不正な場合
    """
    if not check_multi_arg(user_id, username):
        raise NotExistRequiredParameters('user_id, usernameどちらかは必須です')

    if limit > 100:
        raise InvalidParameters('limit は100以上を受け付けません')

    data = remove_dict_empty(
        {'userId': user_id, 'username': username, 'host': host, 'sinceId': since_id, 'untilId': until_id, 'limit': limit})
    if get_all:
        loop = True
        while loop:
            get_data = api('/api/users/followers', json_data=data, auth=True).json()
            if len(get_data) > 0:
                data['untilId'] = get_data[-1]['id']
            else:
                break
            yield get_data
    else:
        get_data = api('/api/users/followers', json_data=data, auth=True).json()
        yield get_data
