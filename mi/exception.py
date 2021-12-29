__all__ = (
    "CogNameDuplicate",
    "CredentialRequired",
    "ContentRequired",
    "CommandError",
    "CommandInvokeError",
    "CommandRegistrationError",
    "ExtensionAlreadyLoaded",
    "ExtensionFailed",
    "CheckFailure",
    "ExtensionNotFound",
    "NoEntryPointError",
    "InvalidCogPath",
    "InvalidParameters",
    "NotExistRequiredParameters",
    "AuthenticationError",
    "ClientError",
    "ImAi",
    "InternalServerError",
    "TaskNotRunningError",
    "NotFoundError",
    "NotExistRequiredData"
)


class NotExistRequiredData(Exception):
    """
    必要なデータが存在しない場合に発生する例外
    """


class NotFoundError(Exception):
    """
    http アクセス時に404が帰ってきた際の例外
    """


class TaskNotRunningError(Exception):
    """
    タスクを停止しようとした際、タスクが起動していない場合に発生する例外
    """


class ImAi(Exception):
    """
    私は藍です
    """


class InternalServerError(Exception):
    """
    http アクセス時に500が帰ってきた際の例外
    """


class ClientError(Exception):
    """
    http アクセス時に400が帰ってきた際の例外
    """


class AuthenticationError(Exception):
    """
    認証で問題が発生した際の例外
    """


class NotExistRequiredParameters(Exception):
    """
    必須のパラメーターが存在しない場合の例外
    """


class InvalidParameters(Exception):
    """
    パラメーターが無効
    """


class CredentialRequired(Exception):
    """
    認証情報が不足している
    """


class ContentRequired(Exception):
    """
    送信するコンテンツが不足している
    """


class CogNameDuplicate(Exception):
    """
    cogの名前が重複している
    """


class ExtensionAlreadyLoaded(Exception):
    """
    cogがすでに読み込まれている
    """


class ExtensionFailed(Exception):
    """
    cog周りのエラー
    """


class NoEntryPointError(Exception):
    """
    cogにsetup関数が無い場合の例外
    """


class ExtensionNotFound(Exception):
    """
    指定されたパスにcogが存在しない場合の例外
    """


class CommandRegistrationError(Exception):
    """
    コマンド登録時のエラー
    """


class CommandError(Exception):
    """
    コマンドで問題が発生した際の例外
    """


class CommandInvokeError(Exception):
    """
    コマンドの実行に問題が発生した際の例外
    """


class CheckFailure(Exception):
    """
    コマンドの実行可能かのチェックに失敗した際の例外
    """


class InvalidCogPath(Exception):
    """
    cogのパスが不正
    """
