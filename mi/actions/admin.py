from typing import Optional

from mi.wrapper.ad import AdminAdvertisingManager
from mi.wrapper.emoji import AdminEmojiManager
from mi.wrapper.user import AdminUserManager


class AdminActions:
    def __init__(self):
        self.emoji = AdminEmojiManager()
        self.user = AdminUserManager()
        self.ad = AdminAdvertisingManager()

    @staticmethod
    def get_emoji_instance(emoji_id: Optional[str] = None) -> AdminEmojiManager:
        return AdminEmojiManager(emoji_id)
