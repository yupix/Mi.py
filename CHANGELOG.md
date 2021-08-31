# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

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


[v0.0.1a]: https://github.com/yupix/Mi.py/releases
[Unreleased]: https://github.com/yupix/mi.py/compare/master...HEAD
