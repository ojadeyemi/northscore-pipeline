from typing import Optional

import pandas as pd

from src.utils.logger import log
from src.validations.common_validations import validate_columns, validate_school_column

EXPECTED_BASKETBALL_STANDINGS_COLUMNS = [
    "team_name",
    "games_played",
    "total_wins",
    "total_losses",
    "win_percentage",
    "total_points",
    "total_points_against",
    "conference",
]

EXPECTED_BASKETBALL_TEAM_STATS_COLUMNS = [
    "team_name",
    "games_played",
    "points_per_game",
    "field_goal_made",
    "field_goal_attempted",
    "field_goal_percentage",
    "three_pointers_made",
    "three_pointers_attempted",
    "three_point_percentage",
    "free_throws_made",
    "free_throws_attempted",
    "free_throw_percentage",
    "offensive_rebounds_per_game",
    "defensive_rebounds_per_game",
    "total_rebounds_per_game",
    "rebound_margin",
    "assists_per_game",
    "turnovers_per_game",
    "steals_per_game",
    "blocks_per_game",
    "team_fouls_per_game",
    "offensive_efficiency",
    "defensive_efficiency",
    "net_efficiency",
    "net_efficiency_against",
    "field_goal_made_against",
    "field_goal_attempted_against",
    "field_goal_percentage_against",
    "three_pointers_made_against",
    "three_pointers_attempted_against",
    "three_point_percentage_against",
    "offensive_rebounds_per_game_against",
    "defensive_rebounds_per_game_against",
    "total_rebounds_per_game_against",
    "rebound_margin_against",
    "assists_per_game_against",
    "turnovers_per_game_against",
    "steals_per_game_against",
    "blocks_per_game_against",
    "team_fouls_per_game_against",
    "points_per_game_against",
    "conference",
]

EXPECTED_BASKETBALL_PLAYERS_COLUMNS = [
    "lastname_initials",
    "first_name",
    "school",
    "games_played",
    "games_started",
    "minutes_played",
    "field_goal_made",
    "field_goal_attempted",
    "field_goal_percentage",
    "three_pointers_made",
    "three_pointers_attempted",
    "three_pointers_percentage",
    "free_throws_made",
    "free_throws_attempted",
    "free_throws_percentage",
    "total_points",
    "offensive_rebounds",
    "defensive_rebounds",
    "total_rebounds",
    "assists",
    "turnovers",
    "steals",
    "blocks",
    "assist_to_turnover_ratio",
    "personal_fouls",
    "disqualifications",
]


def validate_basketball_data(
    standings_df: Optional[pd.DataFrame], team_stats_df: pd.DataFrame, player_stats_df: pd.DataFrame
):
    """Validate basketball data using expected test data columns"""

    if standings_df is not None:
        validate_columns(standings_df, EXPECTED_BASKETBALL_STANDINGS_COLUMNS, "Basketball Standings")
        validate_school_column(standings_df, "team_name")
        log.debug("✅ Basketball standings validation passed")

    if team_stats_df is not None and not team_stats_df.empty:
        validate_columns(team_stats_df, EXPECTED_BASKETBALL_TEAM_STATS_COLUMNS, "Basketball Team Stats")
        validate_school_column(team_stats_df, "team_name")
        log.debug("✅ Basketball team stats validation passed")

    if player_stats_df is not None and not player_stats_df.empty:
        validate_columns(player_stats_df, EXPECTED_BASKETBALL_PLAYERS_COLUMNS, "Basketball Player Stats")
        validate_school_column(player_stats_df, "school")
        log.debug("✅ Basketball player stats validation passed")
