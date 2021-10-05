"""
Mi.pyを使用する上でちょっとした際に便利なツール一覧
"""
import json
import re
from inspect import isawaitable
from typing import Any, Callable, Iterable, Optional, TypeVar

import requests

from mi import config, exception

T = TypeVar('T')


def check_multi_arg(*args) -> bool:
    """複数の値を受け取り値が存在するかをboolで返します

    Parameters
    ----------
    args : list
        確認したい変数のリスト

    Returns
    -------
    bool
        存在する場合はTrue, 存在しない場合はFalse
    """
    return bool([i for i in args if i])


async def async_all(gen, *, check=isawaitable):
    for elem in gen:
        if check(elem):
            elem = await elem
        if not elem:
            return False
    return True


def find(predicate: Callable[[T], Any], seq: Iterable[T]) -> Optional[T]:
    """A helper to return the first element found in the sequence
    that meets the predicate. For example: ::

        member = discord.utils.find(lambda m: m.name == 'Mighty', channel.guild.members)

    would find the first :class:`~discord.Member` whose name is 'Mighty' and return it.
    If an entry is not found, then ``None`` is returned.

    This is different from :func:`py:filter` due to the fact it stops the moment it finds
    a valid entry.

    Parameters
    -----------
    predicate
        A function that returns a boolean-like result.
    seq: :class:`collections.abc.Iterable`
        The iterable to search through.
    """

    for element in seq:
        if predicate(element):
            return element
    return None


def json_dump(data, *args, **kwargs):
    return json.dumps(data, ensure_ascii=False, *args, **kwargs)


def api(
        endpoint: str,
        *,
        origin_uri: str = None,
        data=None,
        json_data=None,
        files: dict = None,
        auth: bool = False
) -> requests.models.Response:
    """
    .. deprecated:: 0.1.5
        `data` 0.2.0で正式に削除され、以降はjson_dataを使用するようにしてください。

    Parameters
    ----------
    origin_uri : str
        起点となるURL
    endpoint : str
        エンドポイント
    data : dict or str
        送るデータ
    json_data : dict
        dict形式のデータ
    auth: bool
        認証情報を付与するか
    files :
        画像などのファイル

    Returns
    -------
    requests.models.Response
    """

    if type(data) is str:
        data = data.encode('utf-8')
    if check_multi_arg(data, json_data, files) is False and auth:
        json_data = {}
    if auth:
        json_data['i'] = config.i.token
    base_url = origin_uri or config.i.origin_uri
    res = requests.post(base_url + endpoint, data=data, files=files, json=json_data)
    print(res.text)
    status_code = res.status_code
    errors = {
        400: {
            'raise': exception.ClientError,
            'description': 'Client Error'
        },
        401: {
            'raise': exception.AuthenticationError,
            'description': 'AuthenticationError'
        },
        418: {
            'raise': exception.ImAi,
            'description': 'I\'m Ai'
        },
        500: {
            'raise': exception.InternalServerError,
            'description': 'InternalServerError'
        }
    }
    if status_code in [400, 401, 418, 500]:
        error_base = errors.get(status_code)
        error = error_base['raise'](error_base['description'] + '\n' + res.text)
        raise error
    return res


def remove_dict_empty(data: dict) -> dict:
    _data = {}
    _data = {k: v for k, v in data.items() if v is not None}
    return _data


def upper_to_lower(data: dict, field: dict = None, nest=True, replace_list: dict = None) -> dict:
    if data is None:
        return {}
    if replace_list is None:
        replace_list = {}

    pattern = re.compile('[A-Z]')
    if field is None:
        field = {}
    for attr in data:
        pattern = re.compile('[A-Z]')
        large = [i.group().lower() for i in pattern.finditer(attr)]
        result = [None] * (len(large + pattern.split(attr)))
        result[::2] = pattern.split(attr)
        result[1::2] = ['_' + i.lower() for i in large]
        default_key = "".join(result)
        if replace_list.get(attr):
            default_key = default_key.replace(attr, replace_list.get(attr))
        field[default_key] = data[attr]
        if type(field[default_key]) is dict and nest is True:
            field[default_key] = upper_to_lower(field[default_key])
    return field


def bool_to_string(boolean: bool) -> str:
    """
    boolを小文字にして文字列として返します

    Parameters
    ----------
    boolean : bool
        変更したいbool値
    Returns
    -------
    true or false: str
        小文字になったbool文字列
    """

    return 'true' if boolean else 'false'
