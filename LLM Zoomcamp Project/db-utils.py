import sqlite3
from typing import List, Dict, Any

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def execute(self, query: str, params: tuple = ()) -> None:
        with self.conn:
            self.conn.execute(query, params)

    def fetchall(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        with self.conn:
            cursor = self.conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def fetchone(self, query: str, params: tuple = ()) -> Dict[str, Any]:
        with self.conn:
            cursor = self.conn.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None

def init_db(db_path: str):
    with Database(db_path) as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                embedding BLOB
            )
        ''')

        db.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                rating INTEGER NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
