from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from mi import Emoji, utils
from mi.exception import NotExistRequiredParameters
from mi.user import User
from mi.utils import check_multi_arg
from .abc.note import AbstractNote
from .types.note import (Note as NotePayload,
                         Poll as PollPayload,
                         Renote as RenotePayload,
                         Reaction as ReactionPayload
                         )

if TYPE_CHECKING:
    from mi import ConnectionState

__all__ = ['Note', 'Poll', 'Reaction']


class Follow:
    def __init__(self, data, state: ConnectionState):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[str] = data.get('created_at')
        self.type: Optional[str] = data.get('type')
        self.user: Optional[User] = data.get('user')
        self._state = state

    def follow(self, user_id: Optional[str] = None) -> tuple[bool, Optional[str]]:
        """
        与えられたIDのユーザーをフォローします

        Parameters
        ----------
        user_id : Optional[str] = None
            フォローしたいユーザーのID

        Returns
        -------
        bool = False
            成功ならTrue, 失敗ならFalse
        str
            実行に失敗した際のエラーコード
        """
        if check_multi_arg(user_id, self.user.id):
            raise NotExistRequiredParameters("user_idが存在しません")

        if user_id is None:
            user_id = self.user.id

        return self._state.follow_user(user_id)

    def unfollow(self, user_id: Optional[str] = None) -> bool:
        """
        与えられたIDのユーザーのフォローを解除します

        Parameters
        ----------
        user_id : Optional[str] = None
            フォローを解除したいユーザーのID

        Returns
        -------
        status: bool = False
            成功ならTrue, 失敗ならFalse
        """
        if user_id is None:
            user_id = self.user.id
        return self._state.unfollow_user(user_id)


class Header:
    def __init__(self, data, state: ConnectionState):
        self.id = data.get("id")
        self.type = data.get("type")
        self._state = state


class Properties:
    def __init__(self, data, state: ConnectionState) -> None:
        self.width: Optional[int] = data['width']
        self.height: Optional[int] = data['height']
        self.state: ConnectionState = state


class File:
    def __init__(self, data, state: ConnectionState):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[str] = data.get('create_at')
        self.name: Optional[str] = data.get('name')
        self.type: Optional[str] = data.get('type')
        self.md5: Optional[str] = data.get('md5')
        self.size: Optional[int] = data.get('size')
        self.is_sensitive: Optional[bool] = bool(data.get('is_sensitive'))
        self.blurhash: Optional[str] = data.get('blurhash')
        self.properties: Optional[Properties] = Properties(
            data.get('properties'), state=state) if data.get('properties') else None
        self.url: Optional[str] = data.get('url')
        self.thumbnail_url: Optional[str] = data.get('thumbnail_url')
        self.comment: Optional[str] = data.get('comment')
        self.folder_id: Optional[str] = data.get('folder_id')
        self.folder: Optional[str] = data.get('folder')
        self.user_id: Optional[str] = data.get('user_id')
        self.user: Optional[str] = data.get('user')


class Poll:
    def __init__(self, data: PollPayload):
        self.multiple: Optional[bool] = data.get("multiple")
        self.expires_at: Optional[int] = data.get("expires_at")
        self.choices: Optional[List[str]] = data.get("choices")
        self.expired_after: Optional[int] = data.get("expired_after")


class Renote(AbstractNote):
    def __init__(self, data: RenotePayload, state: ConnectionState):
        self.id: str = data["id"]
        self.created_at = data["created_at"]
        self.user_id = data["user_id"]
        self.user = User(data.get("user", {}), state=state)
        self.content: Optional[str] = data.get("text", None)
        self.cw = data["cw"]
        self.visibility = data["visibility"]
        self.renote_count = data["renote_count"]
        self.replies_count = data["replies_count"]
        self.reactions = data["reactions"]
        self.emojis = data["emojis"]
        self.file_ids: List[str] = data["file_ids"]
        self.files = data["files"]
        self.reply_id = data["reply_id"]
        self.files = data["files"]
        self.reply_id = data["reply_id"]
        self.renote_id = data["renote_id"]
        self.uri = data.get("uri")
        self.poll = Poll(data["poll"]) if data.get("poll") else None
        self._state = state

    def emoji_count(self) -> int:
        """
        ノートの本文にemojiが何個含まれているかを返します

        Returns
        -------
        int
            含まれている絵文字の数
        """
        return utils.emoji_count(self.content)

    async def delete(self) -> bool:
        return await self._state.delete_note(self.id)


class Reaction:
    def __init__(self, data: ReactionPayload, state: ConnectionState):
        self.id: Optional[str] = data.get('id')
        self.created_at = data.get('created_at')
        self.type: Optional[str] = data.get('type')
        self.is_read: bool = bool(data.get('is_read'))
        self.user: Optional[User] = User(data['user'], state=state) if data.get('user') else None
        self.note: Optional[Note] = Note(data['note'], state=state) if data.get('note') else None
        self.reaction: str = data['reaction']
        self._state: ConnectionState = state


class Note(AbstractNote):
    """
    Attributes
    -----------
    id: str 
    created_at: str
    user_id: str
    author: User
    content: Optional[str]
    cw: Optional[str]
    renote: Renote
    visibility: str
    renote_count: int
    replies_count:int
    reactions:Dict[str, Any]
    emojis:List[Emoji]
    file_ids:Optional[List[str]]
    files: Optional[List[str]]
    reply_id: Optional[str]
    renote_id: Optional[str]
    poll: Optional[Poll]
    """

    def __init__(self, data: NotePayload, state: ConnectionState):
        self.id: str = data["id"]
        self.created_at: str = data["created_at"]
        self.user_id: str = data["user_id"]
        self.author: User = User(data["user"], state)
        self.content: Optional[str] = data.get("text")
        self.cw: Optional[str] = data.get("cw")
        self.renote: Optional[Renote] = Renote(data['renote'], state=state) if data.get('renote') else None
        self.visibility: str = data["visibility"]
        self.renote_count: int = data["renote_count"]
        self.replies_count: int = data["replies_count"]
        self.reactions: Dict[str, Any] = data["reactions"]
        self.emojis: List[Emoji] = [Emoji(i, state=state) for i in data["emojis"]]
        self.file_ids: Optional[List[str]] = data["file_ids"]
        self.files: List[File] = [File(i, state=state) for i in data["files"]]
        self.reply_id: Optional[str] = data["reply_id"]
        self.renote_id: Optional[str] = data["renote_id"]
        self.poll: Optional[Poll] = Poll(data["poll"]) if data.get("poll") else None
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
        self._state = state

    async def reply(
            self, content: str,
            *,
            cw: Optional[str] = None,
            no_extract_mentions: bool = False,
            no_extract_hashtags: bool = False,
            no_extract_emojis: bool = False,
            renote_id: Optional[str] = None,
            channel_id: Optional[str] = None,
            file_ids=None,
            poll: Optional[Poll] = None
    ) -> Note:
        if file_ids is None:
            file_ids = []
        return await self._state.post_note(
            content,
            visibility=self.visibility,
            visible_user_ids=self.visible_user_ids,
            cw=cw,
            local_only=self.local_only,
            no_extract_mentions=no_extract_mentions,
            no_extract_hashtags=no_extract_hashtags,
            no_extract_emojis=no_extract_emojis,
            reply_id=self.id,
            renote_id=renote_id,
            channel_id=channel_id,
            file_ids=file_ids,
            poll=poll
        )


    def emoji_count(self) -> int:
        """
        ノートの本文にemojiが何個含まれているかを返します

        Returns
        -------
        int
            含まれている絵文字の数
        """

        return utils.emoji_count(self.content)

    async def delete(self) -> bool:
        """
        指定したIDのノートを削除します

        Returns
        -------
        is_success: bool
            成功したか否か
        status_code: int
            HTTP レスポンスステータスコード
        """

        return await self._state.delete_note(self.id)
