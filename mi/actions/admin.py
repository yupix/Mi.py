from typing import Optional

from mi.wrapper.emoji import AdminEmojiManager


class AdminActions:
    def __init__(self):
        self.emoji = AdminEmojiManager()

    @staticmethod
    def get_emoji_instance(emoji_id: Optional[str] = None) -> AdminEmojiManager:
        return AdminEmojiManager(emoji_id)
