from usports.base.constants import (
    BASKETBALL,
    FOOTBALL,
    ICE_HOCKEY,
    SOCCER,
    VOLLEYBALL,
)
from usports.base.types import SeasonType


def get_active_seasons_by_month(month: int) -> dict[str, list[SeasonType]]:
    """Determine what data to fetch based on current month"""

    # Fall sports: football, soccer (Sept-Dec)
    # Winter sports: basketball, ice_hockey, volleyball (Jan-Mar)

    if month == 9:  # September: Fall sports regular season only
        return {
            FOOTBALL: ["regular"],
            SOCCER: ["regular"],
        }

    if month == 10:  # October: All sports regular season
        return {
            FOOTBALL: ["regular"],
            SOCCER: ["regular"],
            BASKETBALL: ["regular"],
            ICE_HOCKEY: ["regular"],
            VOLLEYBALL: ["regular"],
        }

    if month == 11:  # November: Fall playoffs start, winter regular season starts
        return {
            FOOTBALL: ["regular", "playoffs", "championship"],
            SOCCER: ["regular", "playoffs", "championship"],
            BASKETBALL: ["regular"],
            ICE_HOCKEY: ["regular"],
            VOLLEYBALL: ["regular"],
        }

    if month == 12:  # December: Fall championships, winter regular season continues
        return {
            FOOTBALL: ["regular", "playoffs", "championship"],
            SOCCER: ["regular", "playoffs", "championship"],
            BASKETBALL: ["regular"],
            ICE_HOCKEY: ["regular"],
            VOLLEYBALL: ["regular"],
        }

    if month == 1:  # January: Winter regular season
        return {
            BASKETBALL: ["regular"],
            ICE_HOCKEY: ["regular"],
            VOLLEYBALL: ["regular"],
        }

    if month == 2:  # February: Winter playoffs
        return {
            BASKETBALL: ["regular", "playoffs"],
            ICE_HOCKEY: ["regular", "playoffs"],
            VOLLEYBALL: ["regular", "playoffs"],
        }

    if month == 3:  # March: Winter championships
        return {
            BASKETBALL: ["regular", "playoffs", "championship"],
            ICE_HOCKEY: ["regular", "playoffs", "championship"],
            VOLLEYBALL: ["regular", "playoffs", "championship"],
        }

    return {}
