import json
import re
from typing import Any, Final
import requests

from mi import Drive
from mi.utils import set_auth_i, upper_to_lower


class _EmptyNote:
    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return 'Note.Empty'

    def __len__(self) -> int:
        return 0


EmptyEmbed: Final = _EmptyNote()


class Message(object):
    def __init__(self, data: Any = None, web_socket=None, auth_i: dict = None):
        if data is None:
            data = {}
        data = json.loads(data)
        self.auth_i = auth_i
        self.type = data.get('type')
        self.header = Header(data.get('body', {}))
        if note := data.get('body', {}).get('body', None):
            self.note = Note(**upper_to_lower(note))
        elif note := data.get('createdNote', None):  # APIの場合
            self.note = Note(**upper_to_lower(note))
        else:
            data = data.get('body', {}).get('res', {}).get('createdNote', {})  # WebSocketsの場合
            data['res'] = True
            self.note = Note(data)

    async def delete(self) -> bool:
        set_auth_i(self.note, self.auth_i, True)
        data = json.dumps({'noteId': self.note.id, 'i': self.note.token})
        res = requests.post(self.note.origin_uri + '/api/notes/delete', data=data)
        status = True if res.status_code == 204 else False
        return status


class Header(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.type = data.get('type')


class Note(object):
    def __init__(self,
                 id_: str = None,
                 created_at: str = None,
                 user_id: str = None,
                 author=None,
                 text: str = None,
                 cw: str = None,
                 visibility=None,
                 renote_count=None,
                 replies_count=None,
                 reactions=None,
                 emojis=None,
                 file_ids=None,
                 files=None,
                 reply_id=None,
                 renote_id=None,
                 via_mobile=None,
                 poll=None,
                 res=None,
                 data=None,
                 token: str = None,
                 origin_uri: str = None):
        if data is None:  # リストをデフォルトにすると使いまわされて良くないので毎回初期化する必要がある。
            data = {}
        self.id = id_
        self.created_at = created_at
        self.user_id = user_id
        self.author = User(**upper_to_lower(author))
        self.text = text
        self.visibility = visibility
        self.renote_count = renote_count
        self.replies_count = replies_count
        self.reactions = reactions
        self.emojis = emojis
        self.file_ids = file_ids
        self.files = files
        self.reply_id = reply_id
        self.renote_id = renote_id
        self.poll = poll
        self.res = res
        self.token = token
        self.field = data
        self.origin_uri = origin_uri
        if not data:  # 型変更としてではなく、投稿などに使う際に必要
            self.field['text'] = text
            if cw:
                self.field['cw'] = cw
            self.field['viaMobile'] = via_mobile
            self.field['i'] = token

    @classmethod
    def from_dict(cls, data):

        self = cls.__new__(cls)

        after_key = {'user': 'author'}
        for attr in ('id', 'createdAt', 'userId', 'user', 'text', 'cw',
                     'visibility', 'renoteCount', 'repliesCount', 'reactions',
                     'emojis', 'fileIds', 'files', 'replyId',
                     'renoteId', 'res'
                     ):
            try:
                value = data[attr]
                p = re.compile('[A-Z]')
                default_key = ("_" + p.search(attr)[0].lower()).join(p.split(attr)) if p.search(attr) is not None else attr
                key = after_key.get(default_key, default_key)
            except KeyError:
                continue
            else:  # エラーが発生しなかった場合は変数に追加
                if key == 'author':
                    setattr(self, key, User(value))
                else:
                    setattr(self, key, data[attr])

    def add_file(self, file_id: str = None, path: str = None, name: str = None) -> 'Note':
        """
        ノートにファイルを添付します。

        Parameters
        ----------
        file_id : str
            既にドライブにあるファイルを使用する場合のファイルID
        path : str
            新しくファイルをアップロードする際のファイルへのパス
        name : str
            新しくファイルをアップロードする際のファイル名(misskey side

        Returns
        -------
        self: Note
        """
        self.field['fileIds'] = []
        if file_id is None:
            res = Drive(token=self.token, origin_uri=self.origin_uri).upload(path=path, name=name)
            self.field['fileIds'].append(f'{res.id}')
        else:
            self.field['fileIds'].append(f'{file_id}')
        return self

    def add_poll(self, data: list = None, item: str = '', expires_at: int = None, expired_after: int = None):
        """
        アンケートを作成します

        Parameters
        ----------
        data : list
            アンケートの配列
        item: str
            アンケートの項目名
        expires_at : int
            いつにアンケートを締め切るか 例:2021-09-02T15:00:00.000Z
        expired_after : int
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

    async def send(self) -> Message:
        """
        既にあるnoteクラスを元にnoteを送信します

        Returns
        -------
        msg: Message
        """
        data = json.dumps(self.field)
        res = requests.post(self.origin_uri + '/api/notes/create', data=data)
        msg = Message(res.text)
        msg.note.origin_uri = self.origin_uri
        msg.note.token = self.token
        return msg

    async def delete(self, id_: str = None) -> bool:
        if id_ is not None:
            self.id = id_
        data = json.dumps({'noteId': self.id, 'i': self.token})
        res = requests.post(self.origin_uri + '/api/notes/delete', data=data)
        status = True if res.status_code == 204 else False
        return status


class Reaction(object):
    def __init__(self, data):
        data = json.loads(data)
        self.header = Header(data.get('body', {}))
        self.note = ReactionNote(data.get('body'))


class ReactionNote(object):
    def __init__(self, data):
        self.reaction = data['body'].get('reaction')
        self.user_id = data['body'].get('userId')


class User(object):
    __slots__ = (
        'id',
        'name',
        'username',
        'host',
        'avatar_url',
        'avatar_blurhash',
        'avatar_color',
        'instance',
        'emojis',
        'is_admin'
    )

    def __init__(self,
                 id_: str = None,
                 name: str = None,
                 username: str = None,
                 host: str = None,
                 avatar_url: str = None,
                 avatar_blurhash: str = None,
                 avatar_color: str = None,
                 instance: dict = None,
                 emojis=None,
                 is_admin=None
                 ):
        self.id = id_
        self.name = name
        self.username = username
        self.host = host
        self.avatar_url = avatar_url
        self.avatar_blurhash = avatar_blurhash
        self.avatar_color = avatar_color
        self.instance = Instance(**upper_to_lower(instance))
        self.emojis = emojis
        self.is_admin = is_admin

    @classmethod
    def from_dict(cls, data: dict):
        self = cls.__new__(cls)
        self.id = data.get('id')
        self.name = data.get('name', data.get('username', None))
        self.username = data.get('username')
        self.host = data.get('host')
        self.avatar_url = data.get('avatarUrl')
        self.avatar_blurhash = data.get('avatarBlurhash')
        self.avatar_color = data.get('avatarColor')
        self.instance = Instance(**upper_to_lower(data))
        self.emojis = data.get('emojis')
        self.is_admin = data.get('is_admin')


class Instance(object):
    __slots__ = (
        'home',
        'name',
        'software_name',
        'icon_url',
        'favicon_url',
        'theme_color'
    )

    def __init__(self,
                 home: str = None,
                 name: str = None,
                 software_name: str = None,
                 icon_url: str = None,
                 favicon_url=None,
                 theme_color=None
                 ):
        self.home = home
        self.name = name
        self.software_name = software_name
        self.icon_url = icon_url
        self.favicon_url = favicon_url
        self.theme_color = theme_color

    @classmethod
    def from_dict(cls, data: dict):
        self = cls.__new__(cls)
        self.home = data.get('instance', {}).get('home')
        self.name = data.get('instance', {}).get('name')
        self.software_name = data.get('instance', {}).get('softwareName')
        self.icon_url = data.get('instance', {}).get('iconUrl')
        self.favicon_url = data.get('instance', {}).get('faviconUrl')
        self.theme_color = data.get('instance', {}).get('themeColor')
