from sqlalchemy import Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class BasketballStandings(Base):
    """Unified basketball standings - regular season only"""

    __tablename__ = "basketball_standings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    conference: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)
    total_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_losses: Mapped[int] = mapped_column(Integer, nullable=False)
    win_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    total_points: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points_against: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("league", "team_name", name="uq_basketball_standings_team"),)


class BasketballTeamStats(Base):
    """Unified basketball team stats - all seasons"""

    __tablename__ = "basketball_team_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    conference: Mapped[str] = mapped_column(String(50), index=True)
    games_played: Mapped[int] = mapped_column(Integer)

    # Performance stats
    points_per_game: Mapped[float] = mapped_column(Float)
    offensive_efficiency: Mapped[float] = mapped_column(Float)
    defensive_efficiency: Mapped[float] = mapped_column(Float)
    net_efficiency: Mapped[float] = mapped_column(Float)
    net_efficiency_against: Mapped[float] = mapped_column(Float)
    field_goal_percentage: Mapped[float] = mapped_column(Float)
    three_point_percentage: Mapped[float] = mapped_column(Float)
    free_throw_percentage: Mapped[float] = mapped_column(Float)
    offensive_rebounds_per_game: Mapped[float] = mapped_column(Float)
    defensive_rebounds_per_game: Mapped[float] = mapped_column(Float)
    total_rebounds_per_game: Mapped[float] = mapped_column(Float)
    rebound_margin: Mapped[float] = mapped_column(Float)
    assists_per_game: Mapped[float] = mapped_column(Float)
    turnovers_per_game: Mapped[float] = mapped_column(Float)
    steals_per_game: Mapped[float] = mapped_column(Float)
    blocks_per_game: Mapped[float] = mapped_column(Float)
    team_fouls_per_game: Mapped[float] = mapped_column(Float)

    # Against stats
    field_goal_percentage_against: Mapped[float] = mapped_column(Float)
    three_point_percentage_against: Mapped[float] = mapped_column(Float)
    offensive_rebounds_per_game_against: Mapped[float] = mapped_column(Float)
    defensive_rebounds_per_game_against: Mapped[float] = mapped_column(Float)
    total_rebounds_per_game_against: Mapped[float] = mapped_column(Float)
    rebound_margin_against: Mapped[float] = mapped_column(Float)
    assists_per_game_against: Mapped[float] = mapped_column(Float)
    turnovers_per_game_against: Mapped[float] = mapped_column(Float)
    steals_per_game_against: Mapped[float] = mapped_column(Float)
    blocks_per_game_against: Mapped[float] = mapped_column(Float)
    team_fouls_per_game_against: Mapped[float] = mapped_column(Float)
    points_per_game_against: Mapped[float] = mapped_column(Float)

    # Shooting totals
    field_goal_made: Mapped[int] = mapped_column(Integer)
    field_goal_attempted: Mapped[int] = mapped_column(Integer)
    three_pointers_made: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted: Mapped[int] = mapped_column(Integer)
    free_throws_made: Mapped[int] = mapped_column(Integer)
    free_throws_attempted: Mapped[int] = mapped_column(Integer)

    # Shooting totals against
    field_goal_made_against: Mapped[int] = mapped_column(Integer)
    field_goal_attempted_against: Mapped[int] = mapped_column(Integer)
    three_pointers_made_against: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted_against: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("league", "season_option", "team_name", name="uq_basketball_team_league_season_team"),
    )


class BasketballPlayerStats(Base):
    """Unified basketball player stats - all seasons"""

    __tablename__ = "basketball_player_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    lastname_initials: Mapped[str] = mapped_column(String(10), nullable=False)
    school: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # Basic stats
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)
    games_started: Mapped[int] = mapped_column(Integer)
    minutes_played: Mapped[int] = mapped_column(Integer)
    total_points: Mapped[int] = mapped_column(Integer)

    # Shooting
    field_goal_made: Mapped[int] = mapped_column(Integer)
    field_goal_attempted: Mapped[int] = mapped_column(Integer)
    field_goal_percentage: Mapped[float] = mapped_column(Float)
    three_pointers_made: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted: Mapped[int] = mapped_column(Integer)
    three_pointers_percentage: Mapped[float] = mapped_column(Float)
    free_throws_made: Mapped[int] = mapped_column(Integer)
    free_throws_attempted: Mapped[int] = mapped_column(Integer)
    free_throws_percentage: Mapped[float] = mapped_column(Float)

    # Other stats
    offensive_rebounds: Mapped[int] = mapped_column(Integer)
    defensive_rebounds: Mapped[int] = mapped_column(Integer)
    total_rebounds: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    turnovers: Mapped[int] = mapped_column(Integer)
    assist_to_turnover_ratio: Mapped[float] = mapped_column(Float)
    steals: Mapped[int] = mapped_column(Integer)
    blocks: Mapped[int] = mapped_column(Integer)
    personal_fouls: Mapped[int] = mapped_column(Integer)
    disqualifications: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        # Team roster queries: get all players for a team in a specific league/season
        Index("ix_basketball_player_roster", "league", "season_option", "school"),
        # Leaderboard queries: rank players by stats with minimum games filter
        Index("ix_basketball_player_leaderboard", "league", "season_option", "games_played"),
    )
