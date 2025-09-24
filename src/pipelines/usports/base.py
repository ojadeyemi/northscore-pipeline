from abc import ABC, abstractmethod

import logfire
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
        with logfire.span(f"{self.sport_name} pipeline"):
            try:
                log.info(f"\n🔄 Running {self.sport_name} {league} {season_option} pipeline...")

                # 1. Fetch data
                with logfire.span(
                    "fetch_data for {sport} {league} {season}",
                    sport=self.sport_name,
                    league=league,
                    season=season_option,
                ):
                    standings_df, team_stats_df, player_stats_df = self.fetch_data(league, season_option)  # type: ignore
                    logfire.info(
                        "Data fetched",
                        teams=len(team_stats_df),
                        players=len(player_stats_df),
                        standings=len(standings_df) if standings_df is not None else 0,
                    )

                # 2. Validate data
                with logfire.span(
                    "validate_data for {sport} {league} {season}",
                    sport=self.sport_name,
                    league=league,
                    season=season_option,
                ):
                    self.validate_data(standings_df, team_stats_df, player_stats_df)

                # 3. Save to database
                with logfire.span(
                    "save_to_database for {sport} {league} {season}",
                    sport=self.sport_name,
                    league=league,
                    season=season_option,
                ):
                    self.save_to_database(session, standings_df, team_stats_df, player_stats_df, league, season_option)

                log.info(f"✅ {self.sport_name} {league} {season_option} pipeline completed successfully\n")
                logfire.info(f"{self.sport_name} pipeline completed", league=league, season=season_option)

            except Exception as e:
                log.error(f"❌ {self.sport_name} {league} {season_option} pipeline failed: {str(e)[:500]}...\n")
                logfire.error(f"{self.sport_name} pipeline failed", league=league, season=season_option, error=str(e))
                raise
