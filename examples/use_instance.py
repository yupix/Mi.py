from misskey import Bot, Message, Router
from misskey.api import API

uri = 'wss://example.com/streaming'
token = 'This is your token'
conn = API(token, uri)
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
    res = await conn.note(text='Hello World').send()  # ノートを投稿
    print(res.note.text)


bot.run(uri, token)
