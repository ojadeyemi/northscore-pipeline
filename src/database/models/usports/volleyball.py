from sqlalchemy import Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class VolleyballStandings(Base):
    """Unified volleyball standings - regular season only"""

    __tablename__ = "volleyball_standings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    conference: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)
    total_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_losses: Mapped[int] = mapped_column(Integer, nullable=False)
    win_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    sets_for: Mapped[int] = mapped_column(Integer, nullable=False)
    sets_against: Mapped[int] = mapped_column(Integer, nullable=False)
    points: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("league", "team_name", name="uq_volleyball_standings_team"),)


class VolleyballTeamStats(Base):
    """Unified volleyball team stats - all seasons"""

    __tablename__ = "volleyball_team_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    conference: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    matches_played: Mapped[int] = mapped_column(Integer, nullable=False)
    sets_played: Mapped[int] = mapped_column(Integer, nullable=False)

    # Offensive stats
    kills: Mapped[int] = mapped_column(Integer)
    kills_per_set: Mapped[float] = mapped_column(Float)
    errors: Mapped[int] = mapped_column(Integer)
    total_attacks: Mapped[int] = mapped_column(Integer)
    hitting_percentage: Mapped[float] = mapped_column(Float)
    assists: Mapped[int] = mapped_column(Integer)
    assists_per_set: Mapped[float] = mapped_column(Float)
    points: Mapped[float] = mapped_column(Float)
    points_per_set: Mapped[float] = mapped_column(Float)

    # Defensive stats
    digs: Mapped[int] = mapped_column(Integer)
    digs_per_set: Mapped[float] = mapped_column(Float)
    block_solos: Mapped[int] = mapped_column(Integer)
    block_assists: Mapped[int] = mapped_column(Integer)
    total_blocks: Mapped[float] = mapped_column(Float)
    blocks_per_set: Mapped[float] = mapped_column(Float)

    # Serve/Receive stats
    service_aces: Mapped[int] = mapped_column(Integer)
    service_aces_per_set: Mapped[float] = mapped_column(Float)
    service_errors: Mapped[int] = mapped_column(Integer)
    receptions: Mapped[int] = mapped_column(Integer)
    reception_errors: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("league", "season_option", "team_name", name="uq_volleyball_team_league_season_team"),
    )


class VolleyballPlayerStats(Base):
    """Unified volleyball player stats - all seasons"""

    __tablename__ = "volleyball_player_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    lastname_initials: Mapped[str] = mapped_column(String(10), nullable=False)
    school: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # Basic stats
    matches_played: Mapped[int] = mapped_column(Integer, nullable=False)
    sets_played: Mapped[int] = mapped_column(Integer, nullable=False)

    # Offensive stats
    kills: Mapped[int] = mapped_column(Integer)
    kills_per_set: Mapped[float] = mapped_column(Float)
    errors: Mapped[int] = mapped_column(Integer)
    total_attacks: Mapped[int] = mapped_column(Integer)
    total_attacks_per_set: Mapped[float] = mapped_column(Float)
    hitting_percentage: Mapped[float] = mapped_column(Float)
    assists: Mapped[int] = mapped_column(Integer)
    assists_per_set: Mapped[float] = mapped_column(Float)
    points: Mapped[float] = mapped_column(Float)
    points_per_set: Mapped[float] = mapped_column(Float)

    # Defensive stats
    digs: Mapped[int] = mapped_column(Integer)
    digs_per_set: Mapped[float] = mapped_column(Float)
    block_solos: Mapped[int] = mapped_column(Integer)
    block_assists: Mapped[int] = mapped_column(Integer)
    total_blocks: Mapped[float] = mapped_column(Float)
    blocks_per_set: Mapped[float] = mapped_column(Float)

    # Serve/Receive stats
    serve_attempts: Mapped[int] = mapped_column(Integer)
    service_aces: Mapped[int] = mapped_column(Integer)
    service_aces_per_set: Mapped[float] = mapped_column(Float)
    service_errors: Mapped[int] = mapped_column(Integer)
    receptions: Mapped[int] = mapped_column(Integer)
    reception_errors: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        # Team roster queries: get all players for a team in a specific league/season
        Index("ix_volleyball_player_roster", "league", "season_option", "school"),
        # Leaderboard queries: rank players by stats with minimum matches/sets filter
        Index("ix_volleyball_player_leaderboard", "league", "season_option", "matches_played"),
        # Sets-based leaderboard for per-set stats
        Index("ix_volleyball_player_sets_leaderboard", "league", "season_option", "sets_played"),
    )
