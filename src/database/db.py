import logfire
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config.settings import DATABASE_URL

# Configure Logfire once at startup
logfire.configure(environment="pipeline", service_name="pipeline")

# https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
engine = create_engine(DATABASE_URL, echo=False)

# Instrument SQLAlchemy for automatic query tracking
logfire.instrument_sqlalchemy(engine=engine)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
