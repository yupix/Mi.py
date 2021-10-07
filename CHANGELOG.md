# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [v0.2.5] 2021-10-07

### Added

- `conn.py` に `get_followers` `get_user` `fetch_user` 関数が追加されました
- `commandFrameWork` に関する多くのものを追加
- `commandFrameWork` に `listener` `commands` デコレーターを追加
- `Drive` クラスの `upload` メソッドでurlから画像をアップロードできるように `url` 引数を追加
- `utils.py` に `check_multi_arg` `remove_dict_empty` 関数を追加
- `upper_to_lower` 関数に `replace_list` 引数を追加
- `Follow` イベント時のユーザーに `follow` `unfollow` メソッドを追加しました
- `on_mention` イベントを追加しました
- `Author`クラスに `follow` `unfollow` `get_profile` メソッドを追加しました
- 複数の例外が追加されました

### Changed

- **破壊的変更**: `commandFrameWork` を使用しない場合の bot モジュールの名前を client に変更しました
    - 主にこれはDiscord.pyに近づけるためと `commandFrameWork` の bot モジュールとの差別化を目的としています
- `on_mention` イベントの `.text` に自分自身のメンションを含まないように、必要な場合は `content` をご利用ください
- デフォルトで接続するチャンネルを `globalTimeline` から `main` に変更しました。グローバルタイムラインを見る場合は `Router` をご利用ください
- `add_poll` の引数位置が変更されています。ご注意ください
- `delete` メソッドの引数を `_id` -> `note_id` に変更しました
- 内部変更: `api` 関数で使用されている `data` 引数は非推奨(Deprecated)に代わりに `json_data` を受け取るように
- 内部変更: `NoteAction` `UserAction` クラスのメソッドを大半をstaticmethodに置き換えしました
- 内部変更: `Note` クラスのメソッドの依存性を下げました
- 内部変更: `Follow` をモデルに変更しました
- 内部変更: イベントの発火に `dispatch` を用いるようになりました。 これにより `bot.py` から各イベントが削除されています

### Removed

- `UserProfile` クラスから `get_i` を削除しました。今後は`UserAction`から直接ご利用ください
- 内部変更: `dispatch` を使うことで `client.py` から `on_message` 等のクラスを削除

### Fixed

- チャンネルに接続する際にfoobarを使用していたのをuuid4動的に生成するように修正しました
- emojiライブラリがrequirementsに不足していた
- 循環インポートを修正しました
- `on_follow` イベントで `user` にアクセスできない不具合を修正

## [v0.1.5] 2021-09-13

### Added

- `on_follow` イベントを追加しました
- `utils.py` に `add_auth_i` 関数を追加しました
- `upper_to_lower` 関数でネストされたdictのkeyを全て小文字化できるようになりました
- `NoteAction` クラスに `emoji_count` メソッドを追加
- `config.py` を追加、auth_i等は全てここに保存するように
- `chart.py` を追加しました。
- `Drive` モデルに `DriveAction` クラスを継承させるように
- `DriveAction` クラスの `upload` メソッドの引数に `is_sensitive` と `force` を追加
- `utils.py` の `api` 関数で `files`  を受け取るように

### Changed

- 内部変更:  `delete` `send` 等のメソッドを別のクラスに分けました
- 内部変更: on_messageへの送信部分の条件式をres使わないように
- 内部変更: auth_iの共有方法を共通化
- 内部変更: auth_iの部分をconfig.iに置き換え
- `upload`メソッドの引数変更に伴う`add_file`の引数に`is_sensitive`と`force` を追加
- ほぼすべてのデータ格納用クラスをPydanticに置き換え( `Note`や`File` など)
- `get_i`を`UserAction` に移動

### Removed

- `auth_i`削除に伴い`api.py` を**削除**しました
- `set_auth_i` `add_auth_i` 関数を削除しました
- `AuthI` モデルを削除しました
- `auth_i` をクラスやメソッドなどの引数から削除しました
- `Message` クラスを削除しました。基本的に不要な情報があり、実装の複雑さが上がっているだけだからです。

### Fixed

- `add_reaction` の認証情報周りの不具合が修正されました
- ドキュメントでPydanticのモデルが表示できるようになりました
- `on_deleted` イベントが正常に動作しない既知の不具合を修正しました
- `api` 関数でデータがunicodeだと正常に動作しない場合があるのを修正

## [v0.1.0-1a] 2021-09-06

### Added

- `Note` `Message`クラスに`add_reaction` メソッドを追加
- `Note` , `Router` クラスにDocStringを追加
- `Note` クラスに `add_poll` メソッドを追加 (アンケート)
- `utils.py` に `upper_to_lower` `set_auth_i` `api` 関数を追加
- `Note` `Message` クラスに `delete` メソッドを追加
- README.mdにドキュメントのURLを追加
- `user.py` に `UserProfile` クラスを追加
- `bot` クラスに `i` 変数を追加(BOT自身のプロフィール)
- README.mdにcodacyのバッヂを追加

### Removed

- 一部でテスト用のprintが残っていたので削除
- `Note` クラスでwebsocketを受け取らないように
- `codecov.yml` はcodecovをサポートする予定がなくなったので削除

### Changed

- 内部的にon_messageとon_responseを切り替えるのに使用していた `res` はデフォルト値が出来たので判断方法を変更
- 内部的に `Note` `Message` `User` `Instance` 等のクラスの引数をdictから詳細な物に変更
- `BotBase` クラスに `API` クラスをMixinする事でコネクションを別途用意する必要がなくなる様に
- `API` クラスから `note` メソッドを削除、代わりに `Note` クラスを追加
- `bool_to_string` をmiネームスペースから削除、今後は `mi.utils` で提供
- `note` から`User` や `Intance` 等を個別のファイルに変更

### Fixed

- pypiからだとLICENSE等の相対リンクが動かないので絶対リンクに変更
- `Note` クラスのadd_filesで誤ってDeprecatedのmediaIdsを使っていたので `fileIds` に変更
- 多すぎるため詳細は書かないが、v12とayuskeyの差異を無くすために引数周りを大幅に修正
- Noteを送るだけなのに画像などのファイルが絶対に必要になっていたので修正
- Noteで画像だけを送ったりする際、文章が無いと送れないのを修正
- `upper_to_lower` で文字列に複数の大文字が含まれると一番最初の文字に置き換えてしまうのを修正 from [@uraking](https://github.com/Uraking-Github)
- `v12` だと多くの引数が足りずにメッセージが作成できないことを修正

## [v0.1.0a] 2021-09-01

### Added

- `API` クラスを追加しました
- `API`クラスに`note`, `drive` メソッドを追加しました
- util.pyに `bool_to_string` 関数を追加しました
- `task`に`stop` メソッドを追加しました
- `Drive` クラスを追加しました
- `Drive`クラスに`upload` メソッドを追加しました
- 一部のメソッドや関数にDocStringを追加しました
- Noteクラスに `add_file` メソッドを追加しました

### Removed

- note classからcontentとreply メソッドを削除しました

### Fixed

- setup.pyのrepositoryURLが間違っていたので修正
- __all__ に存在しなかった関数やクラスを追加しました

### Changed

- Tokenをbot classで保存するように
- Note classのsend メソッドの送信方法をwebsocketsからrequestsに変更
- CHANGELOG.mdの言語を今回から日本語に（CHANGELOGを書く時間が増すためです）
- README.mdからExampleを削除してExampleフォルダ内に移動しました
- **!BREAKING CHANGE**: noteに関する物を一つのファイルに纏めました、これによりインポートの変更が必要です。
- **!BREAKING CHANGE**: パッケージのファイル名をmisskeyからmi.pyに変更しました。これにより全てのインポートの変更が必要です。

## [v0.0.1a] 2021-08-27

### Added

- Added CHANGELOG.md.
- Added README.md.
- Added LICENSE.
- Added Each event method.

[v0.2.5]: https://github.com/yupix/mi.py/compare/v0.1.0-5...v0.2.5

[v0.1.5]: https://github.com/yupix/mi.py/compare/v0.1.0-1a...v0.1.0-5

[v0.1.0-1a]: https://github.com/yupix/mi.py/compare/v0.1.0a...v0.1.0-1a

[v0.1.0a]: https://github.com/yupix/mi.py/compare/v0.0.1a...v0.1.0a

[v0.0.1a]: https://github.com/yupix/Mi.py/releases

[Unreleased]: https://github.com/yupix/mi.py/compare/master...HEAD
