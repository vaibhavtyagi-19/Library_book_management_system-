class Transaction:
    FIELDS = ["transaction_id", "book_id", "student_id",
              "student_name", "issue_date", "return_date"]

    def __init__(self, transaction_id: str, book_id: str, student_id: str,
                 student_name: str, issue_date: str, return_date: str = ""):
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.student_id = student_id
        self.student_name = student_name
        self.issue_date = issue_date
        self.return_date = return_date

    @property
    def is_active(self) -> bool:
        """A transaction is active until a return date is logged."""
        return not self.return_date

    def to_dict(self) -> dict:
        return {f: getattr(self, f) for f in self.FIELDS}

    @classmethod
    def from_dict(cls, row: dict) -> "Transaction":
        return cls(**{f: row.get(f, "") for f in cls.FIELDS})
