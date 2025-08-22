"""Main script to fetch all USports data based on current season timing"""

from datetime import datetime
from pathlib import Path

from src.pipelines.seasonal_logic import get_active_seasons_by_month
from src.pipelines.usports import (
    BasketballPipeline,
    FootballPipeline,
    IceHockeyPipeline,
    SoccerPipeline,
    VolleyballPipeline,
)
from src.utils.constants import BASKETBALL, FOOTBALL, ICE_HOCKEY, SOCCER, VOLLEYBALL

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SPORT_PIPELINES = {
    BASKETBALL: BasketballPipeline(),
    FOOTBALL: FootballPipeline(),
    ICE_HOCKEY: IceHockeyPipeline(),
    VOLLEYBALL: VolleyballPipeline(),
    SOCCER: SoccerPipeline(),
}


def fetch_all_data():
    """Fetch data for all active sports based on current month"""
    now = datetime.now()
    current_month_num = now.month
    current_month_name = now.strftime("%B")
    active_seasons = get_active_seasons_by_month(current_month_num)

    print(f"🗓️  Current month: {current_month_name}")
    print(f"📊 Active seasons: {active_seasons}")

    for sport, season_options in active_seasons.items():
        if sport not in SPORT_PIPELINES:
            print(f"⚠️  No pipeline for {sport}")
            continue

        pipeline = SPORT_PIPELINES[sport]

        # Determine leagues for this sport
        leagues = ["m", "w"] if sport != "football" else ["m"]

        for league in leagues:
            for season_option in season_options:
                try:
                    print(f"🔄 Fetching {sport} {league} {season_option}...")
                    standings_df, team_stats_df, player_stats_df = pipeline.fetch_data(league, season_option)  # type: ignore

                    # Save to CSV for inspection
                    if standings_df is not None:
                        standings_df.to_csv(DATA_DIR / f"{sport}_{league}_{season_option}_standings.csv", index=False)

                    team_stats_df.to_csv(DATA_DIR / f"{sport}_{league}_{season_option}_teams.csv", index=False)
                    player_stats_df.to_csv(DATA_DIR / f"{sport}_{league}_{season_option}_players.csv", index=False)

                    print(f"✅ Saved {sport} {league} {season_option} to CSV")

                except Exception as e:
                    print(f"❌ Failed to fetch {sport} {league} {season_option}: {e}")


if __name__ == "__main__":
    fetch_all_data()
