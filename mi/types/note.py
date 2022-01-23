from typing import Any, Dict, List, Optional, TypedDict

from .drive import File
from .emoji import Emoji
from .user import User


class Geo(TypedDict):
    """
    衛星情報
    """
    coordinates: Optional[List[Any]]
    altitude: Optional[int]
    accuracy: Optional[int]
    altitude_accuracy: Optional[int]
    heading: Optional[int]
    speed: Optional[int]


class Poll(TypedDict, total=False):
    """
    アンケート情報
    """

    multiple: bool
    expires_at: int
    choices: List[str]
    expired_after: int


class Renote(TypedDict):
    id: str
    created_at: str
    user_id: str
    user: User
    text: str
    cw: str
    visibility: str
    renote_count: int
    replies_count: Optional[int]
    reactions: Dict[str, Any]
    emojis: Optional[List]
    file_ids: Optional[List]
    files: Optional[List]
    reply_id: Optional[str]
    renote_id: Optional[str]
    uri: Optional[str]
    poll: Optional[Poll]
    tags: Optional[List[str]]
    channel_id: Optional[str]


class _NoteOptional(TypedDict, total=False):
    """
    ノートに必ず存在すると限らない物
    """
    text: str
    cw: str
    geo: Geo


class Note(_NoteOptional):
    """
    note object
    """

    id: str
    created_at: str
    user_id: str
    user: User
    visibility: Optional[str]
    renote_count: Optional[int]
    replies_count: Optional[int]
    reactions: Optional[Dict[str, Any]]
    emojis: List[Emoji]
    file_ids: Optional[List[str]]
    files: Optional[List[File]]
    reply_id: Optional[str]
    renote_id: Optional[str]
    poll: Optional[Poll]
    visible_user_ids: Optional[List[str]]
    via_mobile: Optional[bool]
    local_only: Optional[bool]
    extract_mentions: Optional[bool]
    extract_hashtags: Optional[bool]
    extract_emojis: Optional[bool]
    preview: Optional[bool]
    media_ids: Optional[List[str]]
    renote: Optional[Renote]
    field: Optional[dict]
    tags: Optional[List[str]]
    channel_id: Optional[str]


class OptionalReaction(TypedDict, total=False):
    created_at: str
    type: str
    is_read: bool
    user: User
    note: Note
    id: str


class Reaction(OptionalReaction):
    reaction: str
