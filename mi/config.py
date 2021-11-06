from typing import Any, Optional


class Config:
    """
    Botを動作させる上でのConfig
    """

    def __init__(
            self,
            token: Optional[str],
            origin_uri: Optional[str],
            profile: Any = None,
            instance: dict = None,
    ):
        self.token: str = token
        self.origin_uri: str = origin_uri
        self.profile: Any = profile
        self.instance: dict = instance


i: Config = Config(token=None, origin_uri=None)
debug: bool = False
