"""
Mi.pyのWebSocket部分
"""

import json
import asyncio
from typing import Any

import websockets

from mi import Message, Reaction
from mi.router import Router


class WebSocket:
    """Misskey APIとやり取りを行うWebSocket object"""
    __slots__ = ['web_socket', 'cls', 'router']

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
                                                          'channel': 'globalTimeline',
                                                          'id': 'foobar',
                                                          'params': {
                                                              'some': 'thing'
                                                          }
                                                      }}, ensure_ascii=False))
                    recv = await web_socket.recv()
                    asyncio.create_task(self._recv(web_socket, recv))
        except Exception as err:
            asyncio.create_task(self._on_error(err))

    async def _on_ready(self, web_socket):
        print('ready')
        self.router = Router(web_socket)
        await self.cls.on_ready(web_socket)

    async def _recv(self, web_socket: Any, message: Any):
        """

        Parameters
        ----------
        web_socket :
        message :
        """
        msg = Message(message, web_socket)
        event_list = {'note': '_on_message', 'reacted': '_on_reacted', 'deleted': '_on_deleted'}
        await getattr(self, f'{event_list.get(msg.header.type, "_on_message")}')(web_socket, message)

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
        message = Message(message, web_socket)
        await self.router.capture_message(message)
        if message.note.res is None:
            task = asyncio.create_task(self.cls.on_message(web_socket, message))
        else:
            task = asyncio.create_task(self.cls.on_response(web_socket, message))

        return task

    async def _on_reacted(self, web_socket, message):
        asyncio.create_task(self.cls.on_reacted(web_socket, Reaction(message)))

    async def _on_deleted(self, web_socket, message):
        asyncio.create_task(self.cls.on_deleted(web_socket, Message(message, web_socket)))

    async def _on_error(self, err):
        await self.cls.on_error(err)

    async def _on_close(self, web_socket):
        pass
