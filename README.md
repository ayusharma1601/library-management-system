# Library Book Management System

A Python-based Library Book Management System upgraded with persistent **SQLite database** storage and enhanced features.

## 🚀 Features

- **Persistent SQLite Database (`library.db`)**: Data persists across application restarts instead of being kept only in-memory.
- **View All Books**: List all available books sorted alphabetically with book ID.
- **Add Books**: Add new books with unique title constraints and author details.
- **Search Books**: Search books by title or author with partial/fuzzy matches (`LIKE` queries).
- **Delete Books**: Remove existing books from the library with confirmation.
- **Input Validation**: Clean handling of empty inputs and case-insensitive uniqueness checks.

---

## 🛠️ Requirements

- Python 3.6 or higher (standard library `sqlite3` is built-in; no extra package installation required).

---

## 📖 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ayusharma1601/Project-2.git
   cd Project-2
   ```

2. **Run the application:**
   ```bash
   python library.py
   ```

---

## 🗄️ Database Schema

The database uses SQLite with the following schema:

```sql
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE NOT NULL COLLATE NOCASE,
    author TEXT NOT NULL
);
```

When run for the first time, default sample books (*Utopia*, *Odyssey*, *Othello*) are seeded automatically into `library.db`.
