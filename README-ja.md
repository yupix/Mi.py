# Mi.py

<a><img src="https://img.shields.io/github/commit-activity/w/yupix/Mi.py"></a>
<a><img src="https://img.shields.io/pypi/dm/Mi.py?label=PyPI"></a>
[![CodeFactor](https://www.codefactor.io/repository/github/yupix/mi.py/badge)](https://www.codefactor.io/repository/github/yupix/mi.py)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f5acd9da804d4a11b031d36dbd398067)](https://www.codacy.com/gh/yupix/Mi.py/dashboard?utm_source=github.com&utm_medium=referral&utm_content=yupix/Mi.py&utm_campaign=Badge_Grade)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_shield)
<a href="https://discord.gg/CcT997U"><img src="https://img.shields.io/discord/530299114387406860?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
[![Join the chat at https://gitter.im/yupix/Mi.py](https://badges.gitter.im/yupix/Mi.py.svg)](https://gitter.im/yupix/Mi.py?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


## 概要

Mi.py は[Discord.py](https://github.com/Rapptz/discord.py)
ライクな書き方ができるように作っている MisskeyApi wrapper です

# サポートしているMisskey

- [Misskey Official v12](https://github.com/misskey-dev/misskey)
- [Ayuskey latest](https://gtihub.com/teamblackcrystal/misskey)

## 使い方

様々な使い方を書くにあたって README から変更しました。[こちら](examples)からご覧ください。 その他のメソッドなどについては[ドキュメント](https://yupix.github.io/Mi.py) をご覧ください

## 注意点

1. グローバルタイムラインに接続したりする際に使う以下の様なコードがあるとホームタイムラインとグローバルタイムラインの 2 つを受信したことになり on_message が 2 回動作します。
   これは接続するチャンネルを増やすごとに増えていく形になります

```python
await Router(ws).connect_channel(['home', 'global'])
```

2. v3.0.0はv2.0.0との互換性が極めて少ないです

3. このプロジェクトは基本SemVerに従ってバージョニングを行っていますが、X.X.X > X.9.9の式が成り立つ際(一番先頭のXは共通とする)は破壊的変更であるか問わずにリリースを行う次のメジャーバージョンまでのベータ版という扱いになっています。例としてあげると3.10.1などもベータ版に含まれることになります。

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
        <td align="center">
            <img src="https://avatars.githubusercontent.com/u/26793720?s=120&v=4" alt="uraking"/>
        </td>
        <td align="center">
            <img src="https://avatars.githubusercontent.com/u/33174568?s=120&v=4" alt="sousuke0422"/>
        </td>
        <td align="center">
            <img src="https://avatars.githubusercontent.com/u/96478337?s=120&v=4" alt="sousuke0422"/>
        </td>
    </tr>
    <tr>
        <td><a href="https://github.com/Uraking-Github">Adviser  ｜ @Uraking</a></td>
        <td><a href="https://github.com/sousuke0422"> Documentation｜ @sousuke0422</a></td>
        <td><a href="https://github.com/fotoente"> Translation｜ @fotoente</a></td>
    </tr>
</table>

### Libraries

- [Discord.py](https://github.com/Rapptz/discord.py)
    - 一部や仕組みを参考にさせてもらっています。実際にコードも利用しています

最後にこのプロジェクトを作るきっかけになり、一部のコードを使用させていただいている Discord.py が Archived になりました。 作者である Danny さんや全てのコラボレーターに最大限の感謝申し上げます。

## Mi.pyを使って作成されたプロジェクト

- [Misskey Ebooks Bot](https://github.com/fotoente/MIsskey-ebooks-bot)
- [Misskey Bot CeilingFox](https://github.com/fotoente/MIsskey-ebooks-bot)

# LICENSE

[Mi.py](https://github.com/yupix/Mi.py/blob/master/LICENSE.md)  
[Credit](https://github.com/yupix/Mi.py/blob/master/COPYING.md)  
[Third party](https://github.com/yupix/Mi.py/blob/master/LICENSE/ThirdPartyLicense.md)

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_large)

<p align="center">
    <a href="https://yupix.github.io/Mi.py/en">Documentation</a>
    *
    <a href="https://discord.gg/CcT997U">Discord Server</a>
</p>

