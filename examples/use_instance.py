from websockets.legacy.client import WebSocketClientProtocol
from mi import Client, Drive, Note, Router
from mi.ext import tasks
from mi.note import NoteContent

uri = "wss://example.com/streaming"
token = "This is your token"
bot = Client()


@tasks.loop(60)
async def task():
    print("ループしてますよ～")


@bot.listen()
async def on_message(ctx: NoteContent):
    print(
        f"{ctx.author.instance.name} | {ctx.author.username}さんがノートしました: {ctx.content}"
    )


@bot.listen()
async def on_reaction(ctx):
    print(
        f"{ctx.note.author.instance.name} | {ctx.author.name}さんがリアクションを付けました: {ctx.note.text}"
    )


@bot.event()
async def on_ready(ws: WebSocketClientProtocol):
    print("work on my machine")
    await Router(ws).channels(["global", "main"])  # globalとmainチャンネルに接続
    task.start()  # タスクを起動
    res = await Note("Hello World").send()  # ノートを投稿
    print(res.content)
    task.stop()  # タスクを止める
    res = Drive().upload("/home/example/example.png", "example.png")  # ドライブに画像をアップロード
    print(res.url)


bot.run(uri, token)
