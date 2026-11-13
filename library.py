import sqlite3
import os

DB_NAME = "library.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL COLLATE NOCASE,
            author TEXT NOT NULL
        )
    """)
    # Seed initial books if the database is empty
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        initial_books = [
            ("Utopia", "Thomas More"),
            ("Odyssey", "Homer"),
            ("Othello", "William Shakespeare")
        ]
        cursor.executemany("INSERT INTO books (title, author) VALUES (?, ?)", initial_books)
        conn.commit()
    conn.close()

def add_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    while True:
        book = input("\nEnter the name of the book you want to add: ").strip().title()
        if not book:
            print("Book title cannot be empty.")
            continue
        author = input("Enter the name of the author: ").strip().title()
        if not author:
            print("Author cannot be empty.")
            continue
        try:
            cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (book, author))
            conn.commit()
            print(f"'{book}' by {author} added successfully!")
        except sqlite3.IntegrityError:
            print(f"Book '{book}' already exists in the database.")
        
        more = input("Add another book? (y/n): ").strip().lower()
        if more != "y":
            break
    conn.close()

def show_books():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author FROM books ORDER BY title ASC")
    rows = cursor.fetchall()
    conn.close()

    print("\n--- Books in Library ---")
    if not rows:
        print("No books found.")
    else:
        for book_id, title, author in rows:
            print(f"[{book_id}] {title} by {author}")
    print("------------------------")

def search_book():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    find = input("\nWhat book or author do you want to search for?: ").strip()
    if not find:
        print("Search query cannot be empty.")
        conn.close()
        return

    cursor.execute("SELECT id, title, author FROM books WHERE title LIKE ? OR author LIKE ?", (f"%{find}%", f"%{find}%"))
    results = cursor.fetchall()
    conn.close()

    if results:
        print(f"\nFound {len(results)} matching book(s):")
        for book_id, title, author in results:
            print(f" - [{book_id}] {title} by {author}")
    else:
        print("Book not found.")

def delete_book():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    title = input("\nEnter the title of the book to delete: ").strip()
    cursor.execute("SELECT id, title, author FROM books WHERE title = ? COLLATE NOCASE", (title,))
    row = cursor.fetchone()
    if row:
        confirm = input(f"Are you sure you want to delete '{row[1]}' by {row[2]}? (y/n): ").strip().lower()
        if confirm == "y":
            cursor.execute("DELETE FROM books WHERE id = ?", (row[0],))
            conn.commit()
            print(f"'{row[1]}' deleted successfully.")
        else:
            print("Deletion cancelled.")
    else:
        print("Book not found.")
    conn.close()

def main():
    init_db()
    while True:
        print("\n========================================")
        print("  Welcome to Library Management System  ")
        print("========================================")
        print("1. Check what books we have")
        print("2. Add books of your choice")
        print("3. Search a book (by title or author)")
        print("4. Delete a book")
        print("5. Exit")
        
        options = input("Enter your choice (1-5): ").strip()

        if options == "1":
            show_books()
        elif options == "2":
            add_books()
        elif options == "3":
            search_book()
        elif options == "4":
            delete_book()
        elif options == "5":
            print("\nThank you for using the Library Management System. Goodbye!")
            break
        else:
            print("Invalid Input. Please select a valid option (1-5).")

if __name__ == "__main__":
    main()
