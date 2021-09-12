import json
import re
from typing import Any, Dict, List, Optional

import emoji
import requests
from pydantic import BaseModel, Field

from mi import Drive, Emoji, UserProfile, config
from mi.exception import CredentialRequired
from mi.user import Author
from mi.utils import api, upper_to_lower


class NoteAction(object):
    def emoji_count(self):
        if self.text is None:
            count = len(self.emojis)
        else:
            count = len(self.emojis) + emoji.emoji_count(self.text)
        return count

    async def add_reaction(self, reaction, note_id=None) -> bool:
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
        if note_id is None:
            id_ = self.id
        else:
            id_ = note_id
        data = json.dumps({'noteId': id_, 'i': config.i.token, 'reaction': reaction}, ensure_ascii=False)
        res = api(config.i.origin_uri, '/api/notes/reactions/create', data=data.encode('utf-8'))
        status = True if res.status_code == 204 else False
        return status

    async def delete(self, id_: Optional[str] = None) -> bool:
        if id_ is not None:
            self.id_ = id_
        else:
            self.id_ = self.id
        data = json.dumps({'noteId': self.id_, 'i': self.token}, ensure_ascii=False)
        res = requests.post(self.origin_uri + '/api/notes/delete', data=data)
        status = True if res.status_code == 204 else False
        return status

    def add_file(self, file_id: Optional[str] = None, path: Optional[str] = None, name: Optional[str] = None) -> 'Note':
        """
        ノートにファイルを添付します。

        Parameters
        ----------
        file_id : Optional[str]
            既にドライブにあるファイルを使用する場合のファイルID
        path : Optional[str]
            新しくファイルをアップロードする際のファイルへのパス
        name : Optional[str]
            新しくファイルをアップロードする際のファイル名(misskey side

        Returns
        -------
        self: Note
        """
        res = Drive(token=config.i.token, origin_uri=config.i.origin_uri).upload(path=path, name=name)
        self.field['fileIds'] = [res.id]
        return self

    def add_poll(self, data: Optional[List] = None, item: Optional[str] = '', expires_at: Optional[int] = None,
                 expired_after: Optional[int] = None, multiple: bool
                 = None):
        """
        アンケートを作成します

        Parameters
        ----------
        multiple :
        data : Optional[List]
            アンケートの配列
        item: Optional[str]
            アンケートの項目名
        expires_at : Optional[int]
            いつにアンケートを締め切るか 例:2021-09-02T15:00:00.000Z
        expired_after : Optional[int]
            投稿後何秒後にアンケートを締め切るか(秒

        Returns
        -------
        self: Note
        """
        if not self.field.get('poll'):
            self.field['poll'] = {}
            self.field['poll']['choices'] = []
        self.field['poll']['expiresAt'] = expires_at
        self.field['poll']['expiredAfter'] = expired_after
        if data:
            self.field['poll']['choices'] = data
        else:
            self.field['poll']['choices'].append(item)

        return self

    async def send(self) -> 'Note':
        """
        既にあるnoteクラスを元にnoteを送信します

        Returns
        -------
        msg: Note
        """
        self: Note
        field = {
            "visibility": self.visibility,
            "visibleUserIds": self.visible_user_ids,
            "text": self.text,
            "cw": self.cw,
            "viaMobile": self.via_mobile,
            "localOnly": self.local_only,
            "noExtractMentions": self.no_extract_mentions,
            "noExtractHashtags": self.no_extract_hashtags,
            "noExtractEmojis": self.no_extract_emojis,
            "replyId": self.reply_id,
            "renoteId": self.renote_id,
            "channelId": self.channel_id,
            "i": config.i.token
        }
        field.update(self.field)
        field = json.dumps(field, ensure_ascii=False)
        res = api(config.i.origin_uri, '/api/notes/create', field)
        res_json = res.json()
        if res_json.get('error') and res_json.get('error', {}).get('code'):
            raise CredentialRequired('認証情報がありましぇん')
        msg = Note(**res_json)
        return msg


class Follow:
    def __init__(self, id_: Optional[str] = None, created_at: Optional[str] = None, type_: Optional[str] = None,
                 body: dict = None):
        self.id_ = id_
        self.created_at = created_at
        self.type_ = type_
        self.user = UserProfile(**upper_to_lower(body))


class Header(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.type = data.get('type')


class Properties(BaseModel):
    width: Optional[int]
    height: Optional[int]


class File(BaseModel):
    id: Optional[str] = Field(None, alias='id_')
    created_at: Optional[str] = Field(None, alias='created_at')
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


class Poll(BaseModel):
    multiple: Optional[bool] = False
    expires_at: Optional[str] = None
    choices: Optional[List] = None
    expired_after: Optional[int] = None


class Renote(BaseModel):
    id: Optional[str] = None
    created_at: Optional[str] = None
    user_id: Optional[str] = None
    user: Optional[Author] = Author()
    text: Optional[str] = None
    cw: Optional[str] = None
    visibility: Optional[str] = None
    renote_count: Optional[int] = 0
    replies_count: Optional[int] = 0
    reactions: Dict[str, Any] = {}
    emojis: Optional[List] = []
    file_ids: Optional[List] = []
    files: Optional[List] = []
    reply_id: Optional[str] = None
    renote_id: Optional[str] = None
    uri: Optional[str] = None
    poll: Optional[Poll] = None


class Reaction(BaseModel):
    id: Optional[str] = Field(None, alias='id_')
    reaction: Optional[str] = None
    user_id: Optional[str] = None


class Note(BaseModel, NoteAction):
    id: Optional[str] = None
    created_at: Optional[str] = None
    user_id: Optional[str] = None
    author: Optional[Author] = Field(Author(), alias='user')
    text: Optional[str] = None
    cw: Optional[str] = None
    visibility: Optional[str] = 'public'
    renote_count: Optional[int] = None
    replies_count: Optional[int] = None
    reactions: Optional[Dict[str, Any]] = None
    emojis: Optional[List[Emoji]] = []
    file_ids: Optional[List[str]] = None
    files: Optional[List[File]] = None
    reply_id: Optional[str] = None
    renote_id: Optional[str] = None
    poll: Optional[Poll] = None
    visible_user_ids: Optional[List[str]] = []
    via_mobile: Optional[bool] = False
    local_only: Optional[bool] = False
    no_extract_mentions: Optional[bool] = False
    no_extract_hashtags: Optional[bool] = False
    no_extract_emojis: Optional[bool] = False
    media_ids: Optional[List[str]] = []
    channel_id: Optional[str] = None
    renote: Optional[Renote] = Renote()
    field: Optional[dict] = Field({})
