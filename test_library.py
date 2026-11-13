import unittest
import os
import sqlite3
from library import DatabaseManager

TEST_DB = "test_library.db"

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        self.db = DatabaseManager(db_name=TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_initial_seed(self):
        books = self.db.get_all_books()
        self.assertEqual(len(books), 5)

    def test_add_book_success(self):
        result = self.db.add_book("1984", "George Orwell", "Dystopian")
        self.assertTrue(result)
        results = self.db.search_books("1984")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][1], "1984")

    def test_add_duplicate_book_failure(self):
        result = self.db.add_book("Utopia", "Duplicate Author")
        self.assertFalse(result)

    def test_search_by_author_and_genre(self):
        results = self.db.search_books("Homer")
        self.assertEqual(len(results), 1)
        results = self.db.search_books("Philosophy")
        self.assertEqual(len(results), 1)

    def test_toggle_status(self):
        book = self.db.get_all_books()[0]
        book_id = book[0]
        self.assertEqual(book[4], "Available")
        
        self.db.update_status(book_id, "Borrowed")
        updated_book = self.db.get_book_by_id(book_id)
        self.assertEqual(updated_book[4], "Borrowed")

    def test_delete_book(self):
        book = self.db.get_all_books()[0]
        book_id = book[0]
        deleted = self.db.delete_book(book_id)
        self.assertTrue(deleted)
        self.assertIsNone(self.db.get_book_by_id(book_id))

if __name__ == "__main__":
    unittest.main()
