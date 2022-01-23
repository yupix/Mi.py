from typing import List, Optional

from mi.types.emoji import Emoji as EmojiPayload


class RawEmoji:
    def __init__(self, data: EmojiPayload):
        self.id: Optional[str] = data.get('id')
        self.aliases: Optional[List[str]] = data.get('aliases')
        self.name: Optional[str] = data.get('name')
        self.category: Optional[str] = data.get('category')
        self.host: Optional[str] = data.get('host')
        self.url: Optional[str] = data.get('url')
