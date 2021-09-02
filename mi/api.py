import re

from mi import Note, Drive


class API(object):
    def __init__(self, token, origin_uri):
        self.token = token
        if _origin_uri := re.search(r'wss?://(.*)/streaming', origin_uri):
            origin_uri = _origin_uri.group(0).replace('wss', 'https').replace('ws', 'http').replace('/streaming', '')

        if origin_uri[-1] == '/':
            self.origin_uri = origin_uri[:-1]
        else:
            self.origin_uri = origin_uri

    def note(self, data=None, text: str = None, cw: str = None, via_mobile: bool = False, *args, **kwargs):
        if data is None:  # リストをデフォルトにすると使いまわされて良くないので毎回初期化する必要がある。
            if data:
                field = data
            else:
                field = {}
            field['text'] = text
            if cw:
                field['cw'] = cw
            field['viaMobile'] = via_mobile
            field['i'] = self.token
        else:
            field = data
        return Note(token=self.token, origin_uri=self.origin_uri, data=field, *args, **kwargs)

    def drive(self):
        return Drive(token=self.token, origin_uri=self.origin_uri)
