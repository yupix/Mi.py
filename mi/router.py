"""
Misskeyのチャンネルへの接続や、メッセージのキャプチャ等のWebSocket関連
"""

import json
from typing import List
import uuid

from websockets.legacy.client import WebSocketClientProtocol


class Router:
    """
    Attributes
    ----------
    web_socket : WebSocketClientProtocol
        WebSocketクライアント

    Methods
    -------
    channels:
        与えられたlistを元にチャンネルに接続します
    global_time_line:
        WebSocketでGlobalTimeLineに接続します
    main_channel:
        WebSocketでMainチャンネルに接続します
    home_time_line:
        WebSocketでHomeTimeLineに接続します
    local_time_line:
        WebSocketでLocalTimeLineに接続します
    capture_message:
        与えられたメッセージを元にnote idを取得し、そのメッセージをon_message等の監視対象に追加します
    """

    def __init__(self, web_socket):
        self.web_socket = web_socket

    async def channels(self, channel_list: List[str]) -> None:
        """
        与えられたlistを元にチャンネルに接続します

        Parameters
        ----------
        channel_list : List
            ['global', 'local', 'home', 'main']

        Returns
        -------
        None: None
        """
        channel_dict = {
            "global": self.global_time_line,
            "main": self.main_channel,
            "home": self.home_time_line,
            "local": self.local_time_line,
        }
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
        await self.web_socket.send_json(
            {
                "type": "connect",
                "body": {
                    "channel": "globalTimeline",
                    "id": f"{uuid.uuid4()}",
                    "params": {"some": "thing"},
                },
            }
        )

    async def main_channel(self) -> None:
        """
        WebSocketでMainチャンネルに接続します

        Returns
        -------
        None: None
        """
        await self.web_socket.send_json(
            {
                "type": "connect",
                "body": {
                    "channel": "main",
                    "id": f"{uuid.uuid4()}",
                    "params": {"some": "thing"},
                },
            }
        )

    async def home_time_line(self) -> None:
        """
        WebSocketでHomeTimeLineに接続します

        Returns
        -------
        None: None
        """
        await self.web_socket.send_json(
            {
                "type": "connect",
                "body": {
                    "channel": "homeTimeline",
                    "id": f"{uuid.uuid4()}",
                    "params": {"some": "thing"},
                }
            }
        )

    async def local_time_line(self) -> None:
        """
        WebSocketでLocalTimeLineに接続します

        Returns
        -------
        None: None
        """
        await self.web_socket.send_json(
            {
                "type": "connect",
                "body": {
                    "channel": "localTimeline",
                    "id": f"{uuid.uuid4()}",
                    "params": {"some": "ting"},
                },
            }
        )

    async def capture_message(self, message_id: str) -> None:
        """
        与えられたメッセージを元にnote idを取得し、そのメッセージをon_message等の監視対象に追加します

        Parameters
        ----------
        message_id : str

        Returns
        -------
        None: None
        """
        await self.web_socket.send_json(
            {"type": "subNote", "body": {"id": f"{message_id}"}}
        )
