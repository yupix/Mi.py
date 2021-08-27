import json
from misskey.context import Header
from misskey.note import Note


class Reaction(object):
    def __init__(self, data):
        data = json.loads(data)
        self.header = Header(data.get('body', {}))
        self.note = ReactionNote(data.get('body'))


class ReactionNote(object):
    def __init__(self, data):
        self.reaction = data['body'].get('reaction')
        self.user_id = data['body'].get('userId')
