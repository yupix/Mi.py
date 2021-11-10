import json
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from mi import Drive, Emoji, UserProfile, utils
from mi.exception import ContentRequired
from mi.user import Author, UserAction
from mi.utils import api, remove_dict_empty, upper_to_lower
from .abc.note import AbstractNote
from .types.note import (
    Note as NotePayload,
    Poll as PollPayload,
    Renote as RenotePayload,
)


class NoteAction:
    @staticmethod
    async def add_reaction(reaction: str, note_id: str = None) -> bool:
        """
        指定したnoteに指定したリアクションを付与します（内部用

        Parameters
        ----------
        reaction : Optional[str]
            付与するリアクション名
        note_id : Optional[str]
            付与対象のノートID

        Returns
        -------
        status: bool
            成功したならTrue,失敗ならFalse
        """
        data = {"noteId": note_id, "reaction": reaction}
        res = api("/api/notes/reactions/create", json_data=data, auth=True)
        return res.status_code == 204

    @staticmethod
    async def delete(note_id: str) -> tuple[bool, int]:
        data = {"noteId": note_id}
        res = api("/api/notes/delete", json_data=data, auth=True)
        return res.status_code == 204, res.status_code

    @staticmethod
    def add_file(
        path: str,
        *,
        name: str = None,
        force: bool = False,
        is_sensitive: bool = False,
        url
    ) -> Drive:
        """
        ノートにファイルを添付します。

        Parameters
        ----------
        is_sensitive : bool
            この画像がセンシティブな物の場合Trueにする
        field : dict
            ファイル送信用のdict
        force : bool
            Trueの場合同じ名前のファイルがあった場合でも強制的に保存する
        path : str
            そのファイルまでのパスとそのファイル.拡張子(/home/test/test.png)
        name: str
            ファイル名(拡張子があるなら含めて)
        url : str
            URLから画像をアップロードする場合にURLを指定する

        Returns
        -------
        self: Note
        """
        return Drive().upload(path, name, force, is_sensitive, url=url)

    @staticmethod
    def add_poll(
        item: Optional[str] = None,
        *,
        poll: Optional[dict],
        expires_at: Optional[int] = None,
        expired_after: Optional[int] = None,
        item_list: Optional[List] = None
    ) -> dict:
        """
        アンケートを作成します

        Parameters
        ----------
        poll : Optional[dict]
            既にあるpollを使用する
        item_list : Optional[List]
            アンケート選択肢を配列にしたもの
        item: Optional[str]
            アンケートの選択肢(単体)
        expires_at : Optional[int]
            いつにアンケートを締め切るか 例:2021-09-02T15:00:00.000Z
        expired_after : Optional[int]
            投稿後何秒後にアンケートを締め切るか(秒

        Returns
        -------
        poll: dict
        """
        if poll is None:
            poll = {
                "choices": [],
                "expiresAt": expires_at,
                "expiredAfter": expired_after,
            }
        if item:
            poll["choices"].append(item)
        if item_list:
            poll["choices"].extend(item_list)

        return poll

    @staticmethod
    async def send(
        *,
        other_field: dict = None,
        visibility,
        visible_user_ids,
        text,
        cw,
        via_mobile,
        local_only,
        no_extract_mentions,
        no_extract_hashtags,
        no_extract_emojis,
        reply_id,
        renote_id,
        channel_id,
        preview,
        geo,
        file_ids,
        poll
    ) -> "NoteContent":
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
            raise ContentRequired("ノートの送信にはtext, file, renote またはpollのいずれか1つが無くてはいけません")
        return NoteContent(res_json)


class Follow(BaseModel):
    id: Optional[str] = None
    created_at: Optional[str] = None
    type: Optional[str] = None
    user: Optional[UserProfile] = UserProfile()
    __user_action: UserAction = UserAction()

    class Config:
        arbitrary_types_allowed = True

    def follow(self, user_id: Optional[str] = None) -> tuple[bool, str]:
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
        if user_id is None:
            user_id = self.user.id
        return self.__user_action.follow(user_id)

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
        return self.__user_action.unfollow(user_id)


class Header:
    def __init__(self, data):
        self.id = data.get("id")
        self.type = data.get("type")


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
        self.multiple: bool = data["multiple"]
        self.expires_at: int = data["expires_at"]
        self.choices: List = data["choices"]
        self.expired_after: int = data["expired_after"]


class Renote(AbstractNote):
    def __init__(self, data: RenotePayload):
        self.id = data["id"]
        self.created_at = data["created_at"]
        self.user_id = data["user_id"]
        self.user = Author(data["user"])
        self.content = data.get("content", None)
        self.cw = data["cw"]
        self.visibility = data["visibility"]
        self.renote_count = data["renote_count"]
        self.replies_count = data["replies_count"]
        self.reactions = data["reactions"]
        self.emojis = data["emojis"]
        self.file_ids = data["file_ids"]
        self.files = data["files"]
        self.reply_id = data["reply_id"]
        self.files = data["files"]
        self.reply_id = data["reply_id"]
        self.renote_id = data["renote_id"]
        self.uri = data["uri"]
        self.poll = Poll(data["poll"]) if data.get("poll") else None
        self.__note_action = NoteAction

    def add_file(
        self,
        path: str = None,
        name: str = None,
        force: bool = False,
        is_sensitive: bool = False,
        url: str = None,
    ):
        self.file_ids.append(
            self.__note_action.add_file(
                path, name=name, force=force, is_sensitive=is_sensitive, url=url
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


class Reaction(BaseModel):
    id: Optional[str] = Field(None, alias="id_")
    reaction: Optional[str] = None
    user_id: Optional[str] = None


class Geo(BaseModel):
    coordinates: Optional[List[Any]] = []
    altitude: Optional[int] = 0
    accuracy: Optional[int] = 0
    altitude_accuracy: Optional[int] = 0
    heading: Optional[int] = 360
    speed: Optional[int] = 0


class Note(AbstractNote):
    def __init__(
        self,
        content: str,
        *,
        visibility: str = "public",
        visible_user_ids: List[str] = None,
        cw: str = None,
        local_only: bool = False,
        no_extract_mentions: bool = False,
        no_extract_hashtags: bool = False,
        no_extract_emojis: bool = False,
        reply_id: List[str] = None,
        renote_id: str = None,
        channel_id: str = None,
        file_ids: List[File] = None,
        poll: Poll = None
    ):
        self.content: str = content
        self.visibility: str = visibility
        self.visible_user_ids: List[str] = visible_user_ids
        self.cw: str = cw
        self.local_only: bool = local_only
        self.no_extract_mentions: bool = no_extract_mentions
        self.no_extract_hashtags: bool = no_extract_hashtags
        self.no_extract_emojis: bool = no_extract_emojis
        self.reply_id: List[str] = reply_id
        self.renote_id: str = renote_id
        self.channel_id: str = channel_id
        self.file_ids: List[File] = file_ids
        self.poll: Poll = poll

    async def send(self):
        field = {
            "visibility": self.visibility,
            "visibleUserIds": self.visible_user_ids,
            "text": self.content,
            "cw": self.cw,
            "localOnly": self.local_only,
            "noExtractMentions": self.no_extract_mentions,
            "noExtractHashtags": self.no_extract_hashtags,
            "noExtractEmojis": self.no_extract_emojis,
            "replyId": self.reply_id,
            "renoteId": self.renote_id,
            "channelId": self.channel_id,
        }
        if self.poll and len(self.poll.choices) > 0:
            field["poll"] = self.poll
        if self.file_ids:
            field["fileIds"] = self.file_ids
        field = remove_dict_empty(field)
        res = api("/api/notes/create", json_data=field, auth=True)
        res_json = res.json()
        if (
            res_json.get("error")
            and res_json.get("error", {}).get("code") == "CONTENT_REQUIRED"
        ):
            raise ContentRequired("ノートの送信にはtext, file, renote またはpollのいずれか1つが無くてはいけません")
        return NoteContent(
            upper_to_lower(res_json["createdNote"], replace_list={"user": "author"})
        )

    def emoji_count(self) -> int:
        return utils.emoji_count(self.content)

    async def delete(self, note_id: str = None) -> bool:
        pass

    def add_file(
        self,
        path: str = None,
        name: str = None,
        force: bool = False,
        is_sensitive: bool = False,
        url: str = None,
    ):
        pass


class NoteContent(AbstractNote):
    def __init__(self, data: NotePayload):
        self.id: str = data["id"]
        self.created_at: str = data["created_at"]
        self.user_id: str = data["user_id"]
        self.author = Author(data["author"])
        self.content: Optional[str] = data.get("content")
        self.cw: str = data["cw"]
        self.renote: Renote = Renote(data["renote"]) if data.get("renote") else None
        self.visibility: str = data["visibility"]
        self.renote_count: int = data["renote_count"]
        self.replies_count: int = data["replies_count"]
        self.reactions: Dict[str, Any] = data["reactions"]
        self.emojis: List[Emoji] = data["emojis"]
        self.file_ids: Optional[List[str]] = data["file_ids"]
        self.files: Optional[List[File]] = data["files"]
        self.reply_id: Optional[str] = data["reply_id"]
        self.renote_id: Optional[str] = data["renote_id"]
        self.poll: Optional[Poll] = Poll(data["poll"]) if data.get("poll") else None
        self.visible_user_ids: Optional[List[str]] = data.get("visible_user_ids", [])
        self.via_mobile: Optional[bool] = data.get("via_mobile", False)
        self.local_only: Optional[bool] = data.get("local_only", False)
        self.no_extract_mentions: Optional[bool] = data.get(
            "no_extract_mentions", False
        )
        self.no_extract_hashtags: Optional[bool] = data.get("no_extract_hashtags")
        self.no_extract_emojis: Optional[bool] = data.get("no_extract_emojis")
        self.preview: Optional[bool] = data.get("preview")
        self.geo: Optional[Geo] = Geo(data["geo"]) if data.get("geo") else None
        self.media_ids: Optional[List[str]] = data.get("media_ids")
        self.field: Optional[dict] = {}
        self.tags: Optional[List[str]] = data.get("tags", [])
        self.channel_id: Optional[str] = data.get("channel_id")
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
            self.__note_action.add_file(
                path, name=name, force=force, is_sensitive=is_sensitive, url=url
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
            **self.__note_action.add_poll(
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
        return await self.__note_action.add_reaction(reaction, note_id=note_id)

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

        return await self.__note_action.delete(self.id)
