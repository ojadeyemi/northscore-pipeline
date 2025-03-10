from sqlalchemy import text
from sqlalchemy.orm import Session


def reset_sequence(session: Session, table_name):
    """Reset the primary key sequence for a table"""
    session.execute(text(f"ALTER SEQUENCE {table_name}_id_seq RESTART WITH 1"))
