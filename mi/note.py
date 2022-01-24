from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from mi import utils
from mi.drive import File
from mi.emoji import Emoji
from mi.exception import NotExistRequiredData
from mi.models.note import RawNote, RawReaction, RawRenote
from mi.models.poll import RawPoll
from mi.models.user import RawUser
from mi.user import User
from .abc.note import AbstractNote
from .models.reaction import RawNoteReaction

if TYPE_CHECKING:
    from mi import ConnectionState
    from mi.state import NoteActions
    from mi.api.reaction import ReactionManager

__all__ = ('Note', 'Poll', 'Reaction', 'Follow', 'Header', 'File', 'Renote', 'NoteReaction')


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
        return await self._state.user.follow.add(user_id=self.id)

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
        return await self._state.user.follow.remove(user_id)


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
    def poll(self) -> Union[Poll, None]:
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


class NoteReaction:
    def __init__(self, raw_data: RawNoteReaction, state: ConnectionState):
        self.__raw_data = raw_data
        self.__state = state

    @property
    def id(self) -> str:
        return self.__raw_data.id

    @property
    def created_at(self) -> str:
        return self.__raw_data.created_at

    @property
    def user(self) -> User:
        return User(RawUser(self.__raw_data.user), state=self.__state)

    @property
    def reaction(self) -> str:
        return self.__raw_data.reaction


class Reaction:
    def __init__(self, raw_data: RawReaction, state: ConnectionState):
        self.__raw_data = raw_data
        self.__state: ConnectionState = state

    @property
    def id(self) -> Optional[str]:
        return self.__raw_data.id

    @property
    def created_at(self) -> Optional[str]:
        return self.__raw_data.created_at

    @property
    def type(self) -> Optional[str]:
        return self.__raw_data.type

    @property
    def is_read(self) -> bool:
        return self.__raw_data.is_read

    @property
    def user(self) -> Optional[User]:
        return User(self.__raw_data.user, state=self.__state) if self.__raw_data.user else None

    @property
    def note(self) -> Optional[Note]:
        return Note(self.__raw_data.note, state=self.__state) if self.__raw_data.note else None

    @property
    def reaction(self) -> str:
        return self.__raw_data.reaction

    @property
    def action(self) -> ReactionManager:
        return self.__state.reaction


class Note(AbstractNote):
    def __init__(self, raw_data: RawNote, state: ConnectionState):
        self.__raw_data: RawNote = raw_data
        self.__state: ConnectionState = state

    @property
    def id(self) -> str:
        return self.__raw_data.id

    @property
    def created_at(self) -> str:
        return self.__raw_data.created_at

    @property
    def user_id(self) -> str:
        return self.__raw_data.user_id

    @property
    def author(self) -> User:
        return User(self.__raw_data.author, state=self.__state)

    @property
    def content(self) -> Optional[str]:
        return self.__raw_data.content

    @property
    def cw(self) -> Optional[str]:
        return self.__raw_data.cw

    @property
    def renote(self) -> Union[None, Renote]:
        return Renote(self.__raw_data.renote, state=self.__state) if self.__raw_data.renote else None

    @property
    def visibility(self) -> Optional[str]:
        return self.__raw_data.visibility

    @property
    def renote_count(self) -> Optional[int]:
        return self.__raw_data.renote_count

    @property
    def replies_count(self) -> Optional[int]:
        return self.__raw_data.replies_count

    @property
    def reactions(self) -> Optional[Dict[str, Any]]:  # TODO: 型の確認
        return self.__raw_data.reactions

    @property
    def emojis(self) -> List[Emoji]:
        return [Emoji(i, state=self.__state) for i in self.__raw_data.emojis]

    @property
    def file_ids(self) -> Optional[List[str]]:
        return self.__raw_data.file_ids

    @property
    def files(self) -> List[File]:
        return [File(i, state=self.__state) for i in self.__raw_data.files]

    @property
    def reply_id(self) -> Optional[str]:
        return self.__raw_data.reply_id

    @property
    def renote_id(self) -> Optional[str]:
        return self.__raw_data.renote_id

    @property
    def poll(self) -> Union[Poll, None]:
        return Poll(self.__raw_data.poll) if self.__raw_data.poll else None

    @property
    def visible_user_ids(self) -> Optional[List[str]]:
        return self.__raw_data.visible_user_ids

    @property
    def via_mobile(self) -> bool:
        return self.__raw_data.via_mobile

    @property
    def local_only(self) -> bool:
        return self.__raw_data.local_only

    @property
    def extract_mentions(self) -> bool:
        return self.__raw_data.extract_mentions

    @property
    def extract_hashtags(self) -> bool:
        return self.__raw_data.extract_hashtags

    @property
    def extract_emojis(self) -> bool:
        return self.__raw_data.extract_emojis

    @property
    def preview(self) -> bool:
        return self.__raw_data.preview

    @property
    def media_ids(self) -> Optional[List[str]]:
        return self.__raw_data.media_ids

    @property
    def field(self) -> Optional[Dict]:
        return self.__raw_data.field

    @property
    def tags(self) -> Optional[List[str]]:
        return self.__raw_data.tags

    @property
    def channel_id(self) -> Optional[str]:
        return self.__raw_data.channel_id

    @property
    def action(self) -> NoteActions:
        return self.__state.get_note_instance(self.id)

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
        return await self.__state.note.send(
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
