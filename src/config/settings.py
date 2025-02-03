import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/usports")
DATABASE_URL = "sqlite:///usports.db"