import json
import asyncio
from typing import Any

import websockets

from misskey import Message, Reaction
from misskey.router import Router


class WebSocket(object):
    """Misskey APIとやり取りを行うWebSocket object"""
    __slots__ = ['ws', 'cls', 'router']

    def __init__(self, cls):
        self.ws = None
        self.cls = cls
        self.router: Router

    async def _run(self, uri):
        try:
            async with websockets.connect(uri) as ws:
                asyncio.create_task(self._on_ready(ws))
                while True:
                    await ws.send(json.dumps({'type': 'connect',
                                              'body': {
                                                  'channel': 'globalTimeline',
                                                  'id': 'foobar',
                                                  'params': {
                                                      'some': 'thing'
                                                  }
                                              }}, ensure_ascii=False))
                    recv = await ws.recv()
                    asyncio.create_task(self._recv(ws, recv))
        except Exception as err:
            asyncio.create_task(self._on_error(err))

    async def _on_ready(self, ws):
        print('ready')
        self.router = Router(ws)
        await self.cls.on_ready(ws)

    async def _recv(self, ws: Any, message: Any):
        """

        Parameters
        ----------
        ws :
        message :
        """
        msg = Message(message, ws)
        event_list = {'note': '_on_message', 'reacted': '_on_reacted', 'deleted': '_on_deleted'}
        await getattr(self, f'{event_list.get(msg.header.type, "_on_message")}')(ws, message)

    async def _on_message(self, ws, message: Any) -> asyncio.Task:
        """
        Parameters
        ----------
        ws:
            WebSocket Instance
        message:
            Received message

        Returns
        -------
        task: asyncio.Task
        """
        message = Message(message, ws)
        await self.router.capture_message(message)
        if not hasattr(message.note, 'res'):
            task = asyncio.create_task(self.cls.on_message(ws, message))
        else:
            task = asyncio.create_task(self.cls.on_response(ws, message))

        return task

    async def _on_reacted(self, ws, message):
        asyncio.create_task(self.cls.on_reacted(ws, Reaction(message)))

    async def _on_deleted(self, ws, message):
        asyncio.create_task(self.cls.on_deleted(ws, Message(message, ws)))

    async def _on_error(self, err):
        await self.cls.on_error(err)

    async def _on_close(self, ws):
        pass
