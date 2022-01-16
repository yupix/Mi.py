from typing import Any, Dict, List, Optional

from mi.models.drive import RawFile
from mi.models.emoji import RawEmoji
from mi.models.poll import RawPoll
from mi.models.user import RawUser
from mi.types.drive import File
from mi.types.emoji import Emoji
from mi.types.note import Note, Renote
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
        self.renote_count: int = data["renote_count"]
        self.replies_count: int = data["replies_count"]
        self.reactions: Dict[str, Any] = data["reactions"]
        self.emojis: List[Emoji] = [RawEmoji(i) for i in data["emojis"]]
        self.file_ids: Optional[List[str]] = data["file_ids"]
        self.files: List[File] = [RawFile(upper_to_lower(i)) for i in data["files"]]
        self.reply_id: Optional[str] = data["reply_id"]
        self.renote_id: Optional[str] = data["renote_id"]
        self.poll: Optional[RawPoll] = RawPoll(data["poll"]) if data.get("poll") else None
        self.visible_user_ids: Optional[List[str]] = data.get("visible_user_ids", [])
        self.via_mobile: Optional[bool] = data.get("via_mobile", False)
        self.local_only: bool = bool(data.get("local_only", False))
        self.no_extract_mentions: Optional[bool] = data.get("no_extract_mentions", False)
        self.no_extract_hashtags: Optional[bool] = data.get("no_extract_hashtags")
        self.no_extract_emojis: Optional[bool] = data.get("no_extract_emojis")
        self.preview: Optional[bool] = data.get("preview")
        self.media_ids: Optional[List[str]] = data.get("media_ids")
        self.field: Optional[dict] = {}
        self.tags: Optional[List[str]] = data.get("tags", [])
        self.channel_id: Optional[str] = data.get("channel_id")
