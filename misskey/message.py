import json
from typing import Any

from misskey.note import Note
from misskey.context import Header


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
