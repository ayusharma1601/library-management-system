import sqlite3
import os
from typing import List, Tuple, Optional
from contextlib import contextmanager

DB_NAME = "library.db"
VALID_STATUSES = {"Available", "Borrowed"}

class DatabaseManager:
    """Manages SQLite database operations for the Library."""

    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self) -> None:
        """Initializes tables and seeds sample data if the catalog is empty."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT UNIQUE NOT NULL COLLATE NOCASE,
                    author TEXT NOT NULL,
                    genre TEXT DEFAULT 'General',
                    status TEXT DEFAULT 'Available' CHECK(status IN ('Available', 'Borrowed'))
                )
            """)
            cursor.execute("SELECT COUNT(*) FROM books")
            if cursor.fetchone()[0] == 0:
                seed_data = [
                    ("Utopia", "Thomas More", "Philosophy", "Available"),
                    ("Odyssey", "Homer", "Epic Poetry", "Available"),
                    ("Othello", "William Shakespeare", "Tragedy", "Available"),
                    ("Clean Code", "Robert C. Martin", "Technology", "Available"),
                    ("To Kill a Mockingbird", "Harper Lee", "Classic", "Available"),
                ]
                cursor.executemany(
                    "INSERT INTO books (title, author, genre, status) VALUES (?, ?, ?, ?)",
                    seed_data,
                )
                conn.commit()

    def add_book(self, title: str, author: str, genre: str = "General") -> bool:
        """Adds a book; returns False for invalid or duplicate records."""
        title, author, genre = title.strip(), author.strip(), genre.strip()
        if not title or not author:
            return False
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "INSERT INTO books (title, author, genre, status) VALUES (?, ?, ?, 'Available')",
                    (title, author, genre or "General"),
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False

    def get_all_books(self) -> List[Tuple]:
        with self.get_connection() as conn:
            return conn.execute(
                "SELECT id, title, author, genre, status FROM books ORDER BY title ASC"
            ).fetchall()

    def search_books(self, query: str) -> List[Tuple]:
        with self.get_connection() as conn:
            search_param = f"%{query.strip()}%"
            return conn.execute("""
                SELECT id, title, author, genre, status
                FROM books
                WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
                ORDER BY title ASC
            """, (search_param, search_param, search_param)).fetchall()

    def update_status(self, book_id: int, new_status: str) -> bool:
        """Updates status only to one of the values supported by the schema."""
        if new_status not in VALID_STATUSES:
            return False
        with self.get_connection() as conn:
            cursor = conn.execute(
                "UPDATE books SET status = ? WHERE id = ?", (new_status, book_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_book(self, book_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_book_by_id(self, book_id: int) -> Optional[Tuple]:
        with self.get_connection() as conn:
            return conn.execute(
                "SELECT id, title, author, genre, status FROM books WHERE id = ?", (book_id,)
            ).fetchone()


class LibraryCLI:
    """Handles the command-line interface for the library."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def print_table(self, rows: List[Tuple]) -> None:
        if not rows:
            print("\nNo books found matching the criteria.\n")
            return
        header = f"{'ID':<5} | {'Title':<28} | {'Author':<24} | {'Genre':<15} | {'Status':<10}"
        separator = "-" * len(header)
        print(f"\n{separator}\n{header}\n{separator}")
        for row in rows:
            print(f"{row[0]:<5} | {row[1]:<28} | {row[2]:<24} | {row[3]:<15} | {row[4]:<10}")
        print(f"{separator}\nTotal: {len(rows)} record(s)\n")

    def show_books_view(self) -> None:
        print("\n--- Current Library Catalog ---")
        self.print_table(self.db.get_all_books())

    def add_book_view(self) -> None:
        print("\n--- Add New Book ---")
        title = input("Enter book title: ").strip()
        author = input("Enter author name: ").strip()
        if not title or not author:
            print("Error: Book title and author cannot be empty.")
            return
        genre = input("Enter genre (leave blank for 'General'): ").strip() or "General"
        if self.db.add_book(title, author, genre):
            print(f"Success: '{title}' by {author} has been added to the library.")
        else:
            print(f"Error: A book with the title '{title}' already exists.")

    def search_book_view(self) -> None:
        print("\n--- Search Catalog ---")
        query = input("Enter keyword (title, author, or genre): ").strip()
        if not query:
            print("Search query cannot be empty.")
            return
        self.print_table(self.db.search_books(query))

    def toggle_borrow_view(self) -> None:
        print("\n--- Issue / Return Book ---")
        book_id_str = input("Enter Book ID: ").strip()
        if not book_id_str.isdigit():
            print("Error: Invalid ID. Please enter an integer.")
            return
        book_id = int(book_id_str)
        book = self.db.get_book_by_id(book_id)
        if not book:
            print(f"Error: No book found with ID {book_id}.")
            return
        new_status = "Borrowed" if book[4] == "Available" else "Available"
        if self.db.update_status(book_id, new_status):
            action = "borrowed" if new_status == "Borrowed" else "returned"
            print(f"Success: '{book[1]}' is now marked as {new_status} ({action}).")
        else:
            print("Failed to update book status.")

    def delete_book_view(self) -> None:
        print("\n--- Remove Book ---")
        book_id_str = input("Enter Book ID to remove: ").strip()
        if not book_id_str.isdigit():
            print("Error: Invalid ID. Please enter an integer.")
            return
        book_id = int(book_id_str)
        book = self.db.get_book_by_id(book_id)
        if not book:
            print(f"Error: Book with ID {book_id} not found.")
            return
        if input(f"Confirm deleting '{book[1]}' by {book[2]}? (y/n): ").strip().lower() == "y":
            if self.db.delete_book(book_id):
                print(f"Success: '{book[1]}' removed from library.")
            else:
                print("Failed to delete book.")
        else:
            print("Deletion cancelled.")

    def run(self) -> None:
        while True:
            print("\n==============================================")
            print("       LIBRARY MANAGEMENT SYSTEM (CLI)        ")
            print("==============================================")
            print("1. View All Books\n2. Add New Book\n3. Search Books")
            print("4. Issue / Return Book (Toggle Status)\n5. Delete a Book\n6. Exit")
            choice = input("Enter your option (1-6): ").strip()
            if choice == "1":
                self.show_books_view()
            elif choice == "2":
                self.add_book_view()
            elif choice == "3":
                self.search_book_view()
            elif choice == "4":
                self.toggle_borrow_view()
            elif choice == "5":
                self.delete_book_view()
            elif choice == "6":
                print("\nThank you for using the Library Management System. Goodbye!\n")
                break
            else:
                print("Invalid selection. Please choose an option from 1 to 6.")


if __name__ == "__main__":
    db_manager = DatabaseManager()
    LibraryCLI(db_manager).run()
