from misskey import Message, Reaction
from misskey.api import API
from misskey.ext import task
from misskey.router import Router
from misskey.bot import Bot

uri = 'wss://example.com/streaming'
token = 'This is your token'
conn = API(token, uri)


class MyBot(Bot):

    @task.loop(60)
    async def task(self, ws):
        print(ws)
        print('ループしてますよ～')

    async def on_ready(self, ws):
        print('work on my machine')
        await Router(ws).channels(['global', 'main'])
        self.task.start()  # タスクを起動する
        res = await conn.note(text='Hello~~~~~').send()  # ノートを投稿
        print(res.note.text)

    async def on_message(self, ws, ctx: Message):
        print(f'{ctx.note.author.instance.name} | {ctx.note.author.username}さんがノートしました: {ctx.note.text}')

    async def on_reacted(self, ws, ctx: Reaction):
        print(ctx.note.reaction)

    async def on_deleted(self, ws, ctx: Message):
        print(ctx)

    async def on_error(self, err):
        print(err)


if __name__ == '__main__':
    MyBot().run(uri, token)
