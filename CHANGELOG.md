# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- `on_follow` イベントを追加しました

### Changed

- 内部的な変更で、`delete` `send`等のメソッドを別のクラスに分けました

### Removed

- `Message`クラスを削除しました。基本的に不要な情報があり、実装の複雑さが上がっているだけだからです。

### Fixed

- `add_reaction`の認証情報周りの不具合が修正されました

## [v0.1.0-1a] 2021-09-06

### Added

- `Note` `Message`クラスに`add_reaction`メソッドを追加
- `Note`, `Router`クラスにDocStringを追加
- `Note`クラスに`add_poll`メソッドを追加 (アンケート)
- `utils.py`に`upper_to_lower` `set_auth_i` `api`関数を追加
- `Note` `Message` クラスに`delete`メソッドを追加
- README.mdにドキュメントのURLを追加
- `user.py`に`UserProfile`クラスを追加
- `bot`クラスに`i`変数を追加(BOT自身のプロフィール)
- README.mdにcodacyのバッヂを追加

### Removed

- 一部でテスト用のprintが残っていたので削除
- `Note`クラスでwebsocketを受け取らないように
- `codecov.yml`はcodecovをサポートする予定がなくなったので削除

### Changed

- 内部的にon_messageとon_responseを切り替えるのに使用していた`res`はデフォルト値が出来たので判断方法を変更
- 内部的に`Note` `Message` `User` `Instance`等のクラスの引数をdictから詳細な物に変更
- `BotBase`クラスに`API`クラスをMixinする事でコネクションを別途用意する必要がなくなる様に
- `API` クラスから`note`メソッドを削除、代わりに`Note`クラスを追加
- `bool_to_string`をmiネームスペースから削除、今後は`mi.utils`で提供
- `note`から`User`や`Intance`等を個別のファイルに変更

### Fixed

- pypiからだとLICENSE等の相対リンクが動かないので絶対リンクに変更
- `Note` クラスのadd_filesで誤ってDeprecatedのmediaIdsを使っていたので`fileIds`に変更
- 多すぎるため詳細は書かないが、v12とayuskeyの差異を無くすために引数周りを大幅に修正
- Noteを送るだけなのに画像などのファイルが絶対に必要になっていたので修正
- Noteで画像だけを送ったりする際、文章が無いと送れないのを修正
- `upper_to_lower`で文字列に複数の大文字が含まれると一番最初の文字に置き換えてしまうのを修正 from [@uraking](https://github.com/Uraking-Github)
- `v12`だと多くの引数が足りずにメッセージが作成できないことを修正

## [v0.1.0a] 2021-09-01

### Added

- `API`クラスを追加しました
- `API`クラスに`note`, `drive` メソッドを追加しました
- util.pyに`bool_to_string`関数を追加しました
- `task`に`stop`メソッドを追加しました
- `Drive`クラスを追加しました
- `Drive`クラスに`upload`メソッドを追加しました
- 一部のメソッドや関数にDocStringを追加しました
- Noteクラスに`add_file`メソッドを追加しました

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

[v0.1.0-1a]: https://github.com/yupix/mi.py/compare/v0.1.0a...v0.1.0-1a
[v0.1.0a]: https://github.com/yupix/mi.py/compare/v0.0.1a...v0.1.0a
[v0.0.1a]: https://github.com/yupix/Mi.py/releases

[Unreleased]: https://github.com/yupix/mi.py/compare/master...HEAD
