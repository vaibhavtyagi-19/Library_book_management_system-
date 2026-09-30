from datetime import date
from typing import List, Tuple

from models.book import Book
from models.transaction import Transaction
from storage.csv_storage import BookRepository, TransactionRepository
from utils.exceptions import LibraryError
from utils.validators import validate_book_id, validate_non_empty


class BorrowingService:
    def __init__(self, books: BookRepository, transactions: TransactionRepository):
        self.books = books
        self.transactions = transactions

    @staticmethod
    def _next_id(transactions: List[Transaction]) -> str:
        nums = [int(t.transaction_id[1:]) for t in transactions
                if t.transaction_id[1:].isdigit()]
        return f"T{(max(nums) + 1 if nums else 1):04d}"

    def issue_book(self, book_id: str, student_id: str, student_name: str) -> Transaction:
        book_id = validate_book_id(book_id)
        student_id = validate_non_empty(student_id, "Student ID")
        student_name = validate_non_empty(student_name, "Student name")

        if not any(b.book_id == book_id for b in self.books.load()):
            raise LibraryError(f"No book found with ID '{book_id}'.")

        transactions = self.transactions.load()
        if any(t.book_id == book_id and t.is_active for t in transactions):
            raise LibraryError(f"Book '{book_id}' is already checked out.")

        txn = Transaction(self._next_id(transactions), book_id, student_id,
                          student_name, date.today().isoformat())
        transactions.append(txn)
        self.transactions.save(transactions)
        return txn

    def return_book(self, book_id: str) -> Transaction:
        book_id = validate_book_id(book_id)
        transactions = self.transactions.load()
        txn = next((t for t in transactions
                    if t.book_id == book_id and t.is_active), None)
        if txn is None:
            raise LibraryError(f"Book '{book_id}' is not currently issued.")
        txn.return_date = date.today().isoformat()
        self.transactions.save(transactions)
        return txn

    def get_issued(self) -> List[Tuple[Transaction, Book]]:
        books = {b.book_id: b for b in self.books.load()}
        return [(t, books[t.book_id]) for t in self.transactions.load()
                if t.is_active and t.book_id in books]
