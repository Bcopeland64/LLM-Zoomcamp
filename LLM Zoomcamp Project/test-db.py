import unittest
import tempfile
import os
from src.utils.db import Database, init_db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test.db')
        init_db(self.db_path)

    def tearDown(self):
        os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_insert_and_fetch(self):
        with Database(self.db_path) as db:
            db.execute("INSERT INTO documents (content) VALUES (?)", ("Test document",))
            result = db.fetchone("SELECT content FROM documents WHERE id = ?", (1,))
            self.assertEqual(result['content'], "Test document")

    def test_fetchall(self):
        with Database(self.db_path) as db:
            db.execute("INSERT INTO documents (content) VALUES (?)", ("Doc 1",))
            db.execute("INSERT INTO documents (content) VALUES (?)", ("Doc 2",))
            results = db.fetchall("SELECT content FROM documents ORDER BY id")
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0]['content'], "Doc 1")
            self.assertEqual(results[1]['content'], "Doc 2")

if __name__ == '__main__':
    unittest.main()
