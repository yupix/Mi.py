from pydantic import BaseModel
from typing import Any

i = None


def init(**kwargs):
    global i
    i = Config(**kwargs)


class Config(BaseModel):
    token: str
    origin_uri: str
    profile: Any
