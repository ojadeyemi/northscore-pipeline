from usports.base.constants import (
    BASKETBALL,
    FOOTBALL,
    ICE_HOCKEY,
    SOCCER,
    VOLLEYBALL,
)
from usports.base.types import SeasonType

# Season type constants
REGULAR = "regular"
PLAYOFFS = "playoffs"
CHAMPIONSHIP = "championship"


def get_active_seasons_by_month(month: int) -> dict[str, list[SeasonType]]:
    """Get active sports seasons for a given month"""

    # October - Fall sports regular season
    if month == 10:
        return {
            FOOTBALL: [REGULAR],
            SOCCER: [REGULAR],
        }

    # November - Fall playoffs begin, winter sports start
    if month == 11:
        return {
            FOOTBALL: [REGULAR, PLAYOFFS],
            SOCCER: [REGULAR, PLAYOFFS],
            BASKETBALL: [REGULAR],
            ICE_HOCKEY: [REGULAR],
            VOLLEYBALL: [REGULAR],
        }

    # December - Fall championships, winter continues
    if month == 12:
        return {
            FOOTBALL: [PLAYOFFS, CHAMPIONSHIP],
            SOCCER: [PLAYOFFS, CHAMPIONSHIP],
            BASKETBALL: [REGULAR],
            ICE_HOCKEY: [REGULAR],
            VOLLEYBALL: [REGULAR],
        }

    # January - Winter sports only
    if month == 1:
        return {
            BASKETBALL: [REGULAR],
            ICE_HOCKEY: [REGULAR],
            VOLLEYBALL: [REGULAR],
        }

    # February - Winter playoffs begin
    if month == 2:
        return {
            BASKETBALL: [REGULAR, PLAYOFFS],
            ICE_HOCKEY: [REGULAR, PLAYOFFS],
            VOLLEYBALL: [REGULAR, PLAYOFFS],
        }

    # March - Winter championships
    if month == 3:
        return {
            BASKETBALL: [PLAYOFFS, CHAMPIONSHIP],
            ICE_HOCKEY: [PLAYOFFS, CHAMPIONSHIP],
            VOLLEYBALL: [PLAYOFFS, CHAMPIONSHIP],
        }

    # No active seasons for other months
    return {}
