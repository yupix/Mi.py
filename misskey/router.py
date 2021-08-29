import json

from misskey import Message


class Router(object):
    def __init__(self, ws):
        self.ws = ws

    async def channels(self, channel_list: list):
        channel_dict = {'global': self.global_time_line, 'main': self.main_channel,
                        'home': self.home_time_line, 'local': self.local_time_line}
        try:
            for channel in channel_list:
                func = channel_dict.get(channel)
                await getattr(self, func.__name__)()
        except KeyError:
            pass

    async def global_time_line(self):
        await self.ws.send(json.dumps({
            'type': 'connect',
            'body': {
                'channel': 'globalTimeline',
                'id': 'foobar',
                'params': {
                    'some': 'thing'
                }
            }
        }, ensure_ascii=False))

    async def main_channel(self):
        await self.ws.send(json.dumps({
            'type': 'connect',
            'body': {
                'channel': 'main',
                'id': 'foobar',
                'params': {
                    'some': 'thing'
                }
            }
        }, ensure_ascii=False))

    async def home_time_line(self):
        await self.ws.send(json.dumps({
            'type': 'connect',
            'body': {
                'channel': 'homeTimeline',
                'id': 'foobar',
                'params': {
                    'some': 'thing'
                }
            }
        }, ensure_ascii=False))

    async def local_time_line(self):
        await self.ws.send(json.dumps({
            'type': 'connect',
            'body': {
                'channel': 'localTimeline',
                'id': 'oobar',
                'params': {
                    'some': 'ting'
                }
            }
        }, ensure_ascii=False))

    async def capture_message(self, message: Message):
        if hasattr(message, 'id'):
            await self.ws.send(json.dumps({
                'type': 'subNote',
                'body': {
                    'id': f'{message.note.id}'
                }
            }))
