from src.database.db import Base, SessionLocal, engine
from src.pipelines.basketball_pipeline import update_basketball_db


def init_db():
    """Initialize database"""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()

    session = SessionLocal()

    try:
        # filter_categories=[("m", "regular"), ("w", "regular")]
        update_basketball_db(session, filter_categories=[("m", "championship"), ("w", "championship")])
    except TypeError as e:
        print("\nTypeError: ", e)
        raise
    except Exception as e:
        print(f"\nFAILED TO UPDATE DATABASE!!!: {e}")
    finally:
        session.close()
