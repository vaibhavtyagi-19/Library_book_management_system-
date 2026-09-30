class LibraryError(Exception):
    """Business-rule violation (duplicate ID, book already issued, etc.)."""


class ValidationError(ValueError):
    """Invalid user input."""


class StorageError(Exception):
    """File read/write failure."""
