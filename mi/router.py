"""
Misskeyのチャンネルへの接続や、メッセージのキャプチャ等のWebSocket関連
"""

import json

from mi import Message


class Router:
    """
    Attributes
    ----------
    web_socket : Any
        WebSocketクライアント
    """

    def __init__(self, web_socket):
        self.web_socket = web_socket

    async def channels(self, channel_list: list) -> None:
        """
        与えられたlistを元にチャンネルに接続します
        Parameters
        ----------
        channel_list : List[str]

        Returns
        -------
        None: None
        """
        channel_dict = {'global': self.global_time_line, 'main': self.main_channel,
                        'home': self.home_time_line, 'local': self.local_time_line}
        try:
            for channel in channel_list:
                func = channel_dict.get(channel)
                await getattr(self, func.__name__)()
        except KeyError:
            pass

    async def global_time_line(self) -> None:
        """
        WebSocketでGlobalTimeLineに接続します

        Returns
        -------
        None: None
        """
        await self.web_socket.send(json.dumps({
            'type': 'connect',
            'body': {
                'channel': 'globalTimeline',
                'id': 'foobar',
                'params': {
                    'some': 'thing'
                }
            }
        }, ensure_ascii=False))

    async def main_channel(self) -> None:
        """
        WebSocketでMainチャンネルに接続します
        Returns
        -------
        None: None
        """
        await self.web_socket.send(json.dumps({
            'type': 'connect',
            'body': {
                'channel': 'main',
                'id': 'foobar',
                'params': {
                    'some': 'thing'
                }
            }
        }, ensure_ascii=False))

    async def home_time_line(self) -> None:
        """
        WebSocketでHomeTimeLineに接続します
        Returns
        -------
        None: None
        """
        await self.web_socket.send(json.dumps({
            'type': 'connect',
            'body': {
                'channel': 'homeTimeline',
                'id': 'foobar',
                'params': {
                    'some': 'thing'
                }
            }
        }, ensure_ascii=False))

    async def local_time_line(self) -> None:
        """
        WebSocketでLocalTimeLineに接続します
        Returns
        -------
        None: None
        """
        await self.web_socket.send(json.dumps({
            'type': 'connect',
            'body': {
                'channel': 'localTimeline',
                'id': 'oobar',
                'params': {
                    'some': 'ting'
                }
            }
        }, ensure_ascii=False))

    async def capture_message(self, message: Message) -> None:
        """
        与えられたメッセージを元にnote idを取得し、そのメッセージをon_message等の監視対象に追加します

        Parameters
        ----------
        message : Message

        Returns
        -------

        """
        if hasattr(message, 'id'):
            await self.web_socket.send(json.dumps({
                'type': 'subNote',
                'body': {
                    'id': f'{message.note.id}'
                }
            }))
