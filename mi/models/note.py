from typing import Any, Dict, List, Optional

from mi.models.drive import RawFile
from mi.models.emoji import RawEmoji
from mi.models.poll import RawPoll
from mi.models.user import RawUser
from mi.types.note import Note, Reaction, Renote
from mi.utils import upper_to_lower


class RawRenote:
    def __init__(self, data: Renote):
        self.id: str = data["id"]
        self.created_at: str = data["created_at"]
        self.user_id: str = data["user_id"]
        self.user: RawUser = RawUser(data['user'])
        self.content: Optional[str] = data.get("text", None)
        self.cw: Optional[str] = data["cw"]
        self.visibility: str = data["visibility"]
        self.renote_count: int = data["renote_count"]
        self.replies_count: int = data["replies_count"]
        self.reactions = data["reactions"]
        self.emojis = data["emojis"]
        self.file_ids: List[str] = data["file_ids"]
        self.files = data["files"]
        self.reply_id = data["reply_id"]
        self.files = data["files"]
        self.reply_id = data["reply_id"]
        self.renote_id = data["renote_id"]
        self.uri = data.get("uri")
        self.poll: Optional[RawPoll] = RawPoll(data["poll"]) if data.get("poll") else None


class RawReaction:
    def __init__(self, data: Reaction):
        self.id: Optional[str] = data.get('id')
        self.created_at = data.get('created_at')
        self.type: Optional[str] = data.get('type')
        self.is_read: bool = bool(data.get('is_read'))
        self.user: Optional[RawUser] = RawUser(data['user']) if data.get('user') else None
        self.note: Optional[RawNote] = RawNote(data['note']) if data.get('note') else None
        self.reaction: str = data['reaction']


class RawNote:
    def __init__(self, data: Note):
        self.id: str = data["id"]
        self.created_at: str = data["created_at"]
        self.user_id: str = data["user_id"]
        self.author: RawUser = RawUser(data['user'])
        self.content: Optional[str] = data.get("text")
        self.cw: Optional[str] = data.get("cw")
        self.renote: Optional[RawRenote] = RawRenote(data['renote']) if data.get('renote') else None
        self.visibility: Optional[str] = data.get("visibility")  # This may be an optional
        self.renote_count: Optional[int] = data.get("renote_count")  # TODO: Optionalかどうか
        self.replies_count: Optional[int] = data.get("replies_count")  # TODO: Optionalかどうか
        self.reactions: Optional[Dict[str, Any]] = data["reactions"]  # TODO: Optionalかどうか
        self.emojis: List[RawEmoji] = [RawEmoji(i) for i in data["emojis"]]
        self.file_ids: Optional[List[str]] = data["file_ids"]
        self.files: List[RawFile] = [RawFile(upper_to_lower(i)) for i in data["files"]]
        self.reply_id: Optional[str] = data["reply_id"]
        self.renote_id: Optional[str] = data["renote_id"]
        self.poll: Optional[RawPoll] = RawPoll(data["poll"]) if data.get("poll") else None
        self.visible_user_ids: Optional[List[str]] = data.get("visible_user_ids", [])
        self.via_mobile: bool = bool(data.get("via_mobile", False))
        self.local_only: bool = bool(data.get("local_only", False))
        self.extract_mentions: bool = bool(data.get("extract_mentions"))
        self.extract_hashtags: bool = bool(data.get("extract_hashtags"))
        self.extract_emojis: bool = bool(data.get("extract_emojis"))
        self.preview: bool = bool(data.get("preview"))
        self.media_ids: Optional[List[str]] = data.get("media_ids")
        self.field: Optional[dict] = {}
        self.tags: Optional[List[str]] = data.get("tags", [])
        self.channel_id: Optional[str] = data.get("channel_id")
