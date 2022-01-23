from abc import ABC, abstractmethod


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
