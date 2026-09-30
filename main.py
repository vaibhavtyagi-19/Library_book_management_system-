"""Presentation layer: menus and I/O only. All logic lives in services/."""
from services.book_service import BookService
from services.borrowing_service import BorrowingService
from services.report_service import ReportService
from storage.csv_storage import BookRepository, TransactionRepository
from utils.exceptions import LibraryError, StorageError, ValidationError

MENU = """
========== LIBRARY MANAGEMENT SYSTEM ==========
 1. Add book              5. Delete book
 2. View all books        6. Issue book to student
 3. Search books          7. Return book
 4. Update book           8. Reports
 0. Exit
===============================================
"""

REPORT_MENU = """
--- Reports ---
 1. Book count by genre
 2. Currently issued books
 0. Back
"""


def print_books(books) -> None:
    if not books:
        print("No books found.")
        return
    print(f"\n{'ID':<10}{'Title':<30}{'Author':<22}{'Genre':<15}")
    print("-" * 77)
    for b in books:
        print(f"{b.book_id:<10}{b.title[:28]:<30}{b.author[:20]:<22}{b.genre[:13]:<15}")


def add_book(books: BookService) -> None:
    book = books.add_book(
        input("Book ID (alphanumeric): "), input("Title: "),
        input("Author: "), input("Genre: "),
    )
    print(f"Added: {book}")


def search_books(books: BookService) -> None:
    print_books(books.search(input("Search keyword: ")))


def update_book(books: BookService) -> None:
    book_id = input("Book ID to update: ")
    print("(Leave a field blank to keep its current value)")
    book = books.update_book(book_id, input("New title: "),
                             input("New author: "), input("New genre: "))
    print(f"Updated: {book}")


def delete_book(books: BookService) -> None:
    book_id = input("Book ID to delete: ")
    if input(f"Delete '{book_id}'? (y/n): ").strip().lower() == "y":
        print(f"Deleted: {books.delete_book(book_id)}")
    else:
        print("Cancelled.")


def issue_book(borrowing: BorrowingService) -> None:
    txn = borrowing.issue_book(input("Book ID: "), input("Student ID: "),
                               input("Student name: "))
    print(f"Issued {txn.book_id} to {txn.student_name} on {txn.issue_date} "
          f"(Txn {txn.transaction_id}).")


def return_book(borrowing: BorrowingService) -> None:
    txn = borrowing.return_book(input("Book ID being returned: "))
    print(f"Returned {txn.book_id} on {txn.return_date}.")


def reports_menu(reports: ReportService) -> None:
    while True:
        print(REPORT_MENU)
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                counts = reports.books_by_genre()
                if not counts:
                    print("No books in the library.")
                for genre, n in counts.items():
                    print(f"  {genre:<20}{n}")
            elif choice == "2":
                issued = reports.currently_issued()
                if not issued:
                    print("No books are currently issued.")
                for txn, book in issued:
                    print(f"  {book.book_id:<8}{book.title[:25]:<27}"
                          f"-> {txn.student_name} ({txn.student_id}), "
                          f"since {txn.issue_date}")
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except StorageError as e:
            print(f"Storage error: {e}")


def main() -> None:
    book_repo, txn_repo = BookRepository(), TransactionRepository()
    books = BookService(book_repo, txn_repo)
    borrowing = BorrowingService(book_repo, txn_repo)
    reports = ReportService(book_repo, borrowing)

    actions = {
        "1": lambda: add_book(books),
        "2": lambda: print_books(books.get_all()),
        "3": lambda: search_books(books),
        "4": lambda: update_book(books),
        "5": lambda: delete_book(books),
        "6": lambda: issue_book(borrowing),
        "7": lambda: return_book(borrowing),
        "8": lambda: reports_menu(reports),
    }

    while True:
        print(MENU)
        try:
            choice = input("Choose an option: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid option. Please try again.")
            continue
        try:
            action()
        except ValidationError as e:
            print(f"Invalid input: {e}")
        except LibraryError as e:
            print(f"Cannot complete request: {e}")
        except StorageError as e:
            print(f"Storage error: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")


if __name__ == "__main__":
    main()
