from typing import List, Optional

from models.book import Book
from storage.csv_storage import BookRepository, TransactionRepository
from utils.exceptions import LibraryError
from utils.validators import validate_book_id, validate_book_fields, validate_non_empty


class BookService:
    def __init__(self, books: BookRepository, transactions: TransactionRepository):
        self.books = books
        self.transactions = transactions

    def add_book(self, book_id: str, title: str, author: str, genre: str) -> Book:
        book_id = validate_book_id(book_id)
        title, author, genre = validate_book_fields(title, author, genre)
        all_books = self.books.load()
        if any(b.book_id == book_id for b in all_books):
            raise LibraryError(f"A book with ID '{book_id}' already exists.")
        book = Book(book_id, title, author, genre.title())
        all_books.append(book)
        self.books.save(all_books)
        return book

    def get_all(self) -> List[Book]:
        return self.books.load()

    def get_by_id(self, book_id: str) -> Optional[Book]:
        book_id = validate_book_id(book_id)
        return next((b for b in self.books.load() if b.book_id == book_id), None)

    def search(self, keyword: str) -> List[Book]:
        """Case-insensitive linear search over ID, title, author and genre."""
        keyword = validate_non_empty(keyword, "Search keyword").lower()
        return [
            b for b in self.books.load()
            if keyword in b.book_id.lower() or keyword in b.title.lower()
            or keyword in b.author.lower() or keyword in b.genre.lower()
        ]

    def update_book(self, book_id: str, title: str = "", author: str = "",
                    genre: str = "") -> Book:
        """Blank arguments keep the existing value."""
        book_id = validate_book_id(book_id)
        all_books = self.books.load()
        book = next((b for b in all_books if b.book_id == book_id), None)
        if book is None:
            raise LibraryError(f"No book found with ID '{book_id}'.")
        if title.strip():
            book.title = title.strip()
        if author.strip():
            book.author = author.strip()
        if genre.strip():
            book.genre = genre.strip().title()
        self.books.save(all_books)
        return book

    def delete_book(self, book_id: str) -> Book:
        book_id = validate_book_id(book_id)
        if any(t.book_id == book_id and t.is_active for t in self.transactions.load()):
            raise LibraryError("Cannot delete a book that is currently issued.")
        all_books = self.books.load()
        book = next((b for b in all_books if b.book_id == book_id), None)
        if book is None:
            raise LibraryError(f"No book found with ID '{book_id}'.")
        all_books.remove(book)
        self.books.save(all_books)
        return book
