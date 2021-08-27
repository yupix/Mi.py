# Mi.py

[![CodeFactor](https://www.codefactor.io/repository/github/yupix/mi.py/badge)](https://www.codefactor.io/repository/github/yupix/mi.py)
[![buddy pipeline](https://app.buddy.works/yupi0982/mi-py/pipelines/pipeline/345007/badge.svg?token=b304dd68d3eeb7917d453a2d2102621123ae4f05e0b659dde59cad486e2984b3 "buddy pipeline")](https://app.buddy.works/yupi0982/mi-py/pipelines/pipeline/345007)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_shield)

## 使い方

<details>
<summary>クラスを継承したBOT作り</summary>

```python
from misskey.ext import task
from misskey.reaction import Reaction
from misskey.message import Message
from misskey.router import Router
from misskey.bot import Bot


class SakuraAoi(Bot):

    @task.loop(60)
    async def task(self, ws):
        print(ws)
        print('ループしてますよ～')

    async def on_ready(self, ws):
        print('work on my machine')
        await Router(ws).channels(['global', 'main'])
        self.task.start()

    async def on_message(self, ws, ctx: Message):
        print(f'{ctx.note.author.instance.name} | {ctx.note.author.username}さんがノートしました: {ctx.note.text}')

    async def on_reacted(self, ws, ctx: Reaction):
        print(ctx.note.reaction)

    async def on_deleted(self, ws, ctx: Message):
        print(ctx)

    async def on_error(self, err):
        print(err)


if __name__ == '__main__':
    url = 'wss://exmaple.com/streaming'
    SakuraAoi().run(url, 'token')
```
</details>

<details>
<summary>インスタンス化してイベントを登録するスタイル</summary>

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
</details>

### Collaborators

<table>
    <tr>
        <td><img src="https://avatars.githubusercontent.com/u/50538210?s=120&v=4"></img></td>
    </tr>
    <tr>
        <td align="center"><a href="https://github.com/yupix">Author | @yupix</a></td>
    </tr>
</table>

### SpecialThanks

開発を手伝ってくれている方々です。

<table>
    <tr>
        <td><img src="https://avatars.githubusercontent.com/u/26793720?s=120&v=4"></img></td>
    </tr>
    <tr>
        <td align="center"><a href="https://github.com/Uraking-Github">Adviser | @Uraking</a></td>
    </tr>
</table>


# LICENSE

[Mi.py](LICENSE.md)  
[Credit](COPYING.md)  
[Third party](LICENSE/ThirdPartyLicense.md)

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_large)
