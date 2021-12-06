from websockets.legacy.client import WebSocketClientProtocol
from mi import Client, Drive, Note, Router
from mi.ext import tasks

uri = "wss://example.com/streaming"
token = "This is your token"
bot = Client()


@tasks.loop(60)
async def task():
    print("ループしてますよ～")


@bot.listen()
async def on_message(ctx: Note):
    print(
        f"{ctx.author.instance.name} | {ctx.author.username}さんがノートしました: {ctx.content}"
    )


@bot.listen()
async def on_reaction(ctx: Note):
    print(
        f"{ctx.author.instance.name} | {ctx.author.name}さんがリアクションを付けました: {ctx.reactions}"
    )


@bot.event()
async def on_ready(ws: WebSocketClientProtocol):
    print("work on my machine")
    await Router(ws).channels(["global", "main"])  # globalとmainチャンネルに接続
    task.start()  # タスクを起動
    res = bot.post_note("Hello World")  # ノートを投稿
    print(res.content)
    task.stop()  # タスクを止める
    res = Drive().upload("/home/example/example.png", "example.png")  # ドライブに画像をアップロード
    print(res.url)


bot.run(uri, token)
