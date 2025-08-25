from sqlalchemy import Float, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import Base


class FootballStandings(Base):
    """Unified football standings - regular season only"""

    __tablename__ = "football_standings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, default="m", index=True)  # Football is men only
    conference: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)
    total_wins: Mapped[int] = mapped_column(Integer, nullable=False)
    total_losses: Mapped[int] = mapped_column(Integer, nullable=False)
    win_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    total_points: Mapped[int] = mapped_column(Integer, nullable=False)
    total_points_against: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("league", "team_name", name="uq_football_standings_team"),)


class FootballTeamStats(Base):
    """Unified football team stats - all seasons"""

    __tablename__ = "football_team_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, default="m", index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    conference: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)

    # Scoring stats
    touchdowns: Mapped[int] = mapped_column(Integer)
    field_goals: Mapped[int] = mapped_column(Integer)
    extra_points: Mapped[int] = mapped_column(Integer)
    two_point_conversions: Mapped[int] = mapped_column(Integer)
    defensive_extra_points: Mapped[int] = mapped_column(Integer)
    safeties: Mapped[int] = mapped_column(Integer)
    points: Mapped[int] = mapped_column(Integer)
    points_per_game: Mapped[float] = mapped_column(Float)

    # Offensive stats
    rushing_yards: Mapped[int] = mapped_column(Integer)
    passing_yards: Mapped[int] = mapped_column(Integer)
    total_offense: Mapped[int] = mapped_column(Integer)
    yards_per_game: Mapped[float] = mapped_column(Float)

    # Passing stats
    pass_completions: Mapped[int] = mapped_column(Integer)
    pass_attempts: Mapped[int] = mapped_column(Integer)
    pass_interceptions: Mapped[int] = mapped_column(Integer)
    passing_yards_per_game: Mapped[float] = mapped_column(Float)
    yards_per_attempt: Mapped[float] = mapped_column(Float)
    yards_per_completion: Mapped[float] = mapped_column(Float)
    passing_touchdowns: Mapped[int] = mapped_column(Integer)

    # Rushing stats
    rushing_attempts: Mapped[int] = mapped_column(Integer)
    rushing_yards_per_game: Mapped[float] = mapped_column(Float)
    rushing_average: Mapped[float] = mapped_column(Float)
    rushing_touchdowns: Mapped[int] = mapped_column(Integer)

    # First downs
    total_first_downs: Mapped[int] = mapped_column(Integer)
    rushing_first_downs: Mapped[int] = mapped_column(Integer)
    passing_first_downs: Mapped[int] = mapped_column(Integer)
    penalty_first_downs: Mapped[int] = mapped_column(Integer)
    first_downs_per_game: Mapped[float] = mapped_column(Float)

    # Conversions
    third_down_conversions_made: Mapped[int] = mapped_column(Integer)
    third_down_attempts: Mapped[int] = mapped_column(Integer)
    third_down_conversion_percentage: Mapped[float] = mapped_column(Float)
    fourth_down_conversions_made: Mapped[int] = mapped_column(Integer)
    fourth_down_attempts: Mapped[int] = mapped_column(Integer)
    fourth_down_conversion_percentage: Mapped[float] = mapped_column(Float)

    # Return stats
    kick_return_count: Mapped[int] = mapped_column(Integer)
    kick_return_yards: Mapped[int] = mapped_column(Integer)
    kickoff_return_average: Mapped[float] = mapped_column(Float)
    punt_return_count: Mapped[int] = mapped_column(Integer)
    punt_return_yards: Mapped[int] = mapped_column(Integer)
    punt_return_average: Mapped[float] = mapped_column(Float)

    # Kicking stats
    field_goal_made: Mapped[int] = mapped_column(Integer)
    field_goal_attempt: Mapped[int] = mapped_column(Integer)
    field_goal_percentage: Mapped[float] = mapped_column(Float)
    extra_point_made: Mapped[int] = mapped_column(Integer)
    extra_point_attempt: Mapped[int] = mapped_column(Integer)
    extra_point_percentage: Mapped[float] = mapped_column(Float)
    punt_count: Mapped[int] = mapped_column(Integer)
    punt_yards: Mapped[int] = mapped_column(Integer)
    punt_average: Mapped[float] = mapped_column(Float)
    kickoff_count: Mapped[int] = mapped_column(Integer)
    kickoff_yards: Mapped[int] = mapped_column(Integer)
    kickoff_average: Mapped[float] = mapped_column(Float)

    # Red zone efficiency
    scores_made: Mapped[int] = mapped_column(Integer)
    scores_attempt: Mapped[int] = mapped_column(Integer)
    red_zone_percentage: Mapped[float] = mapped_column(Float)
    touchdowns_made: Mapped[int] = mapped_column(Integer)
    touchdowns_attempt: Mapped[int] = mapped_column(Integer)
    touchdown_percentage: Mapped[float] = mapped_column(Float)

    # Turnovers and defense
    fumbles: Mapped[int] = mapped_column(Integer)
    fumbles_lost: Mapped[int] = mapped_column(Integer)
    fumble_recoveries: Mapped[int] = mapped_column(Integer)
    interceptions: Mapped[int] = mapped_column(Integer)
    interception_yards: Mapped[int] = mapped_column(Integer)
    interception_average: Mapped[float] = mapped_column(Float)
    interception_touchdowns: Mapped[int] = mapped_column(Integer)
    tackles: Mapped[float] = mapped_column(Float)
    sacks: Mapped[int] = mapped_column(Integer)

    # Penalties
    penalties: Mapped[int] = mapped_column(Integer)
    penalties_per_game: Mapped[float] = mapped_column(Float)
    penalty_yards: Mapped[int] = mapped_column(Integer)
    penalty_yards_per_game: Mapped[float] = mapped_column(Float)
    tackles_per_game: Mapped[float] = mapped_column(Float)

    # Time and attendance
    time_of_possession: Mapped[int] = mapped_column(Integer)
    home_attendance: Mapped[int] = mapped_column(Integer)
    average_home_attendance: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        UniqueConstraint("league", "season_option", "team_name", name="uq_football_team_league_season_team"),
    )


class FootballPlayerStats(Base):
    """Unified football player stats - all seasons"""

    __tablename__ = "football_player_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    lastname_initials: Mapped[str] = mapped_column(String(10), nullable=False)
    school: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    league: Mapped[str] = mapped_column(String(1), nullable=False, default="m", index=True)
    season_option: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # Basic stats
    games_played: Mapped[int] = mapped_column(Integer, nullable=False)

    # Passing stats
    pass_completions: Mapped[int] = mapped_column(Integer)
    pass_attempts: Mapped[int] = mapped_column(Integer)
    completion_percentage: Mapped[float] = mapped_column(Float)
    passing_yards: Mapped[int] = mapped_column(Integer)
    passing_yards_per_game: Mapped[float] = mapped_column(Float)
    yards_per_attempt: Mapped[float] = mapped_column(Float)
    passing_touchdowns: Mapped[int] = mapped_column(Integer)
    interceptions: Mapped[int] = mapped_column(Integer)
    longest_pass: Mapped[int] = mapped_column(Integer)
    passing_efficiency: Mapped[float] = mapped_column(Float)

    # Rushing stats
    rushing_attempts: Mapped[int] = mapped_column(Integer)
    rushing_yards: Mapped[int] = mapped_column(Integer)
    rushing_yards_per_game: Mapped[float] = mapped_column(Float)
    yards_per_carry: Mapped[float] = mapped_column(Float)
    rushing_touchdowns: Mapped[int] = mapped_column(Integer)
    longest_rush: Mapped[int] = mapped_column(Integer)
    fumbles: Mapped[int] = mapped_column(Integer)
    fumbles_lost: Mapped[int] = mapped_column(Integer)

    # Receiving stats
    receptions: Mapped[int] = mapped_column(Integer)
    receptions_per_game: Mapped[float] = mapped_column(Float)
    receiving_yards: Mapped[int] = mapped_column(Integer)
    receiving_yards_per_game: Mapped[float] = mapped_column(Float)
    yards_per_reception: Mapped[float] = mapped_column(Float)
    receiving_touchdowns: Mapped[int] = mapped_column(Integer)
    longest_reception: Mapped[int] = mapped_column(Integer)

    # Kicking stats
    field_goals_made: Mapped[int] = mapped_column(Integer)
    field_goals_attempted: Mapped[int] = mapped_column(Integer)
    field_goal_percentage: Mapped[float] = mapped_column(Float)
    longest_field_goal: Mapped[int] = mapped_column(Integer)
    extra_points_made: Mapped[int] = mapped_column(Integer)
    extra_points_attempted: Mapped[int] = mapped_column(Integer)
    extra_point_percentage: Mapped[float] = mapped_column(Float)
    kicking_points: Mapped[int] = mapped_column(Integer)

    # Punting stats
    punts: Mapped[int] = mapped_column(Integer)
    punting_yards: Mapped[int] = mapped_column(Integer)
    yards_per_punt: Mapped[float] = mapped_column(Float)
    longest_punt: Mapped[int] = mapped_column(Integer)
    punts_inside_20: Mapped[int] = mapped_column(Integer)
    fair_catches: Mapped[int] = mapped_column(Integer)
    touchbacks: Mapped[int] = mapped_column(Integer)
    blocked_punts: Mapped[int] = mapped_column(Integer)

    # Return stats
    kick_returns: Mapped[int] = mapped_column(Integer)
    kick_return_yards: Mapped[int] = mapped_column(Integer)
    yards_per_kick_return: Mapped[float] = mapped_column(Float)
    kick_return_touchdowns: Mapped[int] = mapped_column(Integer)
    longest_kick_return: Mapped[int] = mapped_column(Integer)
    punt_returns: Mapped[int] = mapped_column(Integer)
    punt_return_yards: Mapped[int] = mapped_column(Integer)
    yards_per_punt_return: Mapped[float] = mapped_column(Float)
    punt_return_touchdowns: Mapped[int] = mapped_column(Integer)
    longest_punt_return: Mapped[int] = mapped_column(Integer)

    # All-Purpose yards stats
    punt_return_yards: Mapped[int] = mapped_column(Integer)
    kick_return_yards: Mapped[int] = mapped_column(Integer)
    total_yards: Mapped[int] = mapped_column(Integer)
    yards_per_game: Mapped[float] = mapped_column(Float)

    # Scoring stats
    total_points: Mapped[int] = mapped_column(Integer)
    points_per_game: Mapped[float] = mapped_column(Float)
    interception_return_touchdowns: Mapped[int] = mapped_column(Integer)
    fumble_return_touchdowns: Mapped[int] = mapped_column(Integer)
    two_point_conversions: Mapped[int] = mapped_column(Integer)
    miscellaneous_touchdowns: Mapped[int] = mapped_column(Integer)

    # Defensive stats
    solo_tackles: Mapped[int] = mapped_column(Integer)
    assisted_tackles: Mapped[int] = mapped_column(Integer)
    total_tackles: Mapped[float] = mapped_column(Float)
    tackles_per_game: Mapped[float] = mapped_column(Float)
    sacks: Mapped[float] = mapped_column(Float)
    sack_yards: Mapped[int] = mapped_column(Integer)
    tackles_for_loss: Mapped[float] = mapped_column(Float)
    tackles_for_loss_yards: Mapped[int] = mapped_column(Integer)
    forced_fumbles: Mapped[int] = mapped_column(Integer)
    fumble_recoveries: Mapped[int] = mapped_column(Integer)
    fumble_recovery_yards: Mapped[int] = mapped_column(Integer)
    interception_return_yards: Mapped[int] = mapped_column(Integer)
    pass_breakups: Mapped[int] = mapped_column(Integer)
    blocked_kicks: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        # Team roster queries: get all players for a team in a specific league/season
        Index("ix_football_player_roster", "league", "season_option", "school"),
        # Leaderboard queries: rank players by stats with minimum games filter
        Index("ix_football_player_leaderboard", "league", "season_option", "games_played"),
    )
