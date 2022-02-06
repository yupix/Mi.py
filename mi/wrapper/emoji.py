from __future__ import annotations

from typing import List, Optional

from mi.exception import NotExistRequiredData
from mi.framework.http import HTTPSession, Route


class EmojiManager:
    def __init__(
            self,
            emoji_id: Optional[str] = None
    ):
        self.emoji_id: Optional[str] = emoji_id

    async def add(self, name: str, url: str, category: Optional[str] = None, aliases: Optional[List[str]] = None):
        data = {'name': name, 'url': url, 'category': category, 'aliases': aliases}

        return bool(await HTTPSession.request(Route('POST', '/api/admin/emoji/add'), json=data, lower=True, auth=True))

    async def remove(self, emoji_id: Optional[str] = None) -> bool:
        emoji_id = emoji_id or self.emoji_id

        if emoji_id is None:
            raise NotExistRequiredData('idが不足しています')

        return bool(await HTTPSession.request(Route('POST', '/api/admin/emoji/remove'), json={'id': emoji_id}, lower=True,
                                              auth=True))
