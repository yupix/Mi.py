import asyncio
from mi import Note
from mi.ext import commands, tasks
from mi.note import Note
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

    async def on_ready(self, ws):
        print("work on my machine")
        await Router(ws).connect_channel(["global", "main"])  # globalとmainチャンネルに接続
        self.task.start()  # タスクを起動する
        res = await self.post_note("Hello~~~~~")  # ノートを投稿
        print(res.content)
        self.task.stop()  # タスクを止める

    async def on_message(self, note: Note):
        print(
            f"{note.author.instance.name} | {note.author.username}さんがノートしました: {note.content}"
        )


if __name__ == "__main__":
    asyncio.run(MyBot(prefix).start(uri, token))
