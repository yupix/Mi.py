"""
Mi.pyを使用する上でちょっとした際に便利なツール一覧
"""
import json
import re

import requests


def json_dump(data, *args, **kwargs):
    return json.dumps(data, ensure_ascii=False, *args, **kwargs)


def api(origin_uri: str, endpoint: str, data=None, json_data=None, files: dict = None) -> requests.models.Response:
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
    json_data :
    files :

    Returns
    -------
    requests.models.Response
    """

    if type(data) is str:
        data = data.encode('utf-8')

    return requests.post(origin_uri + endpoint, data=data, files=files, json=json_data)


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
