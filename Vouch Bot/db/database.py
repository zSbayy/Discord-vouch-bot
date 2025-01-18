import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('vouches.db')
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vouches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_id TEXT NOT NULL,
                vouched_user_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)

    def create_vouch(self, author_id, vouched_user_id, rating, message):
        with self.conn:
            self.conn.execute("""
            INSERT INTO vouches (author_id, vouched_user_id, rating, message)
            VALUES (?, ?, ?, ?)
            """, (author_id, vouched_user_id, rating, message))

    def get_vouch_count(self):
        with self.conn:
            result = self.conn.execute("SELECT COUNT(*) FROM vouches").fetchone()
            return result[0]

    def get_all_vouches(self):
        with self.conn:
            result = self.conn.execute("SELECT * FROM vouches").fetchall()
            return result 
