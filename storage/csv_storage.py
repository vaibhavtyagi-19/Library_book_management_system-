import csv
import os
from typing import List

from models.book import Book
from models.transaction import Transaction
from utils.exceptions import StorageError

DATA_DIR = "data"


class CsvRepository:
    """Generic, defensive CSV reader/writer."""

    def __init__(self, filepath: str, fieldnames: List[str]):
        self.filepath = filepath
        self.fieldnames = fieldnames

    def _ensure_file(self) -> None:
        """Create the directory and an empty CSV (header only) if missing."""
        try:
            os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=self.fieldnames).writeheader()
        except OSError as e:
            raise StorageError(f"Cannot create '{self.filepath}': {e}") from e

    def read_all(self) -> List[dict]:
        try:
            with open(self.filepath, "r", newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except FileNotFoundError:
            self._ensure_file()          # self-heal instead of crashing
            return []
        except (OSError, csv.Error) as e:
            raise StorageError(f"Cannot read '{self.filepath}': {e}") from e

    def write_all(self, rows: List[dict]) -> None:
        try:
            os.makedirs(os.path.dirname(self.filepath) or ".", exist_ok=True)
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        except (OSError, csv.Error) as e:
            raise StorageError(f"Cannot write '{self.filepath}': {e}") from e


class BookRepository(CsvRepository):
    def __init__(self, filepath: str = os.path.join(DATA_DIR, "books.csv")):
        super().__init__(filepath, Book.FIELDS)

    def load(self) -> List[Book]:
        return [Book.from_dict(r) for r in self.read_all()]

    def save(self, books: List[Book]) -> None:
        self.write_all([b.to_dict() for b in books])


class TransactionRepository(CsvRepository):
    def __init__(self, filepath: str = os.path.join(DATA_DIR, "transactions.csv")):
        super().__init__(filepath, Transaction.FIELDS)

    def load(self) -> List[Transaction]:
        return [Transaction.from_dict(r) for r in self.read_all()]

    def save(self, transactions: List[Transaction]) -> None:
        self.write_all([t.to_dict() for t in transactions])
