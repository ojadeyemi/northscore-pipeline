import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://user:password@localhost/usports")
