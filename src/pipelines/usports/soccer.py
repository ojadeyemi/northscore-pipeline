import logfire
from pandas import DataFrame
from sqlalchemy.orm import Session
from usports.base.types import LeagueType, SeasonType
from usports.soccer import usports_soccer_players, usports_soccer_standings, usports_soccer_teams

from src.database.models.usports.soccer import SoccerPlayerStats, SoccerStandings, SoccerTeamStats
from src.pipelines.usports.base import BaseSportPipeline
from src.validations.usports.soccer import validate_soccer_data


class SoccerPipeline(BaseSportPipeline):
    def __init__(self):
        super().__init__("soccer")

    def fetch_data(self, league: LeagueType, season_option: SeasonType):
        """Fetch soccer data from USports package"""
        standings_df = None
        if season_option == "regular":
            standings_df = usports_soccer_standings(league)

        team_stats_df = usports_soccer_teams(league, season_option)
        player_stats_df = usports_soccer_players(league, season_option)
        # drop rows of player df where first name is NaN
        player_stats_df = player_stats_df.dropna(subset=["first_name"])

        return standings_df, team_stats_df, player_stats_df

    def validate_data(self, standings_df: DataFrame, team_stats_df: DataFrame, player_stats_df: DataFrame):
        """Validate soccer data using test data columns"""
        validate_soccer_data(standings_df, team_stats_df, player_stats_df)

    def save_to_database(
        self,
        session: Session,
        standings_df: DataFrame,
        team_stats_df: DataFrame,
        player_stats_df: DataFrame,
        league,
        season_option,
    ):
        """Save soccer data to unified tables"""

        # Save standings (regular season only)
        if standings_df is not None and season_option == "regular":
            with logfire.span("save_standings", league=league, records=len(standings_df)):
                session.query(SoccerStandings).filter_by(league=league).delete()

                standings_df = standings_df.copy()
                standings_df["league"] = league

                for _, row in standings_df.iterrows():
                    standing = SoccerStandings(**row.to_dict())
                    session.add(standing)

        # Save team stats
        if team_stats_df is not None and not team_stats_df.empty:
            with logfire.span("save_team_stats", league=league, season=season_option, records=len(team_stats_df)):
                session.query(SoccerTeamStats).filter_by(league=league, season_option=season_option).delete()

                team_stats_df = team_stats_df.copy()
                team_stats_df["league"] = league
                team_stats_df["season_option"] = season_option

                for _, row in team_stats_df.iterrows():
                    team_stat = SoccerTeamStats(**row.to_dict())
                    session.add(team_stat)

        # Save player stats
        if player_stats_df is not None and not player_stats_df.empty:
            with logfire.span("save_player_stats", league=league, season=season_option, records=len(player_stats_df)):
                session.query(SoccerPlayerStats).filter_by(league=league, season_option=season_option).delete()

                player_stats_df = player_stats_df.copy()
                player_stats_df["league"] = league
                player_stats_df["season_option"] = season_option

                for _, row in player_stats_df.iterrows():
                    player_stat = SoccerPlayerStats(**row.to_dict())
                    session.add(player_stat)

        session.commit()
