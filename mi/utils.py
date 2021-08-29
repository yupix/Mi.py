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
