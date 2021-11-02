from typing import Any

i = None


def init(**kwargs):
    global i
    i = Config(**kwargs)


class Config:
    """
    Botを動作させる上でのConfig
    """

    def __init__(self, token: str, origin_uri: str, profile: Any = None, instance: Any = None):
        self.token: str = token
        self.origin_uri: str = origin_uri
        self.profile: Any = profile
        self.instance: Any = instance
