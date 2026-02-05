import sqlite3
from contextlib import contextmanager
from core import settings

class DatabaseManager:
    def __init__(self, db_url):
        # Convert sqlite:///file.db to file.db
        self.db_path = db_url.replace("sqlite:///", "")
        self._init_db()

    def _init_db(self):
        """Initialize tables once at startup."""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS site_configs 
                (site TEXT PRIMARY KEY, rules TEXT)
            ''')

    @contextmanager
    def get_connection(self):
        """Context manager to handle open/close and commits safely."""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

# Initialize once
db_manager = DatabaseManager(settings.db_url)