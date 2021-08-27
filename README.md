# Mi.py

Discord.py ライクなMisskeyBot作り

## 使い方


### クラスを継承したBOT作り

```python
from misskey.ext import task
from misskey.reaction import Reaction
from misskey.message import Message
from loguru import logger
from misskey.router import Router
from misskey.bot import Bot
class SakuraAoi(Bot):

    @task.loop(60)
    async def task(self, ws):
        print(ws)
        print('ループしてますよ～')

    async def on_ready(self, ws):
        logger.info('work on my machine')
        await Router(ws).channels(['global', 'main'])
        self.task.start()

    async def on_message(self, ws, ctx: Message):
        logger.info(f'{ctx.note.author.instance.name} | {ctx.note.author.username}さんがノートしました: {ctx.note.text}')

    async def on_reacted(self, ws, ctx: Reaction):
        logger.info(ctx.note.reaction)

    async def on_deleted(self, ws, ctx: Message):
        logger.info(ctx)

    async def on_error(self, err):
        print(err)

if __name__ ==  '__main__':
    url = 'wss://exmaple.com/streaming'
    SakuraAoi().run(url, 'token')
```

### インスタンス化してイベントを登録するスタイル

```python
from misskey.message import Message
from misskey.router import Router
from misskey.bot import Bot

bot = Bot()


@bot.listen()
async def on_message(ws, ctx: Message):
    print(f'{ctx.note.author.instance.name} | {ctx.note.author.username}さんがノートしました: {ctx.note.text}')


@bot.listen()
async def on_reaction(ws, ctx):
    print(f'{ctx.note.author.instance.name} | {ctx.author.name}さんがリアクションを付けました: {ctx.note.text}')


@bot.event()
async def on_ready(ws):
    print('work on my machine')
    await Router(ws).channels(['global', 'main'])

bot.run('wss:/example.com', 'token')
```

# LICENSE

[Mi.py](LICENSE.md)  
[Third party](COPYING.md)
