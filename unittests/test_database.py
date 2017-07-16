from unittest import TestCase
from backend.database import Database
import os
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
        Database.create_database(directory)

    def check_empty_database(self):
        tables = self.database.cursor("""SELECT name FROM sqlite_master WHERE type=table""")
        self.assertTrue("products" in tables)
        self.assertTrue("users" in tables)

    def test_close(self):
        pass

    def test_repl(self):
        pass


