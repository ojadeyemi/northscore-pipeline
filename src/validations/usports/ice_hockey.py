from typing import Optional

import pandas as pd

from src.utils.logger import log
from src.validations.common_validations import validate_columns, validate_school_column

EXPECTED_ICE_HOCKEY_STANDINGS_COLUMNS = [
    "team_name",
    "games_played",
    "total_wins",
    "total_losses",
    "goals_for",
    "goals_against",
    "total_points",
    "conference",
]

EXPECTED_ICE_HOCKEY_TEAM_STATS_COLUMNS = [
    "team_name",
    "games_played",
    "goals",
    "assists",
    "goals_per_game",
    "shots",
    "penalty_minutes",
    "power_play_goals",
    "power_play_opportunities",
    "power_play_percentage",
    "power_play_goals_against",
    "times_short_handed",
    "penalty_kill_percentage",
    "short_handed_goals",
    "short_handed_goals_against",
    "goals_against",
    "goals_against_average",
    "saves",
    "save_percentage",
    "empty_net_goals_against",
    "conference",
]

EXPECTED_ICE_HOCKEY_PLAYERS_COLUMNS = [
    "lastname_initials",
    "first_name",
    "school",
    "games_played",
    "goals",
    "assists",
    "points",
    "penalty_minutes",
    "plus_minus",
    "power_play_goals",
    "short_handed_goals",
    "empty_net_goals",
    "game_winning_goals",
    "game_tying_goals",
    "hat_tricks",
    "shots_on_goal",
    "role",
    "goalie_games_played",
    "goalie_games_started",
    "goalie_minutes_played",
    "goalie_goals_against",
    "goalie_goals_against_average",
    "goalie_saves",
    "goalie_save_percentage",
    "goalie_wins",
    "goalie_losses",
    "goalie_ties",
    "goalie_win_percentage",
]


def validate_ice_hockey_data(
    standings_df: Optional[pd.DataFrame], team_stats_df: pd.DataFrame, player_stats_df: pd.DataFrame
):
    """Validate ice hockey data using exact test data column expectations"""

    if standings_df is not None and not standings_df.empty:
        validate_columns(standings_df, EXPECTED_ICE_HOCKEY_STANDINGS_COLUMNS, "Ice Hockey Standings")
        validate_school_column(standings_df, "team_name")
        log.debug("✅ Ice hockey standings validation passed")

    if team_stats_df is not None and not team_stats_df.empty:
        validate_columns(team_stats_df, EXPECTED_ICE_HOCKEY_TEAM_STATS_COLUMNS, "Ice Hockey Team Stats")
        validate_school_column(team_stats_df, "team_name")
        log.debug("✅ Ice hockey team stats validation passed")

    if player_stats_df is not None and not player_stats_df.empty:
        validate_columns(player_stats_df, EXPECTED_ICE_HOCKEY_PLAYERS_COLUMNS, "Ice Hockey Player Stats")
        validate_school_column(player_stats_df, "school")

        # Ice hockey specific validation - role should be 'skater' or 'goalie'
        if "role" in player_stats_df.columns:
            valid_roles = {"skater", "goalie"}
            invalid_roles = player_stats_df[~player_stats_df["role"].isin(valid_roles)]
            if not invalid_roles.empty:
                bad_roles = invalid_roles["role"].unique()
                raise ValueError(f"Ice hockey players have invalid roles: {bad_roles}")

        log.debug("✅ Ice hockey player stats validation passed")
