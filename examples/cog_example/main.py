import asyncio
import os
import random

from dotenv import load_dotenv
from loguru import logger

from mi.ext import commands
from mi.framework import Note
from mi.framework.router import Router
from mi.utils import check_multi_arg, get_unicode_emojis
from mi.wrapper.file import MiFile

load_dotenv()

env = os.environ
TOKEN = env.get("TOKEN")
URL = env.get("URL")

EXTENSIONS = ['cogs.basic']

if not check_multi_arg(TOKEN, URL):
    raise Exception("Please provide both TOKEN and URL")


async def connect_channel(ws):
    await Router(ws).connect_channel(['global', 'main'])


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__()
        for extension in EXTENSIONS:
            self.load_extension(extension)

    async def on_drive_file_created(self, msg):
        print(msg)

    async def on_ready(self, ws):
        await connect_channel(ws)
        folder_name = 'test'
        await self.client.drive.folder.action.create(folder_name)
        folders = await self.client.drive.action.get_folders()
        folder = [i for i in folders if i.name == folder_name][0]

        await self.client.note.send('hello', files=[
            MiFile(path='/home/yupix/unknown.png', comment='test~', name="test", folder_id=folder.id),
            MiFile(file_id='123456789')
        ])
        logger.success(f'connected {self.user.name}#{self.user.id}')

    async def on_reconnect(self, ws):
        await connect_channel(ws)

    async def on_message(self, note: Note):
        if note.emojis:
            unicode_emoji = get_unicode_emojis(note.content)
            emoji = random.choice([i.name for i in note.emojis] + unicode_emoji)
            await note.action.reaction.add(f':{emoji}:')
        logger.info(f'{note.author.name}: {note.content}')


if __name__ == '__main__':
    bot = MyBot()
    asyncio.run(bot.start(URL, TOKEN))
