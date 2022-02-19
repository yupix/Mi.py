# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [v3.9.9] 2022-02-19

### Added

- added `ActiveUsersChartPayload` class
- added `DriveLocalChartPayload` class
- added `DriveRemoteChartPayload` class
- added `DriveChartPayload` class
- added `RawDriveLocalChart` class
- added `RawDriveRemoteChart` class
- added `RawDriveChart` class
- added `RawActiveUsersChart` class
- added `ChartManager` class
- added `get_user` method to`FollowRequestManager` class
- feat: ClientActionsクラスに`chart`変数を追加
- `Context` クラスを追加しました

### Changed

- Changed the attribute `i` to `user` to access the bot itself
- モデルに `__slots__` を定義しました
    - 副次的な効果としてメモリの使用量などが低下します

### Fixed

- `FollowManager` クラスの `remove` メソッドがうまく動かない

## [v3.3.0] 2022-01-25

### Added

- `get_files` メソッドを追加しました。
    - **It will be changed to a generator in the next update.**

## [v3.2.1] 2022-01-24

### Fixed

- `mention_command` が複数登録できない不具合を修正しました

## [v3.2.0] 2022-01-24

### Added

- type hint

### Fixed

- 以下の Note クラスのメソッドで note_id が必須になっていたのを修正
    - `add_clips`
    - `create_renote`
    - `create_quote`
    - `get_note`
    - `get_replies`
    - `get_reaction`
    - `delete`
- 以下の引数が正常な動作になりました
    - `noExtractMentions`
    - `noExtractHashtags`
    - `noExtractEmojis`

## [v3.1.0] 2022-01-23

### Added

- Added `get_mention` method to `UserActions` class

### Fixed

- properties が存在しない場合にエラーが出る

## [v3.0.1] 2022-01-23

### Fixed

- user.py で Instance クラスが読み込めてない

## [v3.0.0] 2022-01-23

### Added

- added `ChatManager` class
- added `RawReaction` class
- added `RawChat` class
- added `EmojiManager` class
- added `FolderManager` class
- added `DriveManager` class
- added `text` arg to mention_command
- added `RawNote` class
- added `RawRenote` class
- added `RawEmoji` class
- added `RawProperties` class
- added `RawFolder` class
- added `RawFile` class
- added `RawPollChoices` class
- added `RawPoll` class
- added `RawInstance` class
- added `RawUserDetails` class
- added `RawUser` class
- added `FavoriteManager` class
- added `FollowManager` class
- added FollowRequestManager class

### Changed

- updated a examples
- ドキュメントを更新
- 内部変更: `UserActions` や `ClientActions` のメソッドを別クラスに分割
- Allow only property-based access to most data classes.
- **BREAKING CHANGE**: `User` クラスのプロパティーを以下のように変更
    - `name` -> `nickname`
    - `username` -> `name`
- **BREAKING CHANGE**: `User` クラスの `follow` `unfollow` メソッドを削除
    - 今後は `User` クラスの `action` メソッドから `add` `remove` メソッドを使用できます
- **BREAKING CHANGE**: モデル名の変更 `Following` -> `Follower`
- **BREAKING CHANGE**: モデル名の変更 `Follower` -> `Followee`
- **BREAKING CHANGE**: モデルの\_state 属性を\_\_state に変更
- **BREAKING CHANGE**: `Following` クラスのメソッドを以下のとおりに変更
    - `accept_request` -> `accept`
    - `reject_request` -> `reject`
    - `follow` -> `add`
    - `remove_follow` -> `remove`

## Removed

- Unused class UserDetails
    - from now on use `RawUserDetails`
- Unused file view.py
- **BREAKING CHANGE**: removed `post_note` method
    - from now on use `self.client.note.send`
- **BREAKING CHANGE**: removed `note_delete` method
    - from now on use `self.client.note.delete`

## [v2.1.0-alpha] 2021-12-30

### Fixed

- ドキュメントのバージョン

## [v2.1.0] 2021-12-30

### Added

- Pass the regular expression retrieved by `mention_command` as a function argument

### Fixed

- I used a list as the default argument.
- The `fetch_user` method is not doing a return.
- DocString

### Changed

- command_prefix is no longer used, it will be removed from the argument in **v3.0.0**

## Removed

- Unused arguments

## [v2.0.0] 2021-12-29

### Added

- `commands.mention_command` を追加しました MP-8
- `get_replies` and `get_note` method to `Class` class MP-10 MP-9
- `get_replies` method to `Note` class MP-10 MP-9
- `get_replies` and `get_note` method to `NoteActions` class MP-10 MP-9

### Removed

- **BREAKING CHANGE**: removed core.py and context.py MP-8
- **BREAKING CHANGE**: Cog に関連する多くのクラスを削除しました MP-8
- **BREAKING CHANGE**: `commands.command` デコレータを削除しました MP-8

## [v1.0.3] 2021-12-27

### Added

- add `create_renote` and `create_quote` method to `Note` class
- add `create_renote` and `create_quote` method to `NoteActions` class
- add event `on_user_follow`

### Changed

- The following classes no longer inherit from `BaseModel`
    - Properties
    - Folder
    - File
    - Channel
    - PinnedNote
    - PinnedPage
    - FieldContent
- internal change: optimizing import
- internal change: Renamed `PinnedPage` to `PinnedNote`
- **BREAKING CHANGE**: Moved the post_note method of ConnectionState to NoteActions

### Removed

- removed appveyor.yml
- **BREAKING CHANGE**: Removed api function in utils.py
- **BREAKING CHANGE**: Removed pydantic from dependencies

### Fixed

- Fixed a bug that prevented the correct use of poll in the post_note method.
- Corrected the attribute name of User class to the correct one
- Fixed typo in reconnect argument of start method

## [v1.0.2] 2021-12-24

### Added

- add event `on_follow` and `follow_request`
- add a new `Following` and `UserActions` class
- add `accept_request` and `reject_request` method to `Following` class
- add `accept_following_request` and `reject_following_request` method to `UserActions` class

### Fixed

- Fixed a problem where renote would say the key was missing.

## [v1.0.1] 2021-12-24

### Added

- add event `on_mention`
- add `favorite`, `add_to_clips`, `add_reaction` and `remove_favorite` method to `Note` class
- add `favorite`, `add_note_to_clips`, `add_reaction_to_note` and `remove_favorite` method to `NoteAction` class
- add class
    - NoteActions
    - ClientActions

### Fixed

- fixed a bug where json arguments were replaced with data in requests.

## [v1.0.0] 2021-12-23

### Added

- `Note` クラスに `reply` メソッドを追加しました
- 以下のクラスを追加
    - MisskeyWebSocket
    - MisskeyClientWebSocketResponse
    - Route
    - HTTPClient
- Client に以下のメソッドを追加
    - post_chat
    - delete_chat
    - post_note
        - 今後のノート投稿はこちらを使用してください
    - delete_note
    - get_instance
    - fetch_instance
    - get_user
    - fetch_user
    - upload_file
- `rich` を使ったデバッグ機能を追加しました
- `file_upload` 関数を追加しました
- `run` メソッドに `debug` 引数を追加しました
- DocString を一部追加しました
- 抽象基底クラスを追加しました
- TypedDict を追加しました
- チャットをする際に用いる `Chat` `ChatContent` クラスを追加しました
- `on_chat` イベントを追加しました
- ~~`NoteContent` クラスを追加しました~~
  ~~- ノートの受信イベントでは基本このクラスが使用されます。~~
- `Instance` クラスに `get_users` メソッドを追加しました

### Changed

- api 周りでのエラー出力が分かりやすくなりました
- ~~今までの `Note` クラスに当たるものを `NoteContent` に変更し別途 `Note` クラスを作成させるようにしました~~
    - ~~これは不要なデータなどを生成しないようにすることが目的です。~~
- 部分的に Pydantic を廃止
    - 素直に使わないほうが部分的に楽だから
- `Drive` クラスの `upload` メソッドで例外 `InvalidParameters` を発生させるようにしました
    - これは`to_file`, `to_url` の両方がないと変数が定義されず、`Drive`クラスの生成に失敗する可能性があるからです。
- `get_user` メソッドが 非同期になりました。
- 内部変更: `utils.py` の一部を Cython を用いたものに変更
- 内部変更: `DriveAction` を廃止し, `file_upload` を使用するように
- 内部変更: `event_dispatch` でクラスにイベントがある場合呼び出すようにしました
- 内部変更: シングルクォーテーションをダブルクォーテーションに変更しました
- 内部変更: cog システムを作り直しました
- 内部変更: websocket に関連する部分を作り直しました
- 内部変更: イベントの発火部分を作り直しました
- 内部的変更: `dispatch` に関連する物を非同期から同期に変更しました
- **破壊的変更**: 使用しているライブラリを `websockets` から `aiohttp` に変更しました
- **破壊的変更**: `Router` クラスの `channels` メソッドを `connect_channel` に変更しました
- **破壊的変更**: task を tasks に変更しました
- **破壊的変更**: `on_ready` を除き websocket を引数で渡さないようになりました
- **破壊的変更**: `Note` クラスの `text` 変数を `content` と統合しました
- **破壊的変更**: `Reaction` クラスと `ReactionContent` を結合させました
- **破壊的変更**: `Chat` クラスと `ChatContent` を結合させました
- **破壊的変更**: `Drive` クラスの `upload` メソッドで使用できる引数名を変更、キーワード引数を強制するようにしました。
    - 引数名の変更は次の通りです `url` => `to_url`, `path` => `to_file`
    - 強制されるキーワード引数は次の通りです `force`, `is_sensitive`

### Fixed

- \_\_on_error が動かない不具合を修正しました
- 一部の誤った typing hint を修正
- バグの原因になるコードを修正

### Removed

- `Router` クラスから以下のメソッドを削除しました
    - main_channel
    - home_time_line
    - local_time_line
    - global_time_line
- クラスの削除について
    - `ChatContent`
    - `ReactionContent`
    - `NoteContent`
    - `UserActions`
    - `UserProfile`
        - `UserProfile`にあったものは `User` に統合され、詳細な情報は `User` クラスの details オブジェクト(`UserDetails`) から取得可能です
- **破壊的変更**: `WebSocket` クラスを削除しました
    - 今後は aiohttp の `ws_connect` メソッドを使用します
- **破壊的変更**: `requests` ライブラリを削除しました
    - 今後は aiohttp の `request` メソッドを使用します

## [v0.2.5] 2021-10-07

### Added

- `conn.py` に `get_followers` `get_user` `fetch_user` 関数が追加されました
- `commandFrameWork` に関する多くのものを追加
- `commandFrameWork` に `listener` `commands` デコレータを追加
- `Drive` クラスの `upload` メソッドで url から画像をアップロードできるように `url` 引数を追加
- `utils.py` に `check_multi_arg` `remove_dict_empty` 関数を追加
- `upper_to_lower` 関数に `replace_list` 引数を追加
- `Follow` イベント時のユーザーに `follow` `unfollow` メソッドを追加しました
- `on_mention` イベントを追加しました
- `User`クラスに `follow` `unfollow` `get_profile` メソッドを追加しました
- 複数の例外が追加されました

### Changed

- **破壊的変更**: `commandFrameWork` を使用しない場合の bot モジュールの名前を client に変更しました
    - 主にこれは Discord.py に近づけるためと `commandFrameWork` の bot モジュールとの差別化を目的としています
- `on_mention` イベントの `.text` に自分自身のメンションを含まないように、必要な場合は `content` をご利用ください
- デフォルトで接続するチャンネルを `globalTimeline` から `main` に変更しました。グローバルタイムラインを見る場合は `Router` をご利用ください
- `add_poll` の引数位置が変更されています。ご注意ください
- `delete` メソッドの引数を `_id` -> `note_id` に変更しました
- 内部変更: `api` 関数で使用されている `data` 引数は非推奨(Deprecated)に代わりに `json_data` を受け取るように
- 内部変更: `NoteAction` `UserActions` クラスのメソッドを大半を staticmethod に置き換えしました
- 内部変更: `Note` クラスのメソッドの依存性を下げました
- 内部変更: `Follow` をモデルに変更しました
- 内部変更: イベントの発火に `dispatch` を用いるようになりました。 これにより `bot.py` から各イベントが削除されています

### Removed

- `UserProfile` クラスから `get_i` を削除しました。今後は`UserActions`から直接ご利用ください
- 内部変更: `dispatch` を使うことで `client.py` から `on_message` 等のクラスを削除

### Fixed

- チャンネルに接続する際に foobar を使用していたのを uuid4 動的に生成するように修正しました
- emoji ライブラリが requirements に不足していた
- 循環インポートを修正しました
- `on_follow` イベントで `user` にアクセスできない不具合を修正

## [v0.1.5] 2021-09-13

### Added

- `on_follow` イベントを追加しました
- `utils.py` に `add_auth_i` 関数を追加しました
- `upper_to_lower` 関数でネストされた dict の key を全て小文字化できるようになりました
- `NoteAction` クラスに `emoji_count` メソッドを追加
- `config.py` を追加、auth_i 等は全てここに保存するように
- `chart.py` を追加しました。
- `Drive` モデルに `DriveAction` クラスを継承させるように
- `DriveAction` クラスの `upload` メソッドの引数に `is_sensitive` と `force` を追加
- `utils.py` の `api` 関数で `files` を受け取るように

### Changed

- 内部変更: `delete` `send` 等のメソッドを別のクラスに分けました
- 内部変更: on_message への送信部分の条件式を res 使わないように
- 内部変更: auth_i の共有方法を共通化
- 内部変更: auth_i の部分を config.i に置き換え
- `upload`メソッドの引数変更に伴う`add_file`の引数に`is_sensitive`と`force` を追加
- ほぼすべてのデータ格納用クラスを Pydantic に置き換え( `Note`や`File` など)
- `get_i`を`UserActions` に移動

### Removed

- `auth_i`削除に伴い`api.py` を**削除**しました
- `set_auth_i` `add_auth_i` 関数を削除しました
- `AuthI` モデルを削除しました
- `auth_i` をクラスやメソッドなどの引数から削除しました
- `Message` クラスを削除しました。基本的に不要な情報があり、実装の複雑さが上がっているだけだからです。

### Fixed

- `add_reaction` の認証情報周りの不具合が修正されました
- ドキュメントで Pydantic のモデルが表示できるようになりました
- `on_deleted` イベントが正常に動作しない既知の不具合を修正しました
- `api` 関数でデータが unicode だと正常に動作しない場合があるのを修正

## [v0.1.0-1a] 2021-09-06

### Added

- `Note` `Message`クラスに`add_reaction` メソッドを追加
- `Note` , `Router` クラスに DocString を追加
- `Note` クラスに `add_poll` メソッドを追加 (アンケート)
- `utils.py` に `upper_to_lower` `set_auth_i` `api` 関数を追加
- `Note` `Message` クラスに `delete` メソッドを追加
- README.md にドキュメントの URL を追加
- `user.py` に `UserProfile` クラスを追加
- `bot` クラスに `i` 変数を追加(BOT 自身のプロフィール)
- README.md に codacy のバッヂを追加

### Removed

- 一部でテスト用の print が残っていたので削除
- `Note` クラスで websocket を受け取らないように
- `codecov.yml` は codecov をサポートする予定がなくなったので削除

### Changed

- 内部的に on_message と on_response を切り替えるのに使用していた `res` はデフォルト値が出来たので判断方法を変更
- 内部的に `Note` `Message` `User` `Instance` 等のクラスの引数を dict から詳細な物に変更
- `BotBase` クラスに `API` クラスを Mixin する事でコネクションを別途用意する必要がなくなる様に
- `API` クラスから `note` メソッドを削除、代わりに `Note` クラスを追加
- `bool_to_string` を mi ネームスペースから削除、今後は `mi.utils` で提供
- `note` から`User` や `Intance` 等を個別のファイルに変更

### Fixed

- pypi からだと LICENSE 等の相対リンクが動かないので絶対リンクに変更
- `Note` クラスの add_files で誤って Deprecated の mediaIds を使っていたので `fileIds` に変更
- 多すぎるため詳細は書かないが、v12 と ayuskey の差異を無くすために引数周りを大幅に修正
- Note を送るだけなのに画像などのファイルが絶対に必要になっていたので修正
- Note で画像だけを送ったりする際、文章が無いと送れないのを修正
- `upper_to_lower` で文字列に複数の大文字が含まれると一番最初の文字に置き換えてしまうのを修正 from [@uraking](https://github.com/Uraking-Github)
- `v12` だと多くの引数が足りずにメッセージが作成できないことを修正

## [v0.1.0a] 2021-09-01

### Added

- `API` クラスを追加しました
- `API`クラスに`note`, `drive` メソッドを追加しました
- util.py に `bool_to_string` 関数を追加しました
- `task`に`stop` メソッドを追加しました
- `Drive` クラスを追加しました
- `Drive`クラスに`upload` メソッドを追加しました
- 一部のメソッドや関数に DocString を追加しました
- Note クラスに `add_file` メソッドを追加しました

### Removed

- note class から content と reply メソッドを削除しました

### Fixed

- setup.py の repositoryURL が間違っていたので修正
- **all** に存在しなかった関数やクラスを追加しました

### Changed

- Token を bot class で保存するように
- Note class の send メソッドの送信方法を websockets から requests に変更
- CHANGELOG.md の言語を今回から日本語に（CHANGELOG を書く時間が増すためです）
- README.md から Example を削除して Example フォルダ内に移動しました
- **!BREAKING CHANGE**: note に関する物を一つのファイルに纏めました、これによりインポートの変更が必要です。
- **!BREAKING CHANGE**: パッケージのファイル名を misskey から mi.py に変更しました。これにより全てのインポートの変更が必要です。

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

[unreleased]: https://github.com/yupix/mi.py/compare/master...HEAD
