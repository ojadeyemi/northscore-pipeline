import pandas as pd

from src.utils.constants import VALID_USPORTS_SCHOOLS
from src.utils.logger import log


def validate_school_column(df: pd.DataFrame, school_column: str):
    """Validate U Sports school names"""
    invalid = df[~df[school_column].isin(VALID_USPORTS_SCHOOLS)]

    if not invalid.empty:
        bad_values = invalid[school_column].unique()
        raise ValueError(f"Invalid school names found in column '{school_column}': {bad_values}")


def validate_columns(df: pd.DataFrame, expected_cols: list[str], df_name: str):
    """Validate column names"""
    actual = set(df.columns)
    expected = set(expected_cols)
    missing = expected - actual

    if missing:
        raise ValueError(f"{df_name} is missing columns: {missing}")
    extra = actual - expected
    if extra:
        log.warning(f"{df_name} has extra columns: {extra}")
