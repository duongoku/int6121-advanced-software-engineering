import sqlite3


class SQLiteContext:
    def __init__(self, db_path: str = "data/db.sqlite3"):
        self.db_path = db_path
        # Test connection and initialize database if needed
        with sqlite3.connect(self.db_path) as conn:
            if (
                conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='Users'"
                ).fetchone()
                is None
            ):
                self.initialize_database()

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.connection.set_trace_callback(print)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()

    @staticmethod
    def initialize_database():
        with sqlite3.connect("data/db.sqlite3") as conn:
            with open("schema.sql") as f:
                conn.executescript(f.read())
