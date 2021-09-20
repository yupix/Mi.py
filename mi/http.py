"""
Mi.pyのWebSocket部分
"""

import asyncio
import json
import uuid
from typing import Any

import websockets

from mi.note import Follow, Note, Reaction
from mi.router import Router
from mi.utils import upper_to_lower


class WebSocket:
    """Misskey APIとやり取りを行うWebSocket object"""
    __slots__ = ['web_socket', 'cls', 'router', 'auth_i']

    def __init__(self, cls):
        self.web_socket = None
        self.cls = cls
        self.router: Router

    async def _run(self, uri):
        try:
            async with websockets.connect(uri) as web_socket:
                asyncio.create_task(self._on_ready(web_socket))
                while True:
                    await web_socket.send(json.dumps({'type': 'connect',
                                                      'body': {
                                                          'channel': 'main',
                                                          'id': f'{uuid.uuid4()}',
                                                          'params': {
                                                              'some': 'thing'
                                                          }
                                                      }}, ensure_ascii=False))
                    recv = await web_socket.recv()
                    asyncio.create_task(self._recv(web_socket, recv))
        except Exception as err:
            asyncio.create_task(self._on_error(err))

    async def _on_ready(self, web_socket):
        self.router = Router(web_socket)
        await self.cls.on_ready(web_socket)

    async def _recv(self, web_socket: Any, message: Any):
        """

        Parameters
        ----------
        web_socket :
        message :
        """
        message = json.loads(message)
        base_msg = message.get('body', None)
        if base_msg is None:
            return
        event_list = {'note': '_on_message', 'reacted': '_on_reacted', 'deleted': '_on_deleted', 'follow': '_on_follow',
                      'unfollow': '_on_unfollow', 'followed': '_on_follow', 'unreadNotification': '_on_unread_notification'}
        if base_msg['type'] == 'notification':  # follow等に必要
            await getattr(self, '_on_notification')(web_socket, message)
            return
        try:
            await getattr(self, f'{event_list.get(base_msg["type"])}')(web_socket, message)
        except AttributeError:
            print(base_msg['type'])

    async def _on_message(self, web_socket, message: Any) -> asyncio.Task:
        """
        Parameters
        ----------
        web_socket:
            WebSocket Instance
        message:
            Received message

        Returns
        -------
        task: asyncio.Task
        """
        msg = message.get('body', {}).get('body', {})
        message = Note(**upper_to_lower(msg))
        await self.router.capture_message(message.id)
        task = asyncio.create_task(self.cls.on_message(web_socket, message))

        return task

    async def _on_notification(self, web_socket, message: dict):
        pass

    async def _on_follow(self, web_socket, message: dict):
        task = asyncio.create_task(self.cls.on_follow(
            web_socket, Follow(**upper_to_lower(message.get('body'), replace_list={'body': 'user'}))))
        return task

    async def _on_unfollow(self, web_socket, message):
        pass

    async def _on_reacted(self, web_socket, message):
        base_msg = message.get('body', {}).get('body', {})
        base_msg['id'] = message.get('body', {}).get('id', None)
        asyncio.create_task(self.cls.on_reacted(
            web_socket, Reaction(**upper_to_lower(base_msg))))

    async def _on_deleted(self, web_socket, message):
        asyncio.create_task(self.cls.on_deleted(web_socket, Note(**message)))

    async def _on_error(self, err):
        await self.cls.on_error(err)

    async def _on_close(self, web_socket):
        pass
