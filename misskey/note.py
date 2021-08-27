import json
import re
from misskey.user import User


class Note(object):
    __slots__ = (
        'id',
        'created_at',
        'type',
        'user_id',
        'author',
        'text',
        'cw',
        'visibility',
        'visible_user_ids',
        'renote_count',
        'replies_count',
        'reactions',
        'emojis',
        'file_ids',
        'reply_id',
        'renote_id',
        'deleted_at',
        'uri',
        'ws'
    )

    def __init__(self, data, ws=None, text=None):
        self.ws = ws
        for attr in ('id', 'createdAt', 'userId', 'user', 'text', 'cw',
                     'visibility', 'renoteCount', 'repliesCount', 'reactions',
                     'emojis', 'fileIds', 'files', 'replyId',
                     'renoteId'
                     ):
            try:
                value = data[attr]
            except KeyError:
                continue
            else:  # エラーが発生しなかった場合は変数に追加
                if attr == 'user':
                    setattr(self, attr, User(value))
                else:
                    print(f'setattr(self,{attr}, {value})')
                    setattr(self, f'{attr}', f'{value}')

    def content(self, content):
        content = {
            'visibility': f"{content.get('visibility', self.visibility)}",
            'text': f"{content.get('text', '')}",
            'cw': content.get('cw'),
            'viaMobile': f"{content.get('viaMobile', 'false')}",
            'localOnly': f"{content.get('localOnly', 'false')}",
            'noExtractMentions': f"{content.get('noExtractMentions', 'false')}",
            'noExtractHashtags': f"{content.get('noExtractHashtags', 'false')}",
            'noExtractEmojis': f"{content.get('noExtractEmojis', 'false')}",
            'replyId': f"{content.get('replyId', self.id)}",
        }
        return content

    def create(self):
        self.ws.send('')

    def reply(self, content: dict = {}):
        content = self.content(content)
        self.ws.send(json.dumps(
            {
                'type': 'api',
                'body': {
                    'id': 'f8b2894d-1b5d-60f3-c9ea-60851f8e9730',
                    'endpoint': 'notes/create',
                    'data': content

                }
            }, ensure_ascii=False))
