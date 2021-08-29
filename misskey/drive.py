import json
from typing import Any

import requests


class Drive(object):
    def __init__(self, data=None, token: str = None, origin_uri: str = None):
        # TODO 2021-08-29 こっちでupload等の引数を受け取る様にする
        if data is None:
            data = {}
        else:
            data = json.loads(data)
            self.id = data.get('id')
            self.created_at = data.get('createdAt')
            self.name = data.get('name')
            self.type = data.get('type')
            self.md5 = data.get('md5')
            self.size = data.get('size')
            self.is_sensitive = data.get('isSensitive')
            self.blurhash = data.get('blurhash')
            self.properties = Properties(data.get('properties', {}))
            self.url = data.get('url')
            self.thumbnail_url = data.get('thumbnailUrl')
        self.token = token
        self.origin_uri = origin_uri
        self.path: str = ''
        self.name: str = ''

    async def upload(self, path: str, name: str = None) -> 'Drive':
        """

        Parameters
        ----------
        path : str
            そのファイルまでのパスとそのファイル.拡張子(/home/test/test.png)
        name : str
            アップロードするファイルの名前
        Returns
        -------
        Drive: Drive
            upload後のレスポンスをDrive型に変更して返します
        """
        self.path = path
        self.name = name
        with open(path, 'rb') as f:
            file = f.read()
        args = {'i': f'{self.token}'}
        file = {'file': file}

        res = requests.post(self.origin_uri + '/api/drive/files/create', data=args, files=file)
        return Drive(res.text)


class Properties(object):
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.width = data.get('width')
        self.height = data.get('height')
