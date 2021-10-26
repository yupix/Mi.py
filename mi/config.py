from typing import Any

from pydantic import BaseModel

i = None


def init(**kwargs):
    global i
    i = Config(**kwargs)


class Config(BaseModel):
    token: str
    origin_uri: str
    profile: Any
