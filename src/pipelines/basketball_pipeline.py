from pathlib import Path
from typing import Literal

import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session
from usports.basketball import usport_players_stats, usport_team_stats

from src.database.models.basketball import (
    BasePlayer,
    BasePlayoffTeam,
    BaseTeam,
    MenChampionshipPlayer,
    MenChampionshipTeam,
    MenPlayer,
    MenPlayerPlayoffs,
    MenTeam,
    MenTeamPlayoffs,
    WomenChampionshipPlayer,
    WomenChampionshipTeam,
    WomenPlayer,
    WomenPlayerPlayoffs,
    WomenTeam,
    WomenTeamPlayoffs,
)
from src.utils.logger import log
from src.validations.basketball_validations import validate_player_data, validate_team_data

data_path = Path("data/basketball")

LeagueType = Literal["m", "men", "w", "women"]
SeasonOptionType = Literal["regular", "playoffs", "championship"]


categories: list[
    dict[str, LeagueType | SeasonOptionType | type[BaseTeam] | type[BasePlayoffTeam] | type[BasePlayer]]
] = [
    {"league": "m", "season_option": "regular", "team_model": MenTeam, "player_model": MenPlayer},
    {"league": "m", "season_option": "playoffs", "team_model": MenTeamPlayoffs, "player_model": MenPlayerPlayoffs},
    {
        "league": "m",
        "season_option": "championship",
        "team_model": MenChampionshipTeam,
        "player_model": MenChampionshipPlayer,
    },
    {"league": "w", "season_option": "regular", "team_model": WomenTeam, "player_model": WomenPlayer},
    {"league": "w", "season_option": "playoffs", "team_model": WomenTeamPlayoffs, "player_model": WomenPlayerPlayoffs},
    {
        "league": "w",
        "season_option": "championship",
        "team_model": WomenChampionshipTeam,
        "player_model": WomenChampionshipPlayer,
    },
]


def fetch_and_save_basketball_data(filter_categories=None):
    """Fetch and save U Sports basketball data in csv files"""
    log.info("Fetching basketball team and player stats...")

    data_path = Path("data/basketball")
    data_path.mkdir(parents=True, exist_ok=True)

    categories_to_process = categories
    if filter_categories:
        categories_to_process = [
            cat for cat in categories if (cat["league"], cat["season_option"]) in filter_categories
        ]

    for category in categories_to_process:
        league: LeagueType = category["league"]  # type:ignore
        season_option: SeasonOptionType = category["season_option"]  # type: ignore

        team_df = usport_team_stats(league=league, season_option=season_option)
        player_df = usport_players_stats(league=league, season_option=season_option)

        validate_team_data(team_df, season_type=season_option)
        validate_player_data(player_df)

        team_df.to_csv(data_path / f"{league}_{season_option}_teams.csv", index=False)
        player_df.to_csv(data_path / f"{league}_{season_option}_players.csv", index=False)

    log.info("Basketball data fetched, validated, and saved as CSV.")


def update_basketball_db(session: Session, filter_categories=None):
    """Update U Sports basketball data in db"""
    log.info("Updating basketball database from CSV files...")

    categories_to_process = categories
    if filter_categories:
        categories_to_process = [
            cat for cat in categories if (cat["league"], cat["season_option"]) in filter_categories
        ]

    ordered_categories = []
    for league in ["m", "w"]:  # type: ignore
        ordered_categories.extend(
            [cat for cat in categories_to_process if cat["league"] == league and cat["season_option"] == "championship"]
        )
        ordered_categories.extend(
            [cat for cat in categories_to_process if cat["league"] == league and cat["season_option"] == "playoffs"]
        )
        ordered_categories.extend(
            [cat for cat in categories_to_process if cat["league"] == league and cat["season_option"] == "regular"]
        )

    # First, delete all players for all categories
    with session.begin():
        for category in ordered_categories:
            player_model = category["player_model"]  # type: ignore
            session.query(player_model).delete()

    # Then, delete and recreate teams and players
    for category in ordered_categories:
        league: LeagueType = category["league"]  # type:ignore
        season_option: SeasonOptionType = category["season_option"]  # type: ignore
        team_model: type[BaseTeam] | type[BasePlayoffTeam] = category["team_model"]  # type: ignore
        player_model: type[BasePlayer] = category["player_model"]  # type: ignore

        csv_path = data_path / f"{league}_{season_option}_teams.csv"
        player_csv_path = data_path / f"{league}_{season_option}_players.csv"

        if not csv_path.exists() or not player_csv_path.exists():
            log.warning(f"CSV files for {league}_{season_option} not found. Skipping.")
            continue

        team_df = pd.read_csv(csv_path)
        player_df = pd.read_csv(player_csv_path)

        try:
            with session.begin():
                # Players already deleted in previous step
                session.query(team_model).delete()

                teams = [team_model(**row.to_dict()) for _, row in team_df.iterrows()]
                session.bulk_save_objects(teams)

                team_map = {team.team_name: team.id for team in session.query(team_model).all()}

                players = []
                for _, row in player_df.iterrows():
                    team_id = team_map.get(row["school"])
                    if team_id:
                        player_data = row.to_dict()
                        player_data["team_id"] = team_id

                        if season_option == "playoffs" and "regular_team_id" in player_model.__table__.columns:
                            regular_team_model = MenTeam if league == "m" else WomenTeam
                            regular_team = (
                                session.query(regular_team_model)
                                .filter(func.lower(regular_team_model.team_name) == func.lower(row["school"]))
                                .first()
                            )
                            if regular_team:
                                player_data["regular_team_id"] = regular_team.id

                        player = player_model(**player_data)
                        players.append(player)

                session.bulk_save_objects(players)

            log.info(f"Successfully updated {league.upper()}_{season_option.upper()} basketball data.")
        except Exception as e:
            session.rollback()
            log.error(f"Failed to update {league.upper()}_{season_option.upper()} basketball data: {e}", exc_info=True)
            raise
