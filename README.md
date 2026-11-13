# 📚 Library Management System

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Database](https://img.shields.io/badge/database-SQLite3-lightgrey.svg)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A modular, clean-architecture Command Line Interface (CLI) Library Management System written in Python. This project demonstrates core software engineering principles including database persistence, object-oriented design (OOP), input sanitization, and automated unit testing.

---

## 🌟 Key Features

- **Relational Persistence**: Integrated with SQLite (`library.db`) with relational integrity constraints (`UNIQUE`, `CHECK`).
- **Catalog Management**: View catalog with structured tabular formatting, add books with auto-deduplication, and safely delete entries.
- **Search & Filter**: Case-insensitive multi-attribute search across title, author, and genre.
- **Lending Workflow**: Issue and return books with real-time status toggling (`Available` / `Borrowed`).
- **Clean Architecture & OOP**: Distinct separation of concerns between `DatabaseManager` (Data Access Layer) and `LibraryCLI` (Presentation Layer).
- **Unit Testing**: Automated test coverage using Python's built-in `unittest` framework.

---

## 🏗️ Architecture & Database Design

```text
┌─────────────────┐       Queries & Transactions       ┌─────────────────┐
│   LibraryCLI    │ ─────────────────────────────────> │ DatabaseManager │
│  (Presentation) │ <───────────────────────────────── │  (Data Access)  │
└─────────────────┘             Result Sets            └────────┬────────┘
                                                                │
                                                                ▼
                                                        ┌───────────────┐
                                                        │  library.db   │
                                                        │   (SQLite)    │
                                                        └───────────────┘
```

### Database Schema (`books` Table)
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique identifier for each book |
| `title` | `TEXT` | `UNIQUE NOT NULL COLLATE NOCASE` | Title of the book (case-insensitive) |
| `author` | `TEXT` | `NOT NULL` | Author name |
| `genre` | `TEXT` | `DEFAULT 'General'` | Genre classification |
| `status` | `TEXT` | `DEFAULT 'Available' CHECK(...)` | Book status (`Available` / `Borrowed`) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ (No external third-party dependencies required; relies entirely on the Python Standard Library).

### Installation & Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ayusharma1601/Project-2.git
   cd Project-2
   ```

2. **Launch the application:**
   ```bash
   python library.py
   ```

---

## 🧪 Running Automated Tests

To run the unit test suite:

```bash
python -m unittest test_library.py -v
```

All 6 test cases cover:
- Database initialization and seeding
- Book insertion and duplicate prevention
- Multi-field keyword searching
- Borrowing and return status lifecycle
- Deletion and cascading queries

---

## 📁 Project Structure

```text
├── library.py          # Core logic (DatabaseManager & LibraryCLI)
├── test_library.py     # Unit test suite
├── .gitignore          # Version control exclusions (*.db, __pycache__)
└── README.md           # Documentation & design overview
```
