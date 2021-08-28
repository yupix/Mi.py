import json
import re
import uuid

import requests

from misskey.user import User


class Note(object):
    def __init__(self, data=None, ws=None, text: str = '', cw: str = '', via_mobile: bool = False, token: str = None,
                 origin_uri: str = None):
        if data is None:  # リストをデフォルトにすると使いまわされて良くないので毎回初期化する必要がある。
            data = {}
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

    async def send(self) -> requests.models.Response:
        data = json.dumps(self.field)
        return requests.post(self.origin_uri + '/api/notes/create', data=data)
