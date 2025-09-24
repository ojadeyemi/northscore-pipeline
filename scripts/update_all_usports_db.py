"""Update database with all fetched USports data"""

from datetime import datetime

from src.database.db import Base, SessionLocal, engine
from src.pipelines.seasonal_logic import get_active_seasons_by_month
from src.pipelines.usports import (
    BasketballPipeline,
    FootballPipeline,
    IceHockeyPipeline,
    SoccerPipeline,
    VolleyballPipeline,
)
from src.pipelines.usports.base import BaseSportPipeline
from src.utils.constants import (
    BASKETBALL,
    FOOTBALL,
    ICE_HOCKEY,
    SOCCER,
    VOLLEYBALL,
)
from src.utils.logger import log


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)


def update_all_databases():
    """Update all sport databases based on current season timing"""
    init_db()

    current_month = datetime.now().month
    active_seasons = get_active_seasons_by_month(current_month)
    log.debug(f"🗓️  Active seasons for month {current_month}: {active_seasons}")

    SPORT_PIPELINES: dict[str, BaseSportPipeline] = {
        BASKETBALL: BasketballPipeline(),
        FOOTBALL: FootballPipeline(),
        ICE_HOCKEY: IceHockeyPipeline(),
        VOLLEYBALL: VolleyballPipeline(),
        SOCCER: SoccerPipeline(),
    }

    session = SessionLocal()

    try:
        for sport, season_options in active_seasons.items():
            if sport not in SPORT_PIPELINES:
                continue

            pipeline = SPORT_PIPELINES[sport]
            leagues = ["m", "w"] if sport != FOOTBALL else ["m"]

            for league in leagues:
                for season_option in season_options:
                    try:
                        pipeline.run_pipeline(session, league, season_option)  # type: ignore
                    except Exception:
                        session.rollback()

        log.info("\n🎉 All active sports databases updated successfully!")

    except Exception as e:
        log.error(f"\n💥 Database update failed: {e}")
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    update_all_databases()
