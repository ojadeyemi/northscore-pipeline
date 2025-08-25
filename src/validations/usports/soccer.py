from typing import Optional

import pandas as pd

from src.utils.logger import log
from src.validations.common_validations import validate_columns, validate_school_column

EXPECTED_SOCCER_STANDINGS_COLUMNS = [
    "team_name",
    "games_played",
    "total_wins",
    "total_losses",
    "ties",
    "goals_for",
    "goals_against",
    "points",
    "conference",
]

EXPECTED_SOCCER_TEAM_STATS_COLUMNS = [
    "team_name",
    "games_played",
    "shots",
    "goals",
    "goals_per_game",
    "assists",
    "points",
    "shot_percentage",
    "shots_per_game",
    "goals_against",
    "goals_against_average",
    "saves",
    "shutouts",
    "yellow_cards",
    "red_cards",
    "corner_kicks",
    "conference",
]

EXPECTED_SOCCER_PLAYERS_COLUMNS = [
    "lastname_initials",
    "first_name",
    "school",
    "position",
    "games_played",
    "games_started",
    "goals",
    "assists",
    "points",
    "shots",
    "shot_percentage",
    "shots_on_goal",
    "sog_percentage",
    "yellow_cards",
    "red_cards",
    "penalty_kicks",
    "game_winning_goals",
    "goalie_games_started",
    "goalie_goals_against",
    "goalie_saves",
    "goalie_save_percentage",
    "goalie_wins",
    "goalie_losses",
    "goalie_ties",
    "goalie_shutouts",
    "goalie_minutes_played",
]


def validate_soccer_data(
    standings_df: Optional[pd.DataFrame], team_stats_df: pd.DataFrame, player_stats_df: pd.DataFrame
):
    """Validate soccer data using exact test data column expectations"""

    if standings_df is not None and not standings_df.empty:
        validate_columns(standings_df, EXPECTED_SOCCER_STANDINGS_COLUMNS, "Soccer Standings")
        validate_school_column(standings_df, "team_name")
        log.debug("✅ Soccer standings validation passed")

    if team_stats_df is not None and not team_stats_df.empty:
        validate_columns(team_stats_df, EXPECTED_SOCCER_TEAM_STATS_COLUMNS, "Soccer Team Stats")
        validate_school_column(team_stats_df, "team_name")
        log.debug("✅ Soccer team stats validation passed")

    if player_stats_df is not None and not player_stats_df.empty:
        validate_columns(player_stats_df, EXPECTED_SOCCER_PLAYERS_COLUMNS, "Soccer Player Stats")
        validate_school_column(player_stats_df, "school")

        # Soccer specific validation - position should be 'goalie' or 'field'
        if "position" in player_stats_df.columns:
            valid_positions = {"goalie", "field"}
            invalid_positions = player_stats_df[~player_stats_df["position"].isin(valid_positions)]
            if not invalid_positions.empty:
                bad_positions = invalid_positions["position"].unique()
                raise ValueError(f"Soccer players have invalid positions: {bad_positions}")

        log.debug("✅ Soccer player stats validation passed")
