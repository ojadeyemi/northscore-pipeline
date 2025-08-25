import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:password@localhost:5432/northscore")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
