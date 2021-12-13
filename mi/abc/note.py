from abc import ABC, abstractmethod
from typing import Optional


class AbstractNote(ABC):
    @abstractmethod
    def emoji_count(self) -> int:
        """
        ノートの本文にemojiが何個含まれているかを返します

        Returns
        -------
        int
            含まれている絵文字の数
        """

    @abstractmethod
    async def delete(self) -> bool:
        """
        指定したIDのノートを削除します

        returns
        -------
        is_success: bool
            成功したか否か
        status_code: int
            HTTP レスポンスステータスコード
        """
