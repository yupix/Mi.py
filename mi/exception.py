__all__ = ['CogNameDuplicate', 'CredentialRequired', 'ContentRequired']

class CredentialRequired(Exception):
    pass


class ContentRequired(Exception):
    pass


class CogNameDuplicate(Exception):
    pass