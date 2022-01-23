from __future__ import annotations

import asyncio
from typing import List, Optional, TYPE_CHECKING

from mi.api.favorite import FavoriteManager
from mi.api.reaction import ReactionManager
from mi.exception import ContentRequired
from mi.models.note import RawNote
from mi.note import Note, Poll
from mi.utils import check_multi_arg, remove_dict_empty
from mi.http import HTTPClient, Route

if TYPE_CHECKING:
    from mi.state import ConnectionState

__all__ = ['NoteActions']


class NoteActions:
    def __init__(self, state: 'ConnectionState', http: HTTPClient, loop: asyncio.AbstractEventLoop,
                 note_id: Optional[str] = None):
        self.__state = state
        self.__http = http
        self.__loop = loop
        self.favorite = FavoriteManager(state, http, loop, note_id=note_id)
        self.reaction = ReactionManager(state, http, loop, note_id=note_id)

    async def add_clips(self, clip_id: str, note_id: str) -> bool:
        data = {'noteId': note_id, 'clipId': clip_id}
        return bool(await self.__http.request(Route('POST', '/api/clips/add-note'), json=data, auth=True))

    async def send(self,
                   content: Optional[str] = None,
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
            "noExtractMentions": extract_mentions,
            "noExtractHashtags": extract_hashtags,
            "noExtractEmojis": extract_emojis,
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
        res = await self.__http.request(Route('POST', '/api/notes/create'), json=field, auth=True, lower=True)
        return Note(RawNote(res["created_note"]), state=self.__state)

    async def delete(self, note_id: Optional[str] = None):
        data = {"noteId": note_id}
        res = await self.__http.request(Route('POST', '/api/notes/delete'), json=data, auth=True)
        return bool(res)

    async def create_renote(self, note_id: str) -> Note:
        return await self.send(renote_id=note_id)

    async def create_quote(self, note_id: str,
                           content: Optional[str] = None,
                           visibility: str = 'public',
                           visible_user_ids: Optional[List[str]] = None,
                           cw: Optional[str] = None,
                           local_only: bool = False,
                           extract_mentions: bool = True,
                           extract_hashtags: bool = True,
                           extract_emojis: bool = True,
                           file_ids=None,
                           poll: Optional[Poll] = None) -> Note:
        return await self.send(content=content, visibility=visibility, visible_user_ids=visible_user_ids, cw=cw,
                               local_only=local_only, extract_mentions=extract_mentions,
                               extract_hashtags=extract_hashtags,
                               extract_emojis=extract_emojis, renote_id=note_id, file_ids=file_ids, poll=poll)

    async def get_note(self, note_id) -> Note:
        res = await self.__http.request(Route('POST', '/api/notes/show'), json={"noteId": note_id}, auth=True, lower=True)
        return Note(RawNote(res), state=self.__state)

    async def get_replies(self, note_id: str, since_id: Optional[str] = None, until_id: Optional[str] = None,
                          limit: int = 10, ) -> List[Note]:
        res = await self.__http.request(Route('POST', '/api/notes/replies'),
                                        json={"noteId": note_id, "sinceId": since_id, "untilId": until_id, "limit": limit},
                                        auth=True, lower=True)
        return [Note(RawNote(i), state=self.__state) for i in res]

    def get_reaction(self, note_id: str, reaction: str):
        return ReactionManager(self.__state, self.__http, self.__loop, note_id=note_id)