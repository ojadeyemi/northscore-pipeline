from sqlalchemy import Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class IceHockeyStandings(Base):
    """Unified ice hockey standings - regular season only"""

    __tablename__ = "ice_hockey_standings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    conference: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)
    total_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_losses: Mapped[int] = mapped_column(Integer, nullable=False)
    goals_for: Mapped[int] = mapped_column(Integer, nullable=False)
    goals_against: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("league", "team_name", name="uq_hockey_standings_team"),)


class IceHockeyTeamStats(Base):
    """Unified ice hockey team stats - all seasons"""

    __tablename__ = "ice_hockey_team_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    conference: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)

    # Offensive stats
    goals: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    goals_per_game: Mapped[float] = mapped_column(Float)
    shots: Mapped[int] = mapped_column(Integer)
    penalty_minutes: Mapped[int] = mapped_column(Integer)

    # Power play stats
    power_play_goals: Mapped[int] = mapped_column(Integer)
    power_play_opportunities: Mapped[int] = mapped_column(Integer)
    power_play_percentage: Mapped[float] = mapped_column(Float)
    power_play_goals_against: Mapped[int] = mapped_column(Integer)

    # Penalty kill stats
    times_short_handed: Mapped[int] = mapped_column(Integer)
    penalty_kill_percentage: Mapped[float] = mapped_column(Float)
    short_handed_goals: Mapped[int] = mapped_column(Integer)
    short_handed_goals_against: Mapped[int] = mapped_column(Integer)

    # Goaltending stats
    goals_against: Mapped[int] = mapped_column(Integer)
    goals_against_average: Mapped[float] = mapped_column(Float)
    saves: Mapped[int] = mapped_column(Integer)
    save_percentage: Mapped[float] = mapped_column(Float)
    empty_net_goals_against: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("league", "season_option", "team_name", name="uq_hockey_team_league_season_team"),
    )


class IceHockeyPlayerStats(Base):
    """Unified ice hockey player stats - all seasons"""

    __tablename__ = "ice_hockey_player_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    lastname_initials: Mapped[str] = mapped_column(String(10), nullable=False)
    school: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(10), index=True)  # 'skater' or 'goalie'

    # Basic stats
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)

    # Skater stats
    goals: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    points: Mapped[int] = mapped_column(Integer)
    penalty_minutes: Mapped[int] = mapped_column(Integer)
    plus_minus: Mapped[int] = mapped_column(Integer)
    power_play_goals: Mapped[int] = mapped_column(Integer)
    short_handed_goals: Mapped[int] = mapped_column(Integer)
    empty_net_goals: Mapped[int] = mapped_column(Integer)
    game_winning_goals: Mapped[int] = mapped_column(Integer)
    game_tying_goals: Mapped[int] = mapped_column(Integer)
    hat_tricks: Mapped[int] = mapped_column(Integer)
    shots_on_goal: Mapped[int] = mapped_column(Integer)

    # Goalie-specific stats
    goalie_games_played: Mapped[int] = mapped_column(Integer)
    goalie_games_started: Mapped[int] = mapped_column(Integer)
    goalie_minutes_played: Mapped[float] = mapped_column(Float)
    goalie_goals_against: Mapped[int] = mapped_column(Integer)
    goalie_goals_against_average: Mapped[float] = mapped_column(Float)
    goalie_saves: Mapped[int] = mapped_column(Integer)
    goalie_save_percentage: Mapped[float] = mapped_column(Float)
    goalie_wins: Mapped[int] = mapped_column(Integer)
    goalie_losses: Mapped[int] = mapped_column(Integer)
    goalie_ties: Mapped[int] = mapped_column(Integer)
    goalie_win_percentage: Mapped[float] = mapped_column(Float)

    __table_args__ = (
        # Team roster queries: get all players for a team in a specific league/season
        Index("ix_hockey_player_roster", "league", "season_option", "school"),
        # Leaderboard queries: rank players by stats with minimum games filter
        Index("ix_hockey_player_leaderboard", "league", "season_option", "games_played"),
        # Role-specific leaderboards (separate skater/goalie rankings)
        Index("ix_hockey_player_role_leaderboard", "league", "season_option", "role", "games_played"),
    )
