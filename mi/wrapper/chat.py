from __future__ import annotations

from typing import Optional

from mi.framework.http import HTTPSession, Route
from mi.framework.models.chat import Chat
from mi.wrapper.models.chat import RawChat


class ChatManager:
    def __init__(self, user_id: Optional[str] = None, message_id: Optional[str] = None):
        self.__user_id = user_id
        self.__message_id = message_id

    async def send(
            self,
            text: Optional[str] = None,
            *,
            file_id: Optional[str] = None,
            user_id: Optional[str] = None,
            group_id: Optional[str] = None
    ) -> Chat:
        """
        Send chat.

        Parameters
        ----------
        text : Optional[str], default=None
            チャットのテキスト
        file_id : Optional[str], default=None
            添付するファイルのID
        user_id : Optional[str], default=None
            送信するユーザーのID
        group_id : Optional[str], default=None
            送信するグループのID
        """
        user_id = user_id or self.__user_id
        data = {'userId': user_id, 'groupId': group_id, 'text': text, 'fileId': file_id}
        res = await HTTPSession.request(Route('POST', '/api/messaging/messages/create'), json=data, auth=True, lower=True)
        return Chat(RawChat(res))

    async def delete(self, message_id: str) -> bool:
        """
        指定したidのメッセージを削除します。

        Parameters
        ----------
        message_id : str
            メッセージid

        Returns
        -------
        bool
            成功したか否か
        """

        message_id = message_id or self.__message_id
        args = {'messageId': f'{message_id}'}
        data = await HTTPSession.request(Route('POST', '/api/messaging/messages/delete'), json=args, auth=True)
        return bool(data)
