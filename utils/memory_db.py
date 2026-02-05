from google.adk.sessions.database_session_service import DatabaseSessionService
from Setting import settings

session_service = DatabaseSessionService(settings.db_url)