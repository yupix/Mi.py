import asyncio
import os
import random

from dotenv import load_dotenv
from loguru import logger
from mi.ext import commands
from mi.framework import Note
from mi.framework.router import Router
from mi.utils import check_multi_arg, get_unicode_emojis

load_dotenv()

env = os.environ
TOKEN = env.get("TOKEN")
URL = env.get("URL")

EXTENSIONS = ['cogs.basic']

if not check_multi_arg(TOKEN, URL):
    raise Exception("Please provide both TOKEN and URL")


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__()
        for extension in EXTENSIONS:
            self.load_extension(extension)

    async def on_drive_file_created(self, msg):
        print(msg)

    async def on_ready(self, ws):
        await Router(ws).connect_channel(['global', 'main'])
        logger.success('connected %s#%s' % (self.user.name, self.user.id))

    async def on_message(self, note: Note):
        # if note.emojis:
        #     unicode_emoji = get_unicode_emojis(note.content)
        #     emoji = random.choice([i.name for i in note.emojis] + unicode_emoji)
        #     await note.action.reaction.add(':%s:' % emoji)
        logger.info('%s: %s' % (note.author.name, note.content))


if __name__ == '__main__':
    bot = MyBot()
    asyncio.run(bot.start(URL, TOKEN))
