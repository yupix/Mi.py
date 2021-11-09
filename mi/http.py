"""
Mi.pyのWebSocket部分
"""

import asyncio
import json
import uuid
from typing import Any

import websockets

from mi import config
from mi.chat import ChatContent
from mi.note import Follow, NoteContent, Reaction
from mi.router import Router
from mi.utils import get_module_logger, upper_to_lower


class WebSocket:
    """Misskey APIとやり取りを行うWebSocket object"""

    __slots__ = ["web_socket", "cls", "router", "auth_i", "logger"]

    def __init__(self, cls):
        self.logger = get_module_logger(__name__)
        self.web_socket = None
        self.cls = cls
        self.router: Router

    async def run(self, uri: str) -> None:
        """
        WebSocketを起動してMisskeyインスタンスのセッションを確立します

        Parameters
        ----------
        uri : str

        Returns
        -------
        None
        """

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

    async def on_ready(self, web_socket) -> None:
        """
        Botの起動準備が完了した際にイベントを実行する関数

        Parameters
        ----------
        web_socket

        Returns
        -------
        None
        """

        self.router = Router(web_socket)
        await self.cls.event_dispatch("ready", web_socket)

    async def recv(self, web_socket: Any, message: Any):
        """
        WebSocketで受け取ったデータをparseして各イベントに分担する関数

        Parameters
        ----------
        web_socket :
        message :
        """
        message = json.loads(message)
        self.logger.debug(f"received: {message}")
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
            "messagingMessage": "on_chat",
        }
        self.logger.debug(f"received event: {event_type}")
        if (
            event_type == "notification"
            or "unread" in event_type
            or event_list.get(event_type) is None
        ):
            await self.on_notification(message)
            return

        await getattr(self, f"{event_list.get(event_type)}")(message)

    async def on_message(self, message: Any) -> asyncio.Task:
        """
        タイムラインに来たノートに関するイベントを発生させる関数

        Parameters
        ----------
        message:
            Received message

        Returns
        -------
        task: asyncio.Task
        """
        msg = message.get("body", {}).get("body", {})
        message = NoteContent(
            upper_to_lower(msg, replace_list={"user": "author", "text": "content"})
        )
        await self.router.capture_message(message.id)
        return asyncio.create_task(self.cls._on_message(message))

    async def on_chat(self, ctx):
        """
        チャットイベント

        Parameters
        ----------
        ctx

        Returns
        -------

        """
        msg = ctx.get("body", {}).get("body", {})
        ctx = ChatContent(
            upper_to_lower(msg, replace_list={"user": "author", "text": "content"})
        )
        return asyncio.create_task(self.cls.dispatch("chat", ctx))

    async def on_notification(self, message: dict):
        """
        通知イベント

        Parameters
        ----------
        message

        Returns
        -------

        """
        pass

    async def on_mention(self, ctx: dict) -> asyncio.Task:
        """
        メンションイベント

        Parameters
        ----------
        ctx : dict

        Returns
        -------
        asyncio.Task
        """

        base_ctx = ctx.get("body", {}).get("body")
        base_ctx["content"] = base_ctx["text"]
        base_ctx["text"] = (
            base_ctx["text"].replace(f"@{config.i.profile.username}", "").strip(" ")
        )
        return asyncio.create_task(
            self.cls.dispatch("mention", NoteContent(**base_ctx))
        )

    async def on_follow(self, message: dict) -> asyncio.Task:
        """
        フォローイベント

        Parameters
        ----------
        message

        Returns
        -------

        """
        return asyncio.create_task(
            self.cls.dispatch(
                "follow",
                Follow(
                    **upper_to_lower(message.get("body"), replace_list={"body": "user"})
                ),
            )
        )

    async def on_unfollow(self, message):
        pass

    async def on_reacted(self, message):
        """
        ノートのリアクションイベント

        Parameters
        ----------
        message:dict

        Returns
        -------
        None
        """

        base_msg = message.get("body", {}).get("body", {})
        base_msg["id"] = message.get("body", {}).get("id", None)
        asyncio.create_task(
            self.cls.dispatch("reacted", Reaction(**upper_to_lower(base_msg)))
        )

    async def on_deleted(self, message):
        """
        ノートの削除イベント

        Parameters
        ----------
        message

        Returns
        -------

        """
        base_msg = message.get("body", {}).get("body", {})
        asyncio.create_task(self.cls.dispatch("deleted", base_msg))

    async def on_error(self, err):
        await self.cls.on_error(err)

    async def on_close(self, web_socket):
        pass
