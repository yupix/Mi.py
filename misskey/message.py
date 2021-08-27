import json
from typing import Any

from misskey.note import Note
from misskey.context import Header


class Message(object):
    def __init__(self, data: Any, ws):
        data: dict = json.loads(data)
        self.type = data.get('type')
        self.header = Header(data.get('body', {}))
        if note := data.get('body', {}).get('body', None):
            self.note = Note(note, ws)
        else:
            data = data.get('body', {}).get('res', {}).get('createdNote', {})
            data['res'] = True
            self.note = Note(data, ws)
