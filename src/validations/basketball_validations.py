import pandas as pd

from src.utils.constants import BASKETBALL_PLAYER_COLUMNS, BASKETBALL_TEAM_COLUMNS
from src.utils.logger import log

from .common_validations import validate_columns, validate_school_column


def validate_team_data(df: pd.DataFrame):
    """Validate U Sports basketball team table column names"""
    validate_columns(df, BASKETBALL_TEAM_COLUMNS, "Team")

    validate_school_column(df, school_column="team_name")
    log.info("Team data validated successfully.")


def validate_player_data(df: pd.DataFrame):
    """Validate U Sports basketball player table column names"""
    validate_columns(df, BASKETBALL_PLAYER_COLUMNS, "Players")
    validate_school_column(df, school_column="school")
    log.info("Players data validated successfully.")
