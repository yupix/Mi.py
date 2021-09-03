"""
Mi.pyを使用する上でちょっとした際に便利なツール一覧
"""
import re


def upper_to_lower(data: dict, field: dict = None):
    if data is None:
        return {}
    replace_list: dict = {'user': 'author', 'id': 'id_'}
    p = re.compile('[A-Z]')
    if field is None:
        field = {}
    for attr in data:
        default_key = ("_" + p.search(attr)[0].lower()).join(p.split(attr)) if p.search(attr) is not None else attr
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
