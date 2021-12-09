# Mi.py

[![CodeFactor](https://www.codefactor.io/repository/github/yupix/mi.py/badge)](https://www.codefactor.io/repository/github/yupix/mi.py)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f5acd9da804d4a11b031d36dbd398067)](https://www.codacy.com/gh/yupix/Mi.py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=yupix/Mi.py&amp;utm_campaign=Badge_Grade)
[![buddy pipeline](https://app.buddy.works/yupi0982/mi-py/pipelines/pipeline/345007/badge.svg?token=b304dd68d3eeb7917d453a2d2102621123ae4f05e0b659dde59cad486e2984b3 "buddy pipeline")](https://app.buddy.works/yupi0982/mi-py/pipelines/pipeline/345007)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_shield)  

## 概要

Mi.pyは[Discord.py](https://github.com/Rapptz/discord.py)
ライクな書き方ができるように作っているMisskeyApi wrapperです 現在動作を確認しているMisskeyは本家Misskey v12の最新です。
`Ayuskey` での動作確認も一応行っていますが、 11/5時点でAyuskeyそのものの動作が怪しいため現在はテストを行っていません。

## 使い方

様々な使い方を書くにあたってREADMEから変更しました。[こちら](examples)からご覧ください。 その他のメソッドなどについては[ドキュメント](https://mipy.readthedocs.io/) をご覧ください

## 注意点

グローバルタイムラインに接続したりする際に使う以下の様なコードがあるとホームタイムラインとグローバルタイムラインの2つを受信したことになりon_messageが2回動作します。 これは接続するチャンネルを増やすごとに増えていく形になります

```python
await Router(ws).channels(['home', 'global'])
```

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

### Libraries

- [Discord.py](https://github.com/Rapptz/discord.py)
    - 一部や仕組みを参考にさせてもらっています。実際にコードも利用しています 

最後にこのプロジェクトを作るきっかけになり、一部のコードを使用させていただいているDiscord.pyがArchivedになりました。 作者であるDannyさんや全てのコラボレーターに最大限の感謝申し上げます。

# LICENSE

[Mi.py](https://github.com/yupix/Mi.py/blob/master/LICENSE.md)  
[Credit](https://github.com/yupix/Mi.py/blob/master/COPYING.md)  
[Third party](https://github.com/yupix/Mi.py/blob/master/LICENSE/ThirdPartyLicense.md)

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMi.py.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMi.py?ref=badge_large)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/F2F36AA7M)
