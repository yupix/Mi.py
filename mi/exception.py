__all__ = ['CogNameDuplicate', 'CredentialRequired', 'ContentRequired']


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
