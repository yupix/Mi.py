import asyncio
from mi import Note
from mi.ext import commands, tasks
from mi.note import Note
from mi.router import Router

uri = "wss://example.com/streaming"
token = "This is your token"
prefix = "tu!"


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__()

    @tasks.loop(60)
    async def task(self):
        print("ループしてますよ～")

    async def on_ready(self, ws):
        print("work on my machine")
        await Router(ws).connect_channel(["global", "main"])  # globalとmainチャンネルに接続
        self.task.start()  # タスクを起動する
        res = self.client.note.send('hello world')
        print(res.content)
        self.task.stop()  # タスクを止める

    async def on_message(self, note: Note):
        instance_name = note.author.instance.name if note.author.instance else 'local'
        username = note.author.nickname or note.author.name
        if note.renote is None:
            print(f'{instance_name} | {username}: {note.content}')
        else:
            renote_name = note.renote.user.name
            print(f'{instance_name} | {username}: {note.content}\n    {renote_name}: {note.renote.content}')


if __name__ == "__main__":
    asyncio.run(MyBot().start(uri, token))
