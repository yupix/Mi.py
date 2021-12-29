"""
Mi.pyを使用する上でちょっとした際に便利なツール一覧
"""
import json
import logging
import re
from inspect import isawaitable
from typing import Any, Callable, Dict, Iterable, List, Optional, TypeVar

import emoji

from mi import config

T = TypeVar("T")


def deprecated_func(func):
    print('deprecated function:' + func.__name__)


def get_cache_key(func):
    async def decorator(self, *args, **kwargs):
        ordered_kwargs = sorted(kwargs.items())
        key = (
                (func.__module__ or "")
                + '.{0}'
                + f'{self}'
                + str(args)
                + str(ordered_kwargs)
        )
        return await func(self, *args, **kwargs, cache_key=key)

    return decorator


def key_builder(func, cls, *args, **kwargs):
    ordered_kwargs = sorted(kwargs.items())
    key = (
            (func.__module__ or "")
            + f'.{func.__name__}'
            + f'{cls}'
            + str(args)
            + str(ordered_kwargs)
    )
    return key


def get_module_logger(module_name):
    logger = logging.getLogger(module_name)
    log_level = logging.DEBUG if config.debug else logging.INFO
    logger.setLevel(log_level)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: '
            '%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def emoji_count(text: Optional[str] = None, emojis: Optional[List[str]] = None):
    """
    テキストの中にいくつのemojiが含まれているかをカウントします

    Parameters
    ----------
    text
    emojis
    """

    if emojis is None:
        emojis = []
    return len(emojis) if text is None else len(emojis) + emoji.emoji_count(
        text)


def check_multi_arg(*args: Any) -> bool:
    """
    複数の値を受け取り値が存在するかをboolで返します

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


def remove_list_empty(data: List[Any]) -> List[Any]:
    """
    Parameters
    ----------
    data: dict
        空のkeyを削除したいdict

    Returns
    -------
    Dict[str, Any]
        空のkeyがなくなったdict
    """
    return [k for k in data if k]


def remove_dict_empty(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parameters
    ----------
    data: dict
        空のkeyを削除したいdict

    Returns
    -------
    _data: dict
        空のkeyがなくなったdict
    """

    _data = {}
    _data = {k: v for k, v in data.items() if v is not None}
    _data = {k: v for k, v in data.items() if v}
    return _data


def upper_to_lower(
        data: Dict[str, Any], field: Optional[Dict[str, Any]] = None, nest: bool = True,
        replace_list: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Parameters
    ----------
    data: dict
        小文字にしたいkeyがあるdict
    field: dict, default=None
        謎
    nest: bool, default=True
        ネストされたdictのkeyも小文字にするか否か
    replace_list: dict, default=None
        dictのkey名を特定の物に置き換える

    Returns
    -------
    field : dict
        小文字になった, key名が変更されたdict
    """

    if data is None:
        return {}
    if replace_list is None:
        replace_list = {}

    if field is None:
        field = {}
    for attr in data:
        pattern = re.compile("[A-Z]")
        large = [i.group().lower() for i in pattern.finditer(attr)]
        result = [None] * (len(large + pattern.split(attr)))
        result[::2] = pattern.split(attr)
        result[1::2] = ["_" + i.lower() for i in large]
        default_key = "".join(result)
        if replace_list.get(attr):
            default_key = default_key.replace(attr, replace_list.get(attr))
        field[default_key] = data[attr]
        if type(field[default_key]) is dict and nest:
            field[default_key] = upper_to_lower(field[default_key])
    return field


def str_lower(text: str):
    pattern = re.compile("[A-Z]")
    large = [i.group().lower() for i in pattern.finditer(text)]
    result = [None] * (len(large + pattern.split(text)))
    result[::2] = pattern.split(text)
    result[1::2] = ["_" + i.lower() for i in large]
    return "".join(result)


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
    return "true" if boolean else "false"
