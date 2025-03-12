import pandas as pd

from src.utils.constants import (
    BASKETBALL_PLAYER_COLUMNS,
    BASKETBALL_PLAYOFF_TEAM_COLUMNS,
    BASKETBALL_TEAM_COLUMNS,
    CHAMPIONSHIP,
    PLAYOFFS,
    REGULAR,
)
from src.utils.logger import log

from .common_validations import validate_columns, validate_school_column


def validate_team_data(df: pd.DataFrame, season_type: str = REGULAR):
    """Validate U Sports basketball team table column names based on season type"""
    if season_type.lower() == REGULAR:
        columns_to_validate = BASKETBALL_TEAM_COLUMNS
    elif season_type.lower() in [PLAYOFFS, CHAMPIONSHIP]:
        columns_to_validate = BASKETBALL_PLAYOFF_TEAM_COLUMNS
    else:
        raise ValueError(f"Invalid season type: {season_type}. Must be 'regular', 'playoffs', or 'championship'")

    validate_columns(df, columns_to_validate, f"Team ({season_type})")
    validate_school_column(df, school_column="team_name")
    log.info(f"{season_type.capitalize()} team data validated successfully.")


def validate_player_data(df: pd.DataFrame):
    """Validate U Sports basketball player table column names"""
    validate_columns(df, BASKETBALL_PLAYER_COLUMNS, "Players")
    validate_school_column(df, school_column="school")
    log.info("Players data validated successfully.")
