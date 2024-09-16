import unittest
import tempfile
import os
from src.utils.db import init_db, Database
from src.retrieval.hybrid_search import HybridSearch

class TestHybridSearch(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, 'test.db')
        init_db(self.db_path)
        self.searcher = HybridSearch(self.db_path)

        # Insert some test documents
        with Database(self.db_path) as db:
            db.execute("INSERT INTO documents (content) VALUES (?)", ("The quick brown fox jumps over the lazy dog",))
            db.execute("INSERT INTO documents (content) VALUES (?)", ("A journey of a thousand miles begins with a single step",))
            db.execute("INSERT INTO documents (content) VALUES (?)", ("To be or not to be, that is the question",))

    def tearDown(self):
        os.remove(self.db_path)
        os.rmdir(self.temp_dir)

    def test_search(self):
        results = self.searcher.search("quick fox", k=2)
        self.assertEqual(len(results), 2)
        self.assertIn("quick brown fox", results[0]['content'])

    def test_empty_query(self):
        results = self.searcher.search("", k=1)
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
