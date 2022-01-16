from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

from mi import utils
from mi.drive import File
from mi.exception import NotExistRequiredData
from mi.models.note import RawNote, RawRenote
from mi.models.poll import RawPoll
from mi.models.user import RawUser
from mi.user import User
from .abc.note import AbstractNote
from .types.note import (Reaction as ReactionPayload)

if TYPE_CHECKING:
    from mi import ConnectionState

__all__ = ['Note', 'Poll', 'Reaction', 'Follow', 'Header', 'File', 'Renote']


class Follow:
    def __init__(self, data, state: ConnectionState):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[str] = data.get('created_at')
        self.type: Optional[str] = data.get('type')
        self.user: Optional[User] = data.get('user')
        self._state = state

    async def follow(self) -> tuple[bool, Optional[str]]:
        """
        ユーザーをフォローします
        Returns
        -------
        bool
            成功ならTrue, 失敗ならFalse
        str
            実行に失敗した際のエラーコード
        """

        if self.id:
            raise NotExistRequiredData('user_idがありません')
        return await self._state.follow_user(user_id=self.id)

    async def unfollow(self, user_id: Optional[str] = None) -> bool:
        """
        与えられたIDのユーザーのフォローを解除します

        Parameters
        ----------
        user_id : Optional[str] = None
            フォローを解除したいユーザーのID

        Returns
        -------
        status
            成功ならTrue, 失敗ならFalse
        """

        if user_id is None:
            user_id = self.user.id
        return await self._state.unfollow_user(user_id)


class Header:
    def __init__(self, data, state: ConnectionState):
        self.id = data.get("id")
        self.type = data.get("type")
        self._state = state


class Poll:
    def __init__(self, raw_data: RawPoll):
        self.__raw_data = raw_data

    @property
    def multiple(self):
        return self.__raw_data.multiple

    @property
    def expires_at(self):
        return self.__raw_data.expires_at

    @property
    def choices(self):
        return self.__raw_data.choices

    @property
    def expired_after(self):
        return self.__raw_data.expired_after


class Renote(AbstractNote):
    def __init__(self, raw_data: RawRenote, state: ConnectionState):
        self.__raw_data: RawRenote = raw_data
        self.__state = state

    @property
    def id(self) -> str:
        return self.__raw_data.id

    @property
    def created_at(self):
        return self.__raw_data.created_at

    @property
    def user_id(self):
        return self.__raw_data.user_id

    @property
    def user(self):
        return User(self.__raw_data.user, state=self.__state)

    @property
    def content(self):
        return self.__raw_data.content

    @property
    def cw(self):
        return self.__raw_data.cw

    @property
    def visibility(self):
        return self.__raw_data.visibility

    @property
    def renote_count(self):
        return self.__raw_data.renote_count

    @property
    def replies_count(self):
        return self.__raw_data.replies_count

    @property
    def reactions(self):
        return self.__raw_data.reactions

    @property
    def emojis(self):
        return self.__raw_data.emojis

    @property
    def file_ids(self):
        return self.__raw_data.file_ids

    @property
    def files(self):
        return self.__raw_data.files

    @property
    def reply_id(self):
        return self.__raw_data.reply_id

    @property
    def renote_id(self):
        return self.__raw_data.renote_id

    @property
    def uri(self):
        return self.__raw_data.uri

    @property
    def poll(self) -> Poll | None:
        return Poll(self.__raw_data.poll) if self.__raw_data.poll else None

    def emoji_count(self) -> int:
        """
        ノートの本文にemojiが何個含まれているかを返します

        Returns
        -------
        int
            含まれている絵文字の数
        """

        return utils.emoji_count(self.__raw_data.content)

    async def delete(self) -> bool:
        return await self.__state.delete_note(self.__raw_data.id)


class Reaction:
    def __init__(self, data: ReactionPayload, state: ConnectionState):
        self.id: Optional[str] = data.get('id')
        self.created_at = data.get('created_at')
        self.type: Optional[str] = data.get('type')
        self.is_read: bool = bool(data.get('is_read'))
        self.user: Optional[User] = User(RawUser(data['user']), state=state) if data.get('user') else None
        self.note: Optional[Note] = Note(RawNote(data['note']), state=state) if data.get('note') else None
        self.reaction: str = data['reaction']
        self._state: ConnectionState = state


class Note(AbstractNote):
    def __init__(self, raw_data: RawNote, state: ConnectionState):
        self.__raw_data = raw_data
        self.__state = state

    @property
    def id(self):
        return self.__raw_data.id

    @property
    def created_at(self):
        return self.__raw_data.created_at

    @property
    def user_id(self):
        return self.__raw_data.user_id

    @property
    def author(self):
        return self.__raw_data.author

    @property
    def content(self):
        return self.__raw_data.content

    @property
    def cw(self):
        return self.__raw_data.cw

    @property
    def renote(self) -> None | Renote:
        return Renote(self.__raw_data.renote, state=self.__state) if self.__raw_data.renote else None

    @property
    def visibility(self):
        return self.__raw_data.visibility

    @property
    def renote_count(self):
        return self.__raw_data.renote_count

    @property
    def replies_count(self):
        return self.__raw_data.replies_count

    @property
    def reactions(self):
        return self.__raw_data.reactions

    @property
    def emojis(self):
        return self.__raw_data.emojis  # TODO: 実装

    @property
    def file_ids(self):
        return self.__raw_data.file_ids

    @property
    def files(self) -> List[File]:
        return [File(i, state=self.__state) for i in self.__raw_data.files]

    @property
    def reply_id(self):
        return self.__raw_data.reply_id

    @property
    def renote_id(self):
        return self.__raw_data.renote_id

    @property
    def poll(self) -> Poll | None:
        return Poll(self.__raw_data.poll) if self.__raw_data.poll else None

    @property
    def visible_user_ids(self):
        return self.__raw_data.visible_user_ids

    @property
    def via_mobile(self):
        return self.__raw_data.via_mobile

    @property
    def local_only(self):
        return self.__raw_data.local_only

    @property
    def extract_mentions(self):
        return self.__raw_data.extract_mentions

    @property
    def extract_hashtags(self):
        return self.__raw_data.extract_hashtags

    @property
    def extract_emojis(self):
        return self.__raw_data.extract_emojis

    @property
    def preview(self):
        return self.__raw_data.preview

    @property
    def media_ids(self):
        return self.__raw_data.media_ids

    @property
    def field(self):
        return self.__raw_data.field

    @property
    def tags(self):
        return self.__raw_data.tags

    @property
    def channel_id(self):
        return self.__raw_data.channel_id

    async def reply(
            self, content: Optional[str],
            cw: Optional[str] = None,
            extract_mentions: bool = True,
            extract_hashtags: bool = True,
            extract_emojis: bool = True,
            renote_id: Optional[str] = None,
            channel_id: Optional[str] = None,
            file_ids=None,
            poll: Optional[Poll] = None
    ) -> Note:
        """
        ノートに対して返信を送信します

        Parameters
        ----------
        content: Optional[str]
            返信内容
        cw: Optional[str]
            閲覧注意
        extract_mentions : bool, optional
            メンションを展開するか, by default False
        extract_hashtags : bool, optional
            ハッシュタグを展開するか, by default False
        extract_emojis : bool, optional
            絵文字を展開するか, by default False
        renote_id : Optional[str], optional
            リノート先のid, by default None
        channel_id : Optional[str], optional
            チャンネルid, by default None
        file_ids : [type], optional
            添付するファイルのid, by default None
        poll : Optional[Poll], optional
            アンケート, by default None
        """
        if file_ids is None:
            file_ids = []
        return await self.__state.post_note(
            content,
            visibility=self.visibility,
            visible_user_ids=self.visible_user_ids,
            cw=cw,
            local_only=self.local_only,
            extract_mentions=extract_mentions,
            extract_hashtags=extract_hashtags,
            extract_emojis=extract_emojis,
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

    async def add_reaction(self, reaction: str) -> bool:
        """
        ノートにリアクションを追加します

        Parameters
        ----------
        reaction: str
            つけるリアクション

        Returns
        -------
        bool
            成功したかどうか
        """

        return await self.__state.add_reaction_to_note(note_id=self.id, reaction=reaction)

    async def delete(self) -> bool:
        """
        ノートを削除します

        Returns
        -------
        bool
            成功したか否か
        """

        return await self.__state.delete_note(self.id)

    async def favorite(self) -> bool:
        """
        ノートをお気に入り登録します

        Returns
        -------
        bool
            成功したか否か
        """

        return await self.__state.favorite(note_id=self.id)

    async def remove_favorite(self) -> bool:
        """
        お気に入りから解除します

        Returns
        -------
        bool
            お気に入りの解除に成功したかどうか
        """

        return await self.__state.remove_favorite(note_id=self.id)

    async def add_to_clips(self, clip_id: str) -> bool:
        """
        指定したクリップにノートを追加します

        Returns
        -------
        bool
            クリップに追加できたかどうか
        """

        return await self.__state.add_note_to_clips(clip_id=clip_id, note_id=self.id)

    async def create_renote(self) -> Note:
        """
        ノートをリノートします

        Returns
        -------
        Note
            作成したリノート
        """

        return await self.__state.create_renote(self.id)

    async def get_replies(self, since_id: Optional[str] = None, until_id: Optional[str] = None, limit: int = 10) -> List[Note]:
        """
        ノートに対する返信を取得します

        Parameters
        ----------
        since_id: Optional[str], default=None
        until_id: Optional[str], default=None
            前回の最後のidから取得する場合
        limit: int, default=10
            取得する件数

        Returns
        -------
        List[Note]
            ノートに対する返信一覧
        """

        return await self.__state.get_replies(note_id=self.id, since_id=since_id, until_id=until_id, limit=limit)

    async def create_quote(self,
                           content: Optional[str] = None,
                           visibility: str = None,
                           visible_user_ids: Optional[List[str]] = None,
                           cw: Optional[str] = None,
                           local_only: bool = False,
                           extract_mentions: bool = True,
                           extract_hashtags: bool = True,
                           extract_emojis: bool = True,
                           file_ids=None,
                           poll: Optional[Poll] = None):
        """
        ノートを引用して新規にノートを投稿します

        Parameters
        ----------
        content: Optional[str], default=None
            引用に対するテキスト
        visibility: str, default=None
            ノートの公開範囲
        visible_user_ids: Optional[List[str]]
            ノートの公開対象になるユーザーid
        cw: Optional[str]
            閲覧注意の文字列
        local_only: bool
            ローカルにのみ公開するかどうか
        extract_mentions: bool
            メンションを展開するかどうか
        extract_hashtags: bool
            ハッシュタグを展開するかどうか
        extract_emojis: bool
            絵文字を展開するかどうか
        file_ids:
            添付するファイルのid
        poll: Optional[Poll]
            アンケート

        Returns
        -------
        Note
            作成した引用ノート
        """

        visibility = self.visibility or visibility or 'public'
        return await self.__state.create_quote(content=content, visibility=visibility, visible_user_ids=visible_user_ids,
                                               cw=cw,
                                               local_only=local_only, extract_mentions=extract_mentions,
                                               extract_hashtags=extract_hashtags,
                                               extract_emojis=extract_emojis, note_id=self.id, file_ids=file_ids,
                                               poll=poll)
