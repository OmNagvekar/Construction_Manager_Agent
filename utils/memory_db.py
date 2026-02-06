from google.adk.sessions.database_session_service import DatabaseSessionService
from core import settings
import sqlite3
import os

def initialize_session_service(db_url: str):
    # 1. Extract the file path (e.g., 'sqlite:///agent.db' -> 'agent.db')
    db_path = db_url.replace("sqlite+aiosqlite:///", "")
    
    # 2. Ensure the directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    # 3. Create an empty file if it doesn't exist
    # This ensures the driver doesn't complain about a missing file
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.close()
        print(f"Created new database file at: {db_path}")

    return DatabaseSessionService(db_url)

session_service = initialize_session_service(settings.db_url)