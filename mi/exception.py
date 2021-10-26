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
)


class ImAi(Exception):
    pass


class InternalServerError(Exception):
    pass


class ClientError(Exception):
    pass


class AuthenticationError(Exception):
    pass


class NotExistRequiredParameters(Exception):
    pass


class InvalidParameters(Exception):
    pass


class CredentialRequired(Exception):
    pass


class ContentRequired(Exception):
    pass


class CogNameDuplicate(Exception):
    pass


class ExtensionAlreadyLoaded(Exception):
    pass


class ExtensionFailed(Exception):
    pass


class NoEntryPointError(Exception):
    pass


class ExtensionNotFound(Exception):
    pass


class CommandRegistrationError(Exception):
    pass


class CommandError(Exception):
    pass


class CommandInvokeError(Exception):
    pass


class CheckFailure(Exception):
    pass


class InvalidCogPath(Exception):
    pass
