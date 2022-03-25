from __future__ import annotations

from typing import List, Optional

from mi import config
from mi.exception import NotExistRequiredData
from mi.framework.http import HTTPSession
from mi.framework.router import Route
from mi.utils import check_multi_arg


class AdminEmojiManager:
    def __init__(self, emoji_id: Optional[str] = None):
        self.emoji_id: Optional[str] = emoji_id

    @staticmethod
    async def add(
            file_id: Optional[str] = None,
            *,
            name: Optional[str] = None,
            url: Optional[str] = None,
            category: Optional[str] = None,
            aliases: Optional[List[str]] = None
    ) -> bool:
        if config.is_ayuskey:
            data = {'name': name, 'url': url, 'category': category, 'aliases': aliases}
        else:
            data = {'fileId': file_id}

        if not check_multi_arg(file_id, url):
            raise NotExistRequiredData('required a file_id or url')
        return bool(await HTTPSession.request(Route('POST', '/api/admin/emoji/add'), json=data, lower=True, auth=True))

    async def remove(self, emoji_id: Optional[str] = None) -> bool:
        emoji_id = emoji_id or self.emoji_id

        if emoji_id is None:
            raise NotExistRequiredData('idが不足しています')

        return bool(await HTTPSession.request(Route('POST', '/api/admin/emoji/remove'), json={'id': emoji_id}, lower=True,
                                              auth=True))
