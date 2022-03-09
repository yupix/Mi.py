from __future__ import annotations

from typing import List, Optional

from mi.exception import ContentRequired
from mi.framework.http import HTTPSession
from mi.framework.models.note import Note, NoteReaction, Poll
from mi.framework.router import Route
from mi.utils import check_multi_arg, remove_dict_empty
from mi.wrapper.favorite import FavoriteManager
from mi.wrapper.models.note import RawNote
from mi.wrapper.reaction import ReactionManager

__all__ = ['NoteActions']


class NoteActions:
    def __init__(self, note_id: Optional[str] = None):
        self.__note_id: Optional[str] = note_id
        self.favorite = FavoriteManager(note_id=note_id)
        self.reaction = ReactionManager(note_id=note_id)

    async def add_clips(self, clip_id: str, note_id: Optional[str] = None) -> bool:
        """
        クリップに追加します

        Parameters
        ----------
        note_id : Optional[str], default=None
                追加するノートのID
        clip_id : str
            クリップのID
        note_id : Optional[str], default=None
            追加したいノートのID

        Returns
        -------
        bool
            成功したか否か
        """

        note_id = note_id or self.__note_id

        data = {'noteId': note_id, 'clipId': clip_id}
        return bool(await HTTPSession.request(Route('POST', '/api/clips/add-note'), json=data, auth=True))

    @staticmethod
    async def send(content: Optional[str] = None,
                   visibility: str = "public",
                   visible_user_ids: Optional[List[str]] = None,
                   cw: Optional[str] = None,
                   local_only: bool = False,
                   extract_mentions: bool = True,
                   extract_hashtags: bool = True,
                   extract_emojis: bool = True,
                   reply_id: Optional[str] = None,
                   renote_id: Optional[str] = None,
                   channel_id: Optional[str] = None,
                   file_ids=None,
                   poll: Optional[Poll] = None
                   ) -> Note:
        """
        ノートを投稿します。

        Parameters
        ----------
        content : Optional[str], default=None
            投稿する内容
        visibility : str, optional
            公開範囲, by default "public"
        visible_user_ids : Optional[List[str]], optional
            公開するユーザー, by default None
        cw : Optional[str], optional
            閲覧注意の文字, by default None
        local_only : bool, optional
            ローカルにのみ表示するか, by default False
        extract_mentions : bool, optional
            メンションを展開するか, by default False
        extract_hashtags : bool, optional
            ハッシュタグを展開するか, by default False
        extract_emojis : bool, optional
            絵文字を展開するか, by default False
        reply_id : Optional[str], optional
            リプライ先のid, by default None
        renote_id : Optional[str], optional
            リノート先のid, by default None
        channel_id : Optional[str], optional
            チャンネルid, by default None
        file_ids : [type], optional
            添付するファイルのid, by default None
        poll : Optional[Poll], optional
            アンケート, by default None

        Returns
        -------
        Note
            投稿したノート

        Raises
        ------
        ContentRequired
            [description]
        """

        if file_ids is None:
            file_ids = []
        field = {
            "visibility": visibility,
            "visibleUserIds": visible_user_ids,
            "text": content,
            "cw": cw,
            "localOnly": local_only,
            "noExtractMentions": not extract_mentions,
            "noExtractHashtags": not extract_hashtags,
            "noExtractEmojis": not extract_emojis,
            "replyId": reply_id,
            "renoteId": renote_id,
            "channelId": channel_id
        }
        if not check_multi_arg(content, file_ids, renote_id, poll):
            raise ContentRequired("ノートの送信にはcontent, file_ids, renote_id またはpollのいずれか1つが無くてはいけません")

        if poll and type(Poll):
            poll_data = remove_dict_empty({
                'choices': poll.choices,
                'multiple': poll.multiple,
                'expiresAt': poll.expires_at,
                'expiredAfter': poll.expired_after
            })
            field["poll"] = poll_data

        if file_ids:
            field["fileIds"] = file_ids
        field = remove_dict_empty(field)
        res = await HTTPSession.request(Route('POST', '/api/notes/create'), json=field, auth=True, lower=True)
        return Note(RawNote(res["created_note"]))

    async def delete(self, note_id: Optional[str] = None) -> bool:
        """
        ノートを削除します

        Parameters
        ----------
        note_id : Optional[str], default=None
            削除したいノートのID

        Returns
        -------
        bool
            削除に成功したか否か
        """

        note_id = note_id or self.__note_id

        data = {"noteId": note_id}
        res = await HTTPSession.request(Route('POST', '/api/notes/delete'), json=data, auth=True)
        return bool(res)

    async def create_renote(self, note_id: Optional[str] = None) -> Note:
        """
        リノートを作成します

        Parameters
        ----------
        note_id : Optional[str], default=None
            ノートのID

        Returns
        -------
        Note
            作成したリノート
        """
        note_id = note_id or self.__note_id
        return await self.send(renote_id=note_id)

    async def create_quote(
            self,
            content: Optional[str] = None,
            visibility: str = 'public',
            visible_user_ids: Optional[List[str]] = None,
            cw: Optional[str] = None,
            local_only: bool = False,
            extract_mentions: bool = True,
            extract_hashtags: bool = True,
            extract_emojis: bool = True,
            file_ids: Optional[List[str]] = None,
            poll: Optional[Poll] = None,
            note_id: Optional[str] = None,
    ) -> Note:
        """
        Create a note quote.

        Parameters
        ----------
        content: Optional[str], default=None
            text
        visibility: str, default='public'
            Disclosure range
        visible_user_ids: Optional[List[str]], default=None
            List of users to be published
        cw: Optional[str], default=None
            Text to be displayed when warning is given
        local_only: bool, default=False
            Whether to show only locally or not
        extract_mentions: bool, default=True
            Whether to expand the mention
        extract_hashtags: bool, default=True
            Whether to expand the hashtag
        extract_emojis: bool, default=True
            Whether to expand the emojis
        file_ids: Optional[List[str]], default=None
            The ID list of files to be attached
        poll: Optional[Poll], default=None
            Questionnaire to be created
        note_id: Optional[str], default=None
            Note IDs to target for renote and citations
        """

        note_id = note_id or self.__note_id

        return await self.send(content=content, visibility=visibility, visible_user_ids=visible_user_ids, cw=cw,
                               local_only=local_only, extract_mentions=extract_mentions,
                               extract_hashtags=extract_hashtags,
                               extract_emojis=extract_emojis, renote_id=note_id, file_ids=file_ids, poll=poll)

    async def get_note(self, note_id: Optional[str] = None) -> Note:
        """
        ノートを取得します

        Parameters
        ----------
        note_id : Optional[str], default=None
            ノートのID

        Returns
        -------
        Note
            取得したノートID
        """
        note_id = note_id or self.__note_id
        res = await HTTPSession.request(Route('POST', '/api/notes/show'), json={"noteId": note_id}, auth=True, lower=True)
        return Note(RawNote(res))

    async def get_replies(
            self,
            since_id: Optional[str] = None,
            until_id: Optional[str] = None,
            limit: int = 10,
            note_id: Optional[str] = None
    ) -> List[Note]:
        """
        ノートに対する返信を取得します

        Parameters
        ---------
        since_id : Optional[str], default=None
            指定すると、その投稿を投稿を起点としてより新しい投稿を取得します
        until_id : Optional[str], default=None
            指定すると、その投稿を投稿を起点としてより古い投稿を取得します
        limit : int, default=10
            取得する上限
        note_id: Optional[str], default=None
            返信を取得したいノートのID

        Returns
        -------
        List[Note]
            返信のリスト
        """
        note_id = note_id or self.__note_id
        res = await HTTPSession.request(Route('POST', '/api/notes/replies'),
                                        json={"noteId": note_id, "sinceId": since_id, "untilId": until_id, "limit": limit},
                                        auth=True, lower=True)
        return [Note(RawNote(i)) for i in res]

    async def get_reaction(self, reaction: str, note_id: Optional[str] = None) -> List[NoteReaction]:
        note_id = note_id or self.__note_id
        return await ReactionManager(note_id=note_id).get_reaction(reaction)
