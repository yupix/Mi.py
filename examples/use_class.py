from mi import Drive, Note, Reaction
from mi.ext import commands, task
from mi.router import Router

uri = "wss://example.com/streaming"
token = "This is your token"
prefix = "tu!"


class MyBot(commands.Bot):
    def __init__(self, cmd_prefix):
        super().__init__(cmd_prefix)

    @task.loop(60)
    async def task(self, ws):
        print(ws)
        print("ループしてますよ～")

    async def on_ready(self, ws):
        print("work on my machine")
        await Router(ws).channels(["global", "main"])  # globalとmainチャンネルに接続
        self.task.start()  # タスクを起動する
        res = await Note(text="Hello~~~~~").send()  # ノートを投稿
        print(res.text)
        self.task.stop()  # タスクを止める
        res = Drive().upload(
            "/home/example/example.png", "example.png"
        )  # ドライブに画像をアップロード
        print(res.url)

    async def on_message(self, ctx: Note):
        print(
            f"{ctx.author.instance.name} | {ctx.author.username}さんがノートしました: {ctx.text}"
        )


if __name__ == "__main__":
    MyBot(prefix).run(uri, token)
