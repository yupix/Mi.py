from typing import Any, Dict, List, Optional, TypedDict

from .drive import File
from .emoji import Emoji
from .instance import Instance


class Channel(TypedDict):
    id: Optional[str]
    createdAt: Optional[str]
    lastNotedAt: Optional[str]
    name: Optional[str]
    description: Optional[str]
    bannerUrl: Optional[str]
    notesCount: Optional[int]
    usersCount: Optional[int]
    isFollowing: Optional[bool]
    userId: Optional[str]


class PinnedPage(TypedDict):
    id: Optional[str]
    created_at: Optional[str]
    text: Optional[str]
    cw: Optional[str]
    user_id: Optional[str]
    user: Optional[Dict[str, Any]]
    reply_id: Optional[str]
    renote_id: Optional[str]
    reply: Optional[Dict[str, Any]]
    renote: Optional[Dict[str, Any]]
    via_mobile: Optional[bool]
    is_hidden: Optional[bool]
    visibility: Optional[str]
    mentions: Optional[List[str]]
    visible_user_ids: Optional[List[str]]
    file_ids: Optional[List[str]]
    files: Optional[List[File]]
    tags: Optional[List[str]]
    poll: Optional[Dict[str, Any]]
    channel_id: Optional[str]
    channel: Optional[Channel]
    local_only: Optional[bool]
    emojis: Optional[List[Emoji]]
    reactions: Optional[Dict[str, Any]]
    renote_count: Optional[int]
    replies_count: Optional[int]
    uri: Optional[str]
    url: Optional[str]
    my_reaction: Optional[Dict[str, Any]]


class Author(TypedDict):
    id: Optional[str]
    name: Optional[str]
    username: Optional[str]
    host: Optional[str]
    avatar_url: Optional[str]
    avatar_blurhash: Optional[str]
    avatar_color: Optional[str]
    is_admin: Optional[bool]
    is_bot: Optional[bool]
    is_cat: Optional[bool]
    is_lady: Optional[bool]
    emojis: Optional[List]
    online_status: Optional[str]
    instance: Optional[Instance]
