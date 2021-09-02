import json
import re
from typing import Any

import requests


class Message(object):
    def __init__(self, data: Any, ws=None):
        data = json.loads(data)
        self.type = data.get('type')
        self.header = Header(data.get('body', {}))
        if note := data.get('body', {}).get('body', None):
            self.note = Note(note, ws)
        elif note := data.get('createdNote', None):  # APIの場合
            self.note = Note(note, ws)
        else:
            data = data.get('body', {}).get('res', {}).get('createdNote', {})  # WebSocketsの場合
            data['res'] = True
            self.note = Note(data, ws)


class Header(object):
    def __init__(self, data):
        self.id = data.get('id')
        self.type = data.get('type')


class Note(object):
    def __init__(self, data=None, ws=None, text: str = '', cw: str = '', via_mobile: bool = False, token: str = None,
                 origin_uri: str = None):
        if data is None:  # リストをデフォルトにすると使いまわされて良くないので毎回初期化する必要がある。
            data = {}
        self.token = token
        self.ws = ws
        self.field = data
        self.origin_uri = origin_uri
        if not data:  # 型変更としてではなく、投稿などに使う際に必要
            self.field['text'] = text
            if len(cw) != 0:
                self.field['cw'] = cw
            self.field['viaMobile'] = via_mobile
            self.field['i'] = token

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

    def add_file(self, file_id: str = None, path: str = None, name: str = None) -> None:
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
        None
        """
        from mi import Drive
        self.field['fileIds'] = []
        if file_id is None:
            res = Drive(token=self.token, origin_uri=self.origin_uri).upload(path=path, name=name)
            self.field['fileIds'].append(f'{res.id}')
        else:
            self.field['fileIds'].append(f'{file_id}')

    async def send(self) -> requests.models.Response:
        print(self.field)
        data = json.dumps(self.field)
        res = requests.post(self.origin_uri + '/api/notes/create', data=data)
        print(res.text)
        msg = Message(res.text)
        return msg


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
        'emojis'
    )

    def __init__(self, data: dict):
        self.id = data.get('id')
        self.name = data.get('name', data.get('username', None))
        self.username = data.get('username')
        self.host = data.get('host')
        self.avatar_url = data.get('avatarUrl')
        self.avatar_blurhash = data.get('avatarBlurhash')
        self.avatar_color = data.get('avatarColor')
        self.instance = Instance(data)
        self.emojis = data.get('emojis')


class Instance(object):
    __slots__ = (
        'home',
        'name',
        'software_name',
        'icon_url',
        'favicon_url',
        'theme_color'
    )

    def __init__(self, data):
        self.home = data.get('instance', {}).get('home')
        self.name = data.get('instance', {}).get('name')
        self.software_name = data.get('instance', {}).get('softwareName')
        self.icon_url = data.get('instance', {}).get('iconUrl')
        self.favicon_url = data.get('instance', {}).get('faviconUrl')
        self.theme_color = data.get('instance', {}).get('themeColor')
