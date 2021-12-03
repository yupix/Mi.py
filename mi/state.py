import asyncio
import json
from typing import Any, Callable, Dict, Iterator, Optional

from mi import User, UserProfile
from mi.chat import ChatContent
from mi.emoji import Emoji
from mi.iterators import InstanceIterator
from mi.note import NoteContent, ReactionContent
from mi.utils import api, get_module_logger, str_lower, upper_to_lower


class ConnectionState:
    def __init__(self, dispatch: Callable[..., Any]):
        self.dispatch = dispatch
        self.logger = get_module_logger(__name__)

    async def _parse_channel(self, message: Dict[str, Any]) -> None:
        """parse_channel is a function to parse channel event

        チャンネルタイプのデータを解析後適切なパーサーに移動させます

        Parameters
        ----------
        message : Dict[str, Any]
            Received message
        """
        base_msg = message['body']
        channel_type = str_lower(base_msg.get('type'))
        self.logger.debug(f'ChannelType: {channel_type}')
        await getattr(self, f'_parse_{channel_type}')(base_msg['body'])

    async def _parse_messaging_message(self, message: Dict[str, Any]) -> None:
        """
        チャットが来た際のデータを処理する関数
        """
        await self.dispatch('message', ChatContent(message))

    async def _parse_unread_messaging_message(self, message: Dict[str, Any]) -> None:
        """
        チャットが既読になっていない場合のデータを処理する関数
        """
        await self.dispatch('message', ChatContent(message))

    async def _parse_notification(self, message: Dict[str, Any]) -> None:
        """
        通知イベントを解析する関数
        
        Parameters
        ----------
        message: Dict[str, Any]
            Received message

        Returns
        -------
        None
        """
        notification_type = str_lower(message['type'])
        await getattr(self, f'_parse_{notification_type}')(message)

    async def _parse_unread_notification(self, message: Dict[str, Any]) -> None:
        """
        未読の通知を解析する関数

        Parameters
        ----------
        message : Dict[str, Any]
            Received message
        """
        notification_type = str_lower(message['type'])
        await getattr(self, f'_parse_{notification_type}')(message)

    async def _parse_reaction(self, message: Dict[str, Any]) -> None:
        """
        リアクションに関する情報を解析する関数
        """
        await self.dispatch('reaction', ReactionContent(message))

    async def _parse_note(self, message: Dict[str, Any]) -> None:
        """
        ノートイベントを解析する関数
        """
        await self.dispatch('message', NoteContent(message, self))

    async def on_emoji_add(self, message: dict):
        """
        emojiがインスタンスに追加された際のイベント

        Parameters
        ----------
        message

        Returns
        -------

        """
        await asyncio.create_task(
            self.dispatch("emoji_add", Emoji(
                message['body']['emoji']
            )))

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
            upper_to_lower(msg,
                           replace_list={"user": "author", "text": "content"})
        )
        await self.dispatch(message.id)
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
            upper_to_lower(msg,
                           replace_list={"user": "author", "text": "content"})
        )
        return asyncio.create_task(self.dispatch("chat", ctx))

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
            base_ctx["text"].replace(f"@{config.i.profile.username}",
                                     "").strip(" ")
        )
        return asyncio.create_task(
            self.dispatch("mention", NoteContent(**base_ctx))
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
            self.dispatch(
                "follow",
                Follow(
                    **upper_to_lower(message.get("body"),
                                     replace_list={"body": "user"})
                ),
            )
        )

    async def on_unfollow(self, message):
        pass

    async def on_reaction(self, message):
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
            self.dispatch("reaction", NoteContent(upper_to_lower(base_msg)))
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
        asyncio.create_task(self.dispatch("deleted", base_msg))

        # TODO: on_erroを実装

    async def on_close(self, web_socket):
        pass

    @staticmethod
    async def _get_i():
        res = api("/api/i", auth=True)
        return UserProfile(**upper_to_lower(json.loads(res.text)))

    def get_users(self,
                  limit: int = 10,
                  *,
                  offset: int = 0,
                  sort: Optional[str] = None,
                  state: str = 'all',
                  origin: str = 'local',
                  username: Optional[str] = None,
                  hostname: Optional[str] = None,
                  get_all: bool = False) -> Iterator[User]:
        return InstanceIterator(self).get_users(limit=limit, offset=offset, sort=sort, state=state, origin=origin, username=username, hostname=hostname, get_all=get_all)
