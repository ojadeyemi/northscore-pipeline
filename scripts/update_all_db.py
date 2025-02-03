from src.database.db import Base, SessionLocal, engine
from src.pipelines.basketball_pipeline import update_basketball_db


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()

    session = SessionLocal()

    try:
        update_basketball_db(session)
    except Exception as e:
        print(f"[91mFailed to update database: {e}[0m")
    finally:
        session.close()
