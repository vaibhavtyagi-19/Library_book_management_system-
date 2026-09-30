from utils.exceptions import ValidationError


def validate_non_empty(value: str, field_name: str = "Field") -> str:
    """Return the stripped value, or raise if it is empty/blank."""
    if value is None or not str(value).strip():
        raise ValidationError(f"{field_name} cannot be empty.")
    return str(value).strip()


def validate_book_id(book_id: str) -> str:
    """Book IDs must be non-empty and strictly alphanumeric (A-Z, a-z, 0-9)."""
    book_id = validate_non_empty(book_id, "Book ID")
    if not (book_id.isascii() and book_id.isalnum()):
        raise ValidationError("Book ID must be alphanumeric (letters and digits only).")
    return book_id.upper()


def validate_book_fields(title: str, author: str, genre: str) -> tuple:
    return (
        validate_non_empty(title, "Title"),
        validate_non_empty(author, "Author"),
        validate_non_empty(genre, "Genre"),
    )
