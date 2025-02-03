from pathlib import Path
from typing import Literal

import pandas as pd
from sqlalchemy.orm import Session
from usports.basketball import usport_players_stats, usport_team_stats

from src.database.models.basketball import MenPlayer, MenTeam, WomenPlayer, WomenTeam
from src.utils.logger import log
from src.validations.basketball_validations import validate_player_data, validate_team_data

data_path = Path("data/basketball")

LeagueType = Literal["m", "men", "w", "women"]

categories: list[
    dict[str, LeagueType | type[MenTeam] | type[MenPlayer]]
    | dict[str, LeagueType | type[WomenTeam] | type[WomenPlayer]]
] = [
    {"league": "m", "team_model": MenTeam, "player_model": MenPlayer},
    {"league": "w", "team_model": WomenTeam, "player_model": WomenPlayer},
]


def fetch_and_save_basketball_data():
    """Fetch and save U Sports baskeball data in csv files"""
    log.info("Fetching basketball team and player stats...")

    data_path = Path("data/basketball")
    data_path.mkdir(parents=True, exist_ok=True)

    for category in categories:
        league: LeagueType = category["league"]  # type: ignore

        # Fetch data
        team_df = usport_team_stats(league=league, season_option="regular")
        player_df = usport_players_stats(league=league, season_option="regular")

        # Validate data
        validate_team_data(team_df)
        validate_player_data(player_df)

        # Save CSV files
        team_df.to_csv(data_path / f"{league}_teams.csv", index=False)
        player_df.to_csv(data_path / f"{league}_players.csv", index=False)

    log.info("Basketball data fetched, validated, and saved as CSV.")


def update_basketball_db(session: Session):
    """Update U Sports basketball data in db"""
    log.info("Updating basketball database from CSV files...")

    for category in categories:
        league: LeagueType = category["league"]  # type:ignore
        team_model: type[MenTeam] | type[WomenTeam] = category["team_model"]  # type: ignore
        player_model: type[MenPlayer] | type[WomenPlayer] = category["player_model"]  # type: ignore

        team_df = pd.read_csv(data_path / f"{league}_teams.csv")
        player_df = pd.read_csv(data_path / f"{league}_players.csv")

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

            log.info(f"Successfully updated {league.upper()} basketball data.")
        except Exception as e:
            session.rollback()
            log.error(f"Failed to update {league.upper()} basketball data: {e}", exc_info=True)
            raise

    log.info("Basketball database update completed successfully.")
