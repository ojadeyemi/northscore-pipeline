from pandas import DataFrame
from sqlalchemy.orm import Session
from usports.base.types import LeagueType, SeasonType
from usports.ice_hockey import usports_ice_hockey_players, usports_ice_hockey_standings, usports_ice_hockey_teams

from src.database.models.usports.ice_hockey import IceHockeyPlayerStats, IceHockeyStandings, IceHockeyTeamStats
from src.pipelines.usports.base import BaseSportPipeline
from src.validations.usports.ice_hockey import validate_ice_hockey_data


class IceHockeyPipeline(BaseSportPipeline):
    def __init__(self):
        super().__init__("ice_hockey")

    def fetch_data(self, league: LeagueType, season_option: SeasonType):
        """Fetch ice hockey data from USports package"""
        standings_df = None
        if season_option == "regular":
            standings_df = usports_ice_hockey_standings(league)

        team_stats_df = usports_ice_hockey_teams(league, season_option)
        player_stats_df = usports_ice_hockey_players(league, season_option)

        return standings_df, team_stats_df, player_stats_df

    def validate_data(self, standings_df: DataFrame, team_stats_df: DataFrame, player_stats_df: DataFrame):
        """Validate ice hockey data using test data columns"""
        validate_ice_hockey_data(standings_df, team_stats_df, player_stats_df)

    def save_to_database(
        self,
        session: Session,
        standings_df: DataFrame,
        team_stats_df: DataFrame,
        player_stats_df: DataFrame,
        league,
        season_option,
    ):
        """Save ice hockey data to unified tables"""

        # Save standings (regular season only)
        if standings_df is not None and season_option == "regular":
            session.query(IceHockeyStandings).filter_by(league=league).delete()

            standings_df = standings_df.copy()
            standings_df["league"] = league

            for _, row in standings_df.iterrows():
                standing = IceHockeyStandings(**row.to_dict())
                session.add(standing)

        # Save team stats
        if team_stats_df is not None and not team_stats_df.empty:
            session.query(IceHockeyTeamStats).filter_by(league=league, season_option=season_option).delete()

            team_stats_df = team_stats_df.copy()
            team_stats_df["league"] = league
            team_stats_df["season_option"] = season_option

            for _, row in team_stats_df.iterrows():
                team_stat = IceHockeyTeamStats(**row.to_dict())
                session.add(team_stat)

        # Save player stats
        if player_stats_df is not None and not player_stats_df.empty:
            session.query(IceHockeyPlayerStats).filter_by(league=league, season_option=season_option).delete()

            player_stats_df = player_stats_df.copy()
            player_stats_df["league"] = league
            player_stats_df["season_option"] = season_option

            for _, row in player_stats_df.iterrows():
                player_stat = IceHockeyPlayerStats(**row.to_dict())
                session.add(player_stat)

        session.commit()
