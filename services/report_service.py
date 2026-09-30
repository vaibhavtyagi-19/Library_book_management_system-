from collections import Counter
from typing import Dict, List, Tuple

from models.book import Book
from models.transaction import Transaction
from services.borrowing_service import BorrowingService
from storage.csv_storage import BookRepository


class ReportService:
    def __init__(self, books: BookRepository, borrowing: BorrowingService):
        self.books = books
        self.borrowing = borrowing

    def books_by_genre(self) -> Dict[str, int]:
        counts = Counter(b.genre for b in self.books.load())
        return dict(sorted(counts.items()))

    def currently_issued(self) -> List[Tuple[Transaction, Book]]:
        return self.borrowing.get_issued()
