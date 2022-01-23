import asyncio

from mi import Client, Note, Router
from mi.ext import tasks

uri = "wss://example.com/streaming"
token = "This is your token"
bot = Client()


@tasks.loop(60)
async def task():
    print("ループしてますよ～")


@bot.listen()
async def on_message(note: Note):
    print(
        f"{note.author.instance.name} | {note.author.username}さんがノートしました: {note.content}"
    )


@bot.listen()
async def on_reaction(ctx: Note):
    print(
        f"{ctx.author.instance.name} | {ctx.author.name}さんがリアクションを付けました: {ctx.reactions}"
    )


@bot.event()
async def on_ready(ws):
    print("work on my machine")
    await Router(ws).connect_channel(["global", "main"])  # globalとmainチャンネルに接続
    task.start()  # タスクを起動
    res = await bot.client.note.send("Hello World")  # ノートを投稿
    print(res.content)
    task.stop()  # タスクを止める


if __name__ == "__main__":
    asyncio.run(bot.start(uri, token))
