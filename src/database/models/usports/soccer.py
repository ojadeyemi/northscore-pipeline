from sqlalchemy import Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class SoccerStandings(Base):
    """Unified soccer standings - regular season only"""

    __tablename__ = "soccer_standings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    conference: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)
    total_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_losses: Mapped[int] = mapped_column(Integer, nullable=False)
    ties: Mapped[int] = mapped_column(Integer, nullable=False)
    goals_for: Mapped[int] = mapped_column(Integer, nullable=False)
    goals_against: Mapped[int] = mapped_column(Integer, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("league", "team_name", name="uq_soccer_standings_team"),)


class SoccerTeamStats(Base):
    """Unified soccer team stats - all seasons"""

    __tablename__ = "soccer_team_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    conference: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)

    # Offensive stats
    shots: Mapped[int] = mapped_column(Integer)
    goals: Mapped[int] = mapped_column(Integer)
    goals_per_game: Mapped[float] = mapped_column(Float)
    assists: Mapped[int] = mapped_column(Integer)
    points: Mapped[int] = mapped_column(Integer)
    shot_percentage: Mapped[float] = mapped_column(Float)
    shots_per_game: Mapped[float] = mapped_column(Float)

    # Defensive stats
    goals_against: Mapped[int] = mapped_column(Integer)
    goals_against_average: Mapped[float] = mapped_column(Float)
    saves: Mapped[int] = mapped_column(Integer)
    shutouts: Mapped[int] = mapped_column(Integer)

    # Misc stats
    yellow_cards: Mapped[int] = mapped_column(Integer)
    red_cards: Mapped[int] = mapped_column(Integer)
    corner_kicks: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("league", "season_option", "team_name", name="uq_soccer_team_league_season_team"),
    )


class SoccerPlayerStats(Base):
    """Unified soccer player stats - all seasons"""

    __tablename__ = "soccer_player_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    lastname_initials: Mapped[str] = mapped_column(String(10), nullable=False)
    school: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    position: Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # 'goalie' or 'field'

    # Basic stats
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)
    games_started: Mapped[int] = mapped_column(Integer)

    # Field player stats
    goals: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    points: Mapped[int] = mapped_column(Integer)
    shots: Mapped[int] = mapped_column(Integer)
    shot_percentage: Mapped[float] = mapped_column(Float)
    shots_on_goal: Mapped[int] = mapped_column(Integer)
    sog_percentage: Mapped[float] = mapped_column(Float)
    yellow_cards: Mapped[int] = mapped_column(Integer)
    red_cards: Mapped[int] = mapped_column(Integer)
    penalty_kicks: Mapped[int] = mapped_column(Integer)
    game_winning_goals: Mapped[int] = mapped_column(Integer)

    # Goalie-specific stats
    goalie_games_started: Mapped[int] = mapped_column(Integer)
    goalie_goals_against: Mapped[int] = mapped_column(Integer)
    goalie_saves: Mapped[int] = mapped_column(Integer)
    goalie_save_percentage: Mapped[float] = mapped_column(Float)
    goalie_wins: Mapped[int] = mapped_column(Integer)
    goalie_losses: Mapped[int] = mapped_column(Integer)
    goalie_ties: Mapped[int] = mapped_column(Integer)
    goalie_shutouts: Mapped[int] = mapped_column(Integer)
    goalie_minutes_played: Mapped[float] = mapped_column(Float)

    __table_args__ = (
        # Team roster queries: get all players for a team in a specific league/season
        Index("ix_soccer_player_roster", "league", "season_option", "school"),
        # Leaderboard queries: rank players by stats with minimum games filter
        Index("ix_soccer_player_leaderboard", "league", "season_option", "games_played"),
        # Position-specific leaderboards (separate field/goalie rankings)
        Index("ix_soccer_player_position_leaderboard", "league", "season_option", "position", "games_played"),
    )
