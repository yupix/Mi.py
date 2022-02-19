from __future__ import annotations
from typing import Optional, TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from mi.framework.models.emoji import Emoji


class EmojiList(TypedDict):
    name: str
    count: Optional[int]
    object: Optional[Emoji]
