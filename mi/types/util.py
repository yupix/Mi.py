from __future__ import annotations

from typing import TYPE_CHECKING, Optional, TypedDict

if TYPE_CHECKING:
    from mi.framework.models.emoji import Emoji


class EmojiList(TypedDict):
    name: str
    count: Optional[int]
    object: Optional[Emoji]
