# Library Book and Borrowing Management System

A modular CLI application in Python 3 using a 3-tier architecture.

## Structure
- `main.py` – Presentation layer (menus only)
- `services/` – Business logic: book CRUD/search, borrowing, reports
- `storage/` – CSV persistence (built-in `csv` module, no SQL)
- `models/` – `Book` and `Transaction` classes
- `utils/` – Validators and custom exceptions
- `tests/` – `unittest` suite for validators
- `data/` – CSV files (auto-created on first run)

## Run
```bash
python main.py
python -m unittest discover -v
```

## Features
- Add, view, search, update, delete books
- Issue a book to a student and log its return date
- Prevents issuing an already checked-out book
- Reports: book count by genre, currently issued books
- Defensive file I/O; missing CSVs are recreated automatically
