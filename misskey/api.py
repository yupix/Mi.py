import re

from misskey import Note


class API(object):
    def __init__(self, token, origin_uri):
        self.token = token
        if _origin_uri := re.search(r'wss?://(.*)/streaming', origin_uri):
            origin_uri = _origin_uri.group(0).replace('wss', 'https').replace('ws', 'http').replace('/streaming', '')

        if origin_uri[-1] == '/':
            self.origin_uri = origin_uri[:-1]
        else:
            self.origin_uri = origin_uri

    def note(self, *args, **kwargs):
        return Note(token=self.token, origin_uri=self.origin_uri, *args, **kwargs)

