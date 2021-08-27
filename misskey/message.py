import json
from misskey.note import Note
from misskey.context import Header


class Message(object):
    def __init__(self, data, ws):
        data = json.loads(data)
        self.type = data.get('type')
        self.header = Header(data.get('body', {}))
        self.note = Note(data.get('body', {}).get('body', {}), ws)
