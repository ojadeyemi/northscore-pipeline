from typing import Optional

import logfire
from pandas import DataFrame
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from usports.base.types import LeagueType, SeasonType
from usports.basketball import usports_bball_players, usports_bball_standings, usports_bball_teams

from src.database.models.usports.basketball import (
    BasketballPlayerStats,
    BasketballStandings,
    BasketballTeamStats,
)
from src.pipelines.seasonal_logic import REGULAR
from src.pipelines.usports.base import BaseSportPipeline
from src.utils.constants import BASKETBALL
from src.validations.usports.basketball import validate_basketball_data


class BasketballPipeline(BaseSportPipeline):
    def __init__(self):
        super().__init__(BASKETBALL)

    def fetch_data(self, league: LeagueType, season_option: SeasonType):
        """Fetch basketball data from USports package"""
        standings_df = usports_bball_standings(league) if season_option == REGULAR else None
        team_stats_df = usports_bball_teams(league, season_option)
        player_stats_df = usports_bball_players(league, season_option)
        # drop rows of player df where first name is NaN
        player_stats_df = player_stats_df.dropna(subset=["first_name"])

        return standings_df, team_stats_df, player_stats_df

    def validate_data(
        self,
        standings_df: Optional[DataFrame],
        team_stats_df: DataFrame,
        player_stats_df: DataFrame,
    ):
        """Validate basketball data using schema checks"""
        validate_basketball_data(standings_df, team_stats_df, player_stats_df)

    def _add_metadata(self, df: DataFrame, league: LeagueType, season_option: Optional[SeasonType] = None) -> DataFrame:
        """Attach metadata columns for league/season"""
        df = df.copy()
        df["league"] = league
        if season_option:
            df["season_option"] = season_option
        return df

    def save_to_database(
        self,
        session: Session,
        standings_df: Optional[DataFrame],
        team_stats_df: DataFrame,
        player_stats_df: DataFrame,
        league: LeagueType,
        season_option: SeasonType,
    ):
        """Validate and save basketball data atomically"""
        self.validate_data(standings_df, team_stats_df, player_stats_df)

        # === Standings (only regular season) ===
        if standings_df is not None and season_option == REGULAR:
            with logfire.span(
                "save_standings for {league} with {records} records", league=league, records=len(standings_df)
            ):
                standings_df = self._add_metadata(standings_df, league)
                session.query(BasketballStandings).filter_by(league=league).delete(synchronize_session=False)

                records = standings_df.to_dict(orient="records")
                stmt = insert(BasketballStandings).values(records)
                session.execute(stmt)

        # === Team stats ===
        if team_stats_df is not None:
            with logfire.span(
                "save_team_stats for {league} {season} with {records} records",
                league=league,
                season=season_option,
                records=len(team_stats_df),
            ):
                team_stats_df = self._add_metadata(team_stats_df, league, season_option)
                session.query(BasketballTeamStats).filter_by(league=league, season_option=season_option).delete(
                    synchronize_session=False
                )

                records = team_stats_df.to_dict(orient="records")
                stmt = insert(BasketballTeamStats).values(records)
                session.execute(stmt)

        # === Player stats ===
        if player_stats_df is not None:
            with logfire.span(
                "save_player_stats for {league} {season} with {records} records",
                league=league,
                season=season_option,
                records=len(player_stats_df),
            ):
                player_stats_df = self._add_metadata(player_stats_df, league, season_option)
                session.query(BasketballPlayerStats).filter_by(league=league, season_option=season_option).delete(
                    synchronize_session=False
                )

                records = player_stats_df.to_dict(orient="records")
                stmt = insert(BasketballPlayerStats).values(records)
                session.execute(stmt)

        session.commit()
