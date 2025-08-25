from abc import ABC, abstractmethod

from pandas import DataFrame
from sqlalchemy.orm import Session
from usports.base.types import LeagueType, SeasonType

from src.utils.logger import log


class BaseSportPipeline(ABC):
    """Base class for all sport pipelines"""

    def __init__(self, sport_name: str):
        self.sport_name = sport_name

    @abstractmethod
    def fetch_data(self, league: LeagueType, season_option: SeasonType):
        """Fetch data from USports package"""
        pass

    @abstractmethod
    def validate_data(self, standings_df: DataFrame, team_stats_df: DataFrame, player_stats_df: DataFrame):
        """Validate fetched data"""
        pass

    @abstractmethod
    def save_to_database(
        self,
        session: Session,
        standings_df: DataFrame,
        team_stats_df: DataFrame,
        player_stats_df: DataFrame,
        league: LeagueType,
        season_option: SeasonType,
    ):
        """Save validated data to database"""
        pass

    def run_pipeline(self, session: Session, league: LeagueType, season_option: SeasonType):
        """Complete pipeline execution"""
        try:
            log.info(f"🔄 Running {self.sport_name} {league} {season_option} pipeline...")
            # 1. Fetch data
            standings_df, team_stats_df, player_stats_df = self.fetch_data(league, season_option)  # type: ignore

            # 2. Validate data
            self.validate_data(standings_df, team_stats_df, player_stats_df)

            # 3. Save to database
            self.save_to_database(session, standings_df, team_stats_df, player_stats_df, league, season_option)

            log.info(f"✅ {self.sport_name} {league} {season_option} pipeline completed successfully")

        except Exception as e:
            log.error(f"❌ {self.sport_name} {league} {season_option} pipeline failed: {str(e)[:500]}...")
            raise
