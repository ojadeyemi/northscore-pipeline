from pathlib import Path
from typing import Literal

import pandas as pd
from sqlalchemy.orm import Session
from usports.basketball import usport_players_stats, usport_team_stats

from src.database.models.basketball import (
    BasePlayer,
    BaseTeam,
    MenPlayer,
    MenTeam,
    WomenPlayer,
    WomenTeam,
)
from src.utils.logger import log
from src.validations.basketball_validations import validate_player_data, validate_team_data

data_path = Path("data/basketball")

LeagueType = Literal["m", "men", "w", "women"]
SeasonOptionType = Literal["regular", "playoffs", "championship"]

# TODO: handle logic of games_played_standings key error when merging stats together in usports repo first

categories: list[dict[str, LeagueType | SeasonOptionType | type[BaseTeam] | type[BasePlayer]]] = [
    {"league": "m", "season_option": "regular", "team_model": MenTeam, "player_model": MenPlayer},
    # {"league": "m", "season_option": "playoffs", "team_model": MenTeam, "player_model": MenPlayerPlayoffs},
    {"league": "w", "season_option": "regular", "team_model": WomenTeam, "player_model": WomenPlayer},
    # {"league": "w", "season_option": "playoffs", "team_model": WomenTeam, "player_model": WomenPlayerPlayoffs},
]


def fetch_and_save_basketball_data():
    """Fetch and save U Sports baskeball data in csv files"""
    log.info("Fetching basketball team and player stats...")

    data_path = Path("data/basketball")
    data_path.mkdir(parents=True, exist_ok=True)

    for category in categories:
        league: LeagueType = category["league"]  # type:ignore
        season_option: SeasonOptionType = category["season_option"]  # type: ignore

        # Fetch data
        team_df = usport_team_stats(league=league, season_option=season_option)
        player_df = usport_players_stats(league=league, season_option=season_option)

        # Validate data
        validate_team_data(team_df)
        validate_player_data(player_df)

        # Save CSV files including the season option in the filename
        team_df.to_csv(data_path / f"{league}_{season_option}_teams.csv", index=False)
        player_df.to_csv(data_path / f"{league}_{season_option}_players.csv", index=False)

    log.info("Basketball data fetched, validated, and saved as CSV.")


def update_basketball_db(session: Session):
    """Update U Sports basketball data in db"""
    log.info("Updating basketball database from CSV files...")

    for category in categories:
        league: LeagueType = category["league"]  # type:ignore
        season_option: SeasonOptionType = category["season_option"]  # type: ignore

        team_model: type[BaseTeam] = category["team_model"]  # type: ignore
        player_model: type[BasePlayer] = category["player_model"]  # type: ignore

        team_df = pd.read_csv(data_path / f"{league}_{season_option}_teams.csv")
        player_df = pd.read_csv(data_path / f"{league}_{season_option}_players.csv")

        validate_team_data(team_df)
        validate_player_data(player_df)

        try:
            with session.begin():
                session.query(player_model).delete()
                session.query(team_model).delete()

                # Insert new teams table
                teams = [team_model(**row.to_dict()) for _, row in team_df.iterrows()]
                session.bulk_save_objects(teams)

                # Map team names to team IDs
                team_map = {team.team_name: team.id for team in session.query(team_model).all()}

                # Insert players
                players = []
                for _, row in player_df.iterrows():
                    team_id = team_map.get(row["school"])
                    if team_id:
                        player = player_model(**row.to_dict(), team_id=team_id)
                        players.append(player)

                session.bulk_save_objects(players)

            log.info(f"Successfully updated {league.upper()}_{season_option.upper()} basketball data.")
        except Exception as e:
            session.rollback()
            log.error(f"Failed to update {league.upper()}_{season_option.upper()} basketball data: {e}", exc_info=True)
            raise
