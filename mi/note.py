from __future__ import annotations
import json
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from pydantic import BaseModel, Field

from mi import Emoji, User, utils
from mi.exception import ContentRequired, NotExistRequiredParameters
from mi.user import User
from mi.utils import api, check_multi_arg, remove_dict_empty, upper_to_lower
from .abc.note import AbstractNote
from .types.note import (Note as NotePayload,
                         Poll as PollPayload,
                         Renote as RenotePayload)

if TYPE_CHECKING:
    from mi import ConnectionState

__all__ = ['Note']


class NoteAction:

    @staticmethod
    async def send(
            *,
            visibility: str,
            visible_user_ids: str,
            text: str,
            cw: str,
            via_mobile: bool,
            local_only: bool,
            no_extract_mentions: bool,
            no_extract_hashtags: bool,
            no_extract_emojis: bool,
            reply_id: str,
            renote_id: str,
            channel_id: str,
            preview: bool,
            geo: Any,
            file_ids: List[str],
            poll: Dict[str, Any]  # TODO:ここはもうちょい正確に type hint 定義したい
    ) -> "Note":
        """
        既にあるnoteクラスを元にnoteを送信します

        Returns
        -------
        msg: Note
        """
        field = {
            "visibility": visibility,
            "visibleUserIds": visible_user_ids,
            "text": text,
            "cw": cw,
            "viaMobile": via_mobile,
            "localOnly": local_only,
            "noExtractMentions": no_extract_mentions,
            "noExtractHashtags": no_extract_hashtags,
            "noExtractEmojis": no_extract_emojis,
            "replyId": reply_id,
            "renoteId": renote_id,
            "channelId": channel_id,
            "preview": preview,
            "geo": geo,
        }
        # field.update(other_field)
        if poll and len(poll["choices"]) > 0:
            field["poll"] = poll
        if file_ids:
            field["fileIds"] = file_ids
        field = remove_dict_empty(field)
        res = api("/api/notes/create", json_data=field, auth=True)
        res_json = res.json()
        if (
                res_json.get("error")
                and res_json.get("error", {}).get("code") == "CONTENT_REQUIRED"
        ):
            raise ContentRequired(
                "ノートの送信にはtext, file, renote またはpollのいずれか1つが無くてはいけません")
        return Note(res_json)


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


class Properties(BaseModel):
    width: Optional[int]
    height: Optional[int]


class File(BaseModel):
    id: Optional[str] = Field(None, alias="id_")
    created_at: Optional[str] = Field(None, alias="created_at")
    name: Optional[str] = None
    type: Optional[str] = None
    md5: Optional[str] = None
    size: Optional[int]
    is_sensitive: Optional[bool] = False
    blurhash: Optional[str] = None
    properties: Properties
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    comment: Optional[str] = None
    folder_id: Optional[str] = None
    folder: Optional[str] = None
    user_id: Optional[str] = None
    user: Optional[str] = None


class Poll:
    def __init__(self, data: PollPayload):
        self.multiple: Optional[bool] = data.get("multiple")
        self.expires_at: Optional[int] = data.get("expires_at")
        self.choices: Optional[List[str]] = data.get("choices")
        self.expired_after: Optional[int] = data.get("expired_after")


class Renote(AbstractNote):
    def __init__(self, data: RenotePayload, state: ConnectionState):
        self.id = data["id"]
        self.created_at = data["created_at"]
        self.user_id = data["user_id"]
        self.user = User(data.get("user", {}), state)
        self.content: Optional[str] = data.get("content", None)
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
        self.__note_action = NoteAction
        self._state = state

    def add_file(
            self,
            path: Optional[str] = None,
            name: Optional[str] = None,
            force: bool = False,
            is_sensitive: bool = False,
            url: Optional[str] = None,
    ):
        self.file_ids.append(
            self.__note_action.add_file(
                path, name=name, force=force, is_sensitive=is_sensitive,
                url=url
            ).id
        )
        return self

    def emoji_count(self) -> int:
        """
        ノートの本文にemojiが何個含まれているかを返します

        Returns
        -------
        int
            含まれている絵文字の数
        """
        return utils.emoji_count(self.content)

    async def delete(self, note_id: str = None) -> bool:
        """
        指定したIDのノートを削除します

        Parameters
        ----------
        note_id: str
            削除するノートのid

        returns
        -------
        bool
            成功したか否か
        """

        if note_id is None:
            note_id = self.id
        return await self.__note_action.delete(note_id)


class ReactionContent:
    def __init__(self, data):
        self.created_at = data.get('created_at')
        self.type = data.get('type')
        self.is_read: bool = data['is_read']
        self.user: User = User(data['user'])
        self.note: Note = Note(data['note'])
        self.reaction = data['reaction']


class Reaction(BaseModel):
    id: Optional[str] = Field(None, alias="id_")
    reaction: Optional[str] = None
    user_id: Optional[str] = None


class Note(AbstractNote):
    """
    Attributes
    -----------
    id: str 
    created_at: str
    user_id: str
    author: User
    content: Optiona[str]
    cw: Optional[str]
    renote: Renote
    visibility: str
    renote_count: int
    replies_count:int
    reactions:Dict[str, Any]
    emojis:List[Emoji]
    file_ids:Optional[List[str]]
    files: Optiona[List[str]]
    reply_id: Optional[str]
    renote_id: Optional[str]
    poll: Optional[Poll]
    """

    def __init__(self, data: NotePayload, state: ConnectionState):
        self.id: str = data["id"]
        self.created_at: str = data["created_at"]
        self.user_id: str = data["user_id"]
        self.author = User(data["user"], state)  #TODO: (Serarch) 自分自身が投稿したらNoneかも
        self.content: Optional[str] = data.get("text")
        self.cw: Optional[str] = data["cw"]
        self.renote: Renote = Renote(data["renote"], state) if data.get(
            "renote") else None
        self.visibility: str = data["visibility"]
        self.renote_count: int = data["renote_count"]
        self.replies_count: int = data["replies_count"]
        self.reactions: Dict[str, Any] = data["reactions"]
        self.emojis: List[Emoji] = data["emojis"]
        self.file_ids: Optional[List[str]] = data["file_ids"]
        self.files: Optional[List[File]] = data["files"]
        self.reply_id: Optional[str] = data["reply_id"]
        self.renote_id: Optional[str] = data["renote_id"]
        self.poll: Optional[Poll] = Poll(data["poll"]) if data.get(
            "poll") else None
        self.visible_user_ids: Optional[List[str]] = data.get(
            "visible_user_ids", [])
        self.via_mobile: Optional[bool] = data.get("via_mobile", False)
        self.local_only: Optional[bool] = data.get("local_only", False)
        self.no_extract_mentions: Optional[bool] = data.get(
            "no_extract_mentions", False
        )
        self.no_extract_hashtags: Optional[bool] = data.get(
            "no_extract_hashtags")
        self.no_extract_emojis: Optional[bool] = data.get("no_extract_emojis")
        self.preview: Optional[bool] = data.get("preview")
        self.media_ids: Optional[List[str]] = data.get("media_ids")
        self.field: Optional[dict] = {}
        self.tags: Optional[List[str]] = data.get("tags", [])
        self.channel_id: Optional[str] = data.get("channel_id")
        self._state = state
        self.__note_action = NoteAction

    def __poll_formatter(self) -> dict:
        if self.poll:
            poll = json.loads(self.poll.json(ensure_ascii=False))
            poll["expiresAt"] = poll.pop("expired_after")
            poll["expiredAfter"] = poll.pop("expires_at")
            if poll["expiredAfter"] is None:
                poll.pop("expiredAfter")
        else:
            poll = None
        return poll

    async def send(self) -> "Note":
        poll = self.__poll_formatter()
        return await self.__note_action.send(
            visibility=self.visibility,
            visible_user_ids=self.visible_user_ids,
            text=self.content,
            cw=self.cw,
            via_mobile=self.via_mobile,
            local_only=self.local_only,
            no_extract_mentions=self.no_extract_mentions,
            no_extract_hashtags=self.no_extract_hashtags,
            no_extract_emojis=self.no_extract_emojis,
            preview=self.preview,
            geo=self.geo,
            file_ids=self.file_ids,
            reply_id=self.reply_id,
            renote_id=self.renote_id,
            channel_id=self.channel_id,
            poll=poll,
        )

    def add_file(
            self,
            path: str = None,
            name: str = None,
            force: bool = False,
            is_sensitive: bool = False,
            url: str = None,
    ):
        self.file_ids.append(
            self._state._add_file(
                path, name=name, force=force, is_sensitive=is_sensitive,
                url=url
            ).id
        )
        return self

    def add_poll(
            self,
            item: Optional[str] = "",
            expires_at: Optional[int] = None,
            expired_after: Optional[int] = None,
            item_list: Optional[dict] = None,
    ) -> "Note":
        poll = self.__poll_formatter()
        self.poll = Poll(
            **self._state._add_poll(
                item,
                poll=poll,
                expires_at=expires_at,
                expired_after=expired_after,
                item_list=item_list,
            )
        )
        return self

    async def add_reaction(self, reaction: str, note_id: str = None) -> bool:
        if note_id is None:
            note_id = self.id
        return await self._state._add_reaction(reaction, note_id=note_id)

    def emoji_count(self) -> int:
        """
        ノートの本文にemojiが何個含まれているかを返します

        Returns
        -------
        int
            含まれている絵文字の数
        """

        return utils.emoji_count(self.content)

    async def delete(self) -> tuple[bool, int]:
        """
        指定したIDのノートを削除します

        Returns
        -------
        is_success: bool
            成功したか否か
        status_code: int
            HTTP レスポンスステータスコード
        """

        return await self._state._note_delete(self.id)
