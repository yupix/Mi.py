from typing import Optional

from mi.framework.http import HTTPSession
from mi.framework.router import Route
from mi.wrapper.ad import AdminAdvertisingManager
from mi.wrapper.emoji import AdminEmojiManager
from mi.wrapper.moderator import AdminModeratorManager
from mi.wrapper.user import AdminUserManager


class AdminActions:
    def __init__(self):
        self.emoji = AdminEmojiManager()
        self.user = AdminUserManager()
        self.ad = AdminAdvertisingManager()
        self.moderator = AdminModeratorManager()

    @staticmethod
    def get_emoji_instance(emoji_id: Optional[str] = None) -> AdminEmojiManager:
        return AdminEmojiManager(emoji_id)

    @staticmethod
    async def get_invite() -> bool:
        return bool(await HTTPSession.request(Route('POST', '/api/admin/invite')))
