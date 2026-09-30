class Book:
    FIELDS = ["book_id", "title", "author", "genre"]

    def __init__(self, book_id: str, title: str, author: str, genre: str):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre

    def to_dict(self) -> dict:
        return {f: getattr(self, f) for f in self.FIELDS}

    @classmethod
    def from_dict(cls, row: dict) -> "Book":
        return cls(row["book_id"], row["title"], row["author"], row["genre"])

    def __str__(self) -> str:
        return f"[{self.book_id}] {self.title} by {self.author} ({self.genre})"
