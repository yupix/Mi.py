from typing import List

from mi.types.emoji import Emoji as EmojiPayload


class Emoji:
    def __init__(self, data: EmojiPayload):
        self.id: str = data.get('id')
        self.aliases: List[str] = data.get('aliases')
        self.name: str = data.get('name')
        self.category: str = data.get('category')
        self.host: str = data.get('host')
        self.url: str = data.get('url')
