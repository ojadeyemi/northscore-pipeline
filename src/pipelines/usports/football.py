import logfire
from sqlalchemy.orm import Session
from usports.base.types import LeagueType, SeasonType
from usports.football import usports_fball_players, usports_fball_standings, usports_fball_teams

from src.database.models.usports.football import FootballPlayerStats, FootballStandings, FootballTeamStats
from src.pipelines.usports.base import BaseSportPipeline
from src.validations.usports.football import validate_football_data


class FootballPipeline(BaseSportPipeline):
    def __init__(self):
        super().__init__("football")

    def fetch_data(self, league: LeagueType, season_option: SeasonType):
        """Fetch football data - league is always 'm' for football"""
        standings_df = None
        if season_option == "regular":
            standings_df = usports_fball_standings()  # No league param for football

        team_stats_df = usports_fball_teams(season_option)
        player_stats_df = usports_fball_players(season_option)
        # drop rows of player df where first name is NaN
        player_stats_df = player_stats_df.dropna(subset=["first_name"])

        return standings_df, team_stats_df, player_stats_df

    def validate_data(self, standings_df, team_stats_df, player_stats_df):
        """Validate football data using test data columns"""
        validate_football_data(standings_df, team_stats_df, player_stats_df)

    def save_to_database(self, session: Session, standings_df, team_stats_df, player_stats_df, league, season_option):
        """Save football data to unified tables"""
        # Force league to 'm' for football since it's men only
        league = "m"

        # Save standings (regular season only)
        if standings_df is not None and season_option == "regular":
            with logfire.span("save_standings", league=league, records=len(standings_df)):
                session.query(FootballStandings).delete()  # Football only has men

                standings_df = standings_df.copy()
                standings_df["league"] = league

                for _, row in standings_df.iterrows():
                    standing = FootballStandings(**row.to_dict())
                    session.add(standing)

        # Save team stats
        if team_stats_df is not None and not team_stats_df.empty:
            with logfire.span("save_team_stats", league=league, season=season_option, records=len(team_stats_df)):
                session.query(FootballTeamStats).filter_by(league=league, season_option=season_option).delete()

                team_stats_df = team_stats_df.copy()
                team_stats_df["league"] = league
                team_stats_df["season_option"] = season_option

                for _, row in team_stats_df.iterrows():
                    team_stat = FootballTeamStats(**row.to_dict())
                    session.add(team_stat)

        # Save player stats
        if player_stats_df is not None and not player_stats_df.empty:
            with logfire.span("save_player_stats", league=league, season=season_option, records=len(player_stats_df)):
                session.query(FootballPlayerStats).filter_by(league=league, season_option=season_option).delete()

                player_stats_df = player_stats_df.copy()
                player_stats_df["league"] = league
                player_stats_df["season_option"] = season_option

                for _, row in player_stats_df.iterrows():
                    player_stat = FootballPlayerStats(**row.to_dict())
                    session.add(player_stat)

        session.commit()
