"""
Mi.pyを使用する上でちょっとした際に便利なツール一覧
"""
import re


def set_auth_i(cls, auth_i: dict, exist: bool = False):
    if not exist and not auth_i:
        return
    cls.token = auth_i.get('token')
    cls.origin_uri = auth_i.get('origin_uri')


def upper_to_lower(data: dict, field: dict = None):
    if data is None:
        return {}
    replace_list: dict = {'user': 'author', 'id': 'id_'}
    p = re.compile('[A-Z]')
    if field is None:
        field = {}
    for attr in data:
        p = re.compile('[A-Z]')
        large = [i.group().lower() for i in p.finditer(attr)]
        result = [None] * (len(large + p.split(attr)))
        result[::2] = p.split(attr)
        result[1::2] = ['_' + i.lower() for i in large]
        default_key = "".join(result)
        if replace_list.get(attr):
            default_key = default_key.replace(attr, replace_list.get(attr))

        field[default_key] = data[attr]
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
