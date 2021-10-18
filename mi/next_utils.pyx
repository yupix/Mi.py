import cython

@cython.boundscheck(False)
@cython.wraparound(False)
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
