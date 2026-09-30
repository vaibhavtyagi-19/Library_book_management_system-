# Library Book and Borrowing Management System

A modular command-line application in Python 3 for managing a library's book catalogue and tracking which books are issued to students. Built with a clean **3-tier architecture**, object-oriented models, and **CSV flat-file storage** (no external database or packages).

> **Author:** Vaibhav Tyagi | **Reg. No:** 26BCE10325
> **College:** VIT Bhopal University | **Course:** CSE Core | **Project:** VITyarthi Project

---

## Features

- **Book management:** add, view, search, update and delete books (ID, Title, Author, Genre)
- **Search:** case-insensitive search across ID, title, author and genre
- **Borrowing:** issue a book to a student and log the return date
- **Validation:** an already issued book cannot be issued again; a book that is out cannot be deleted; Book IDs are unique
- **Reports:** book count by genre, and a list of currently issued books
- **Defensive design:** input validation, typed exceptions, and try/except around all file I/O (a missing CSV is recreated automatically instead of crashing)
- **Tested:** `unittest` suite for the validators

## Architecture

```
main.py  ->  services/  ->  storage/  ->  CSV files
(UI only)    (business      (csv module)
              logic)
        models/ and utils/ are shared by all layers
```

| Layer | Location | Responsibility |
|---|---|---|
| Presentation | `main.py` | Menus, prompts, printing, error messages. No business logic. |
| Service | `services/` | Rules, search, issue/return, reports |
| Storage | `storage/csv_storage.py` | Reading and writing CSV files |
| Models | `models/` | `Book` and `Transaction` classes |
| Utilities | `utils/` | Validators and custom exceptions |

## Project Structure

```
library_system/
├── main.py
├── models/
│   ├── book.py
│   └── transaction.py
├── storage/
│   └── csv_storage.py
├── services/
│   ├── book_service.py
│   ├── borrowing_service.py
│   └── report_service.py
├── utils/
│   ├── exceptions.py
│   └── validators.py
├── tests/
│   └── test_validators.py
└── data/                # created automatically on first run
    ├── books.csv
    └── transactions.csv
```

## Getting Started

**Requirements:** Python 3.8 or later. No third-party packages needed.

```bash
git clone <your-repository-url>
cd library_system
python main.py
```

### Run the tests

```bash
python -m unittest discover -v
```

## Usage

```
========== LIBRARY MANAGEMENT SYSTEM ==========
 1. Add book              5. Delete book
 2. View all books        6. Issue book to student
 3. Search books          7. Return book
 4. Update book           8. Reports
 0. Exit
===============================================
```

Example:

```
Book ID: B101
Student ID: 26BCE0001
Student name: Rahul Sharma
Issued B101 to Rahul Sharma on 2026-09-30 (Txn T0001).

Book ID: B101
Student ID: 26BCE0002
Student name: Aman Verma
Cannot complete request: Book 'B101' is already checked out.
```

## Data Storage

| File | Columns |
|---|---|
| `books.csv` | book_id, title, author, genre |
| `transactions.csv` | transaction_id, book_id, student_id, student_name, issue_date, return_date |

A book is considered *currently issued* when it has a transaction with an empty `return_date`. Returned transactions are kept, so borrowing history is preserved.

## Possible Improvements

- Due dates, overdue detection and fines
- Borrowing history report per student or book
- Swap CSV for SQLite by adding a new repository class
- GUI or web front end reusing the same service layer

## License

Developed for academic purposes as part of the VITyarthi project at VIT Bhopal University.
