from unittest import TestCase
from backend.database import Database
import unittest
import os
import operator
import sqlite3
import sys
print(os.getcwd())
class TestDatabase(TestCase):
    def setUp(self):
        self.database = Database(":memory:")

    def tearDown(self):
        self.database.close()
        del self.database


    def test_create_database(self):
        # create a database on current directory, called database_test.db
        directory = "database_test.db"
        if os.path.exists(directory):
            os.remove(directory)
        self._check_empty_database(Database.create_database(directory))

    def _check_empty_database(self, database):
        """
        :type database: Database
        """
        tables = database.execute("""SELECT name FROM sqlite_master WHERE type="table" """).fetchall()
        tables = list(map(lambda x:x[0], tables))
        self.assertTrue("products" in tables)
        self.assertTrue("users" in tables)

    def test_close(self):
        self.database.close()
        self.assertRaises(sqlite3.ProgrammingError, self.database.connection.execute)

    def test_repl(self):
        pass


if __name__ == "__main__":
    unittest.main()
