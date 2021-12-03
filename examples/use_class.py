from websockets.legacy.client import WebSocketClientProtocol
from mi import Drive, Note
from mi.ext import commands, tasks
from mi.note import NoteContent
from mi.router import Router

uri = "wss://example.com/streaming"
token = "This is your token"
prefix = "tu!"


class MyBot(commands.Bot):
    def __init__(self, cmd_prefix: str):
        super().__init__(cmd_prefix)

    @tasks.loop(60)
    async def task(self):
        print("ループしてますよ～")

    async def on_ready(self, ws: WebSocketClientProtocol):
        print("work on my machine")
        await Router(ws).channels(["global", "main"])  # globalとmainチャンネルに接続
        self.task.start()  # タスクを起動する
        res = await Note("Hello~~~~~").send()  # ノートを投稿
        print(res.content)
        self.task.stop()  # タスクを止める
        res = Drive().upload(
            "/home/example/example.png", "example.png"
        )  # ドライブに画像をアップロード
        print(res.url)

    async def on_message(self, ctx: NoteContent):
        print(
            f"{ctx.author.instance.name} | {ctx.author.username}さんがノートしました: {ctx.content}"
        )


if __name__ == "__main__":
    MyBot(prefix).run(uri, token)
