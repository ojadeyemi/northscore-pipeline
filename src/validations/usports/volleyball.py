from typing import Optional

import pandas as pd

from src.utils.logger import log
from src.validations.common_validations import validate_columns, validate_school_column

EXPECTED_VOLLEYBALL_STANDINGS_COLUMNS = [
    "team_name",
    "games_played",
    "total_wins",
    "total_losses",
    "win_percentage",
    "sets_for",
    "sets_against",
    "points",
    "conference",
]

EXPECTED_VOLLEYBALL_TEAM_STATS_COLUMNS = [
    "team_name",
    "matches_played",
    "sets_played",
    "kills",
    "kills_per_set",
    "errors",
    "total_attacks",
    "hitting_percentage",
    "assists",
    "assists_per_set",
    "points",
    "points_per_set",
    "digs",
    "digs_per_set",
    "block_solos",
    "block_assists",
    "total_blocks",
    "blocks_per_set",
    "service_aces",
    "service_aces_per_set",
    "service_errors",
    "receptions",
    "reception_errors",
    "conference",
]

EXPECTED_VOLLEYBALL_PLAYERS_COLUMNS = [
    "lastname_initials",
    "first_name",
    "school",
    "matches_played",
    "sets_played",
    "kills",
    "kills_per_set",
    "errors",
    "total_attacks",
    "total_attacks_per_set",
    "hitting_percentage",
    "assists",
    "assists_per_set",
    "points",
    "points_per_set",
    "digs",
    "digs_per_set",
    "block_solos",
    "block_assists",
    "total_blocks",
    "blocks_per_set",
    "serve_attempts",
    "service_aces",
    "service_aces_per_set",
    "service_errors",
    "receptions",
    "reception_errors",
]


def validate_volleyball_data(
    standings_df: Optional[pd.DataFrame], team_stats_df: pd.DataFrame, player_stats_df: pd.DataFrame
):
    """Validate volleyball data using exact test data column expectations"""

    if standings_df is not None and not standings_df.empty:
        validate_columns(standings_df, EXPECTED_VOLLEYBALL_STANDINGS_COLUMNS, "Volleyball Standings")
        validate_school_column(standings_df, "team_name")
        log.debug("✅ Volleyball standings validation passed")

    if team_stats_df is not None and not team_stats_df.empty:
        validate_columns(team_stats_df, EXPECTED_VOLLEYBALL_TEAM_STATS_COLUMNS, "Volleyball Team Stats")
        validate_school_column(team_stats_df, "team_name")

        # Volleyball specific validation - sets should be >= matches
        if "matches_played" in team_stats_df.columns and "sets_played" in team_stats_df.columns:
            invalid_data = team_stats_df[team_stats_df["sets_played"] < team_stats_df["matches_played"]]
            if not invalid_data.empty:
                log.warning(f"Found {len(invalid_data)} teams where sets_played < matches_played")

        log.debug("✅ Volleyball team stats validation passed")

    if player_stats_df is not None and not player_stats_df.empty:
        validate_columns(player_stats_df, EXPECTED_VOLLEYBALL_PLAYERS_COLUMNS, "Volleyball Player Stats")
        validate_school_column(player_stats_df, "school")

        # Volleyball specific validation - sets should be >= matches for players too
        if "matches_played" in player_stats_df.columns and "sets_played" in player_stats_df.columns:
            invalid_data = player_stats_df[player_stats_df["sets_played"] < player_stats_df["matches_played"]]
            if not invalid_data.empty:
                log.warning(f"Found {len(invalid_data)} players where sets_played < matches_played")

        log.debug("✅ Volleyball player stats validation passed")
