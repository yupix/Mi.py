from typing import Any, Dict, List, Optional, TypedDict

from .user import Author
from .emoji import Emoji
from .drive import File


class Geo(TypedDict):
    """
    衛生情報
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
    id: Optional[str]
    created_at: Optional[str]
    user_id: Optional[str]
    user: Optional[Author]
    content: Optional[str]
    cw: Optional[str]
    visibility: Optional[str]
    renote_count: Optional[int]
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


class Note(TypedDict):
    """
    note object
    """

    id: str
    created_at: str
    user_id: str
    author: Author
    content: Optional[str]
    cw: Optional[str]
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
    no_extract_mentions: Optional[bool]
    no_extract_hashtags: Optional[bool]
    no_extract_emojis: Optional[bool]
    preview: Optional[bool]
    geo: Optional[Geo]
    media_ids: Optional[List[str]]
    renote: Optional[Renote]
    field: Optional[dict]
    tags: Optional[List[str]]
    channel_id: Optional[str]
