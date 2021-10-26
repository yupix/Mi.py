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
from mi import config


class WebSocket:
    """Misskey APIとやり取りを行うWebSocket object"""

    __slots__ = ["web_socket", "cls", "router", "auth_i"]

    def __init__(self, cls):
        self.web_socket = None
        self.cls = cls
        self.router: Router

    async def run(self, uri):
        try:
            async with websockets.connect(uri) as web_socket:
                asyncio.create_task(self.on_ready(web_socket))
                while True:
                    await web_socket.send(
                        json.dumps(
                            {
                                "type": "connect",
                                "body": {
                                    "channel": "main",
                                    "id": f"{uuid.uuid4()}",
                                    "params": {"some": "thing"},
                                },
                            },
                            ensure_ascii=False,
                        )
                    )
                    recv = await web_socket.recv()
                    asyncio.create_task(self.recv(web_socket, recv))
        except Exception as err:
            asyncio.create_task(self._on_error(err))

    async def on_ready(self, web_socket):
        self.router = Router(web_socket)
        status = await self.cls.event_dispatch("ready", web_socket)
        if status:
            await self.cls.dispatch("ready", web_socket)

    async def recv(self, web_socket: Any, message: Any):
        """

        Parameters
        ----------
        web_socket :
        message :
        """
        message = json.loads(message)
        base_msg = message.get("body", None)
        if base_msg is None:
            return
        event_type = base_msg["type"]
        event_list = {
            "note": "on_message",
            "reacted": "on_reacted",
            "deleted": "on_deleted",
            "follow": "on_follow",
            "unfollow": "on_unfollow",
            "followed": "on_follow",
            "unreadNotification": "on_unread_notification",
            "mention": "on_mention",
        }
        if (
            event_type == "notification"
            or "unread" in event_type
            or event_list.get(event_type) is None
        ):
            await getattr(self, "on_notification")(web_socket, message)
            return

        await getattr(self, f"{event_list.get(event_type)}")(web_socket, message)

    async def on_message(self, web_socket, message: Any) -> asyncio.Task:
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
        msg = message.get("body", {}).get("body", {})
        message = Note(**upper_to_lower(msg))
        await self.router.capture_message(message.id)
        return asyncio.create_task(self.cls._on_message(message))

    async def on_notification(self, web_socket, message: dict):
        pass

    async def on_mention(self, web_socket, ctx: dict):
        base_ctx = ctx.get("body", {}).get("body")
        base_ctx["content"] = base_ctx["text"]
        base_ctx["text"] = (
            base_ctx["text"].replace(f"@{config.i.profile.username}", "").strip(" ")
        )
        return asyncio.create_task(
            self.cls.dispatch("mention", web_socket, Note(**base_ctx))
        )

    async def on_follow(self, web_socket, message: dict):
        return asyncio.create_task(
            self.cls.dispatch(
                "follow",
                web_socket,
                Follow(
                    **upper_to_lower(message.get("body"), replace_list={"body": "user"})
                ),
            )
        )

    async def on_unfollow(self, web_socket, message):
        pass

    async def on_reacted(self, web_socket, message):
        base_msg = message.get("body", {}).get("body", {})
        base_msg["id"] = message.get("body", {}).get("id", None)
        asyncio.create_task(
            self.cls.dispatch(
                "reacted", web_socket, Reaction(**upper_to_lower(base_msg))
            )
        )

    async def on_deleted(self, web_socket, message):
        asyncio.create_task(self.cls.dispatch("deleted", web_socket, Note(**message)))

    async def on_error(self, err):
        await self.cls.on_error(err)

    async def on_close(self, web_socket):
        pass
