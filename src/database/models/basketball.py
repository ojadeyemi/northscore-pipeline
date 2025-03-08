from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.db import Base
from src.utils.constants import (
    BASKETBALL_MEN_PLAYERS_CHAMPIONSHIP,
    BASKETBALL_MEN_PLAYERS_PLAYOFFS,
    BASKETBALL_MEN_PLAYERS_REG,
    BASKETBALL_MEN_TEAM_CHAMPIONSHIP,
    BASKETBALL_MEN_TEAM_PLAYOFFS,
    BASKETBALL_MEN_TEAM_REG,
    BASKETBALL_WOMEN_PLAYERS_CHAMPIONSHIP,
    BASKETBALL_WOMEN_PLAYERS_PLAYOFFS,
    BASKETBALL_WOMEN_PLAYERS_REG,
    BASKETBALL_WOMEN_TEAM_CHAMPIONSHIP,
    BASKETBALL_WOMEN_TEAM_PLAYOFFS,
    BASKETBALL_WOMEN_TEAM_REG,
)


class BaseTeam(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    conference: Mapped[str] = mapped_column(String(50))
    games_played: Mapped[int] = mapped_column(Integer)
    total_wins: Mapped[int] = mapped_column(Integer)
    total_losses: Mapped[int] = mapped_column(Integer)
    win_percentage: Mapped[float] = mapped_column(Float)
    offensive_efficiency: Mapped[float] = mapped_column(Float)
    defensive_efficiency: Mapped[float] = mapped_column(Float)
    net_efficiency: Mapped[float] = mapped_column(Float)
    net_efficiency_against: Mapped[float] = mapped_column(Float)
    points_per_game: Mapped[float] = mapped_column(Float)
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
    field_goal_made: Mapped[int] = mapped_column(Integer)
    field_goal_attempted: Mapped[int] = mapped_column(Integer)
    three_pointers_made: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted: Mapped[int] = mapped_column(Integer)
    free_throws_made: Mapped[int] = mapped_column(Integer)
    free_throws_attempted: Mapped[int] = mapped_column(Integer)
    field_goal_made_against: Mapped[int] = mapped_column(Integer)
    field_goal_attempted_against: Mapped[int] = mapped_column(Integer)
    three_pointers_made_against: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted_against: Mapped[int] = mapped_column(Integer)
    total_points: Mapped[int] = mapped_column(Integer)
    total_points_against: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"<Team(id={self.id}, team_name='{self.team_name}', conference='{self.conference}')>"


class BasePlayoffTeam(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    conference: Mapped[str] = mapped_column(String(50))
    games_played: Mapped[int] = mapped_column(Integer)
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
    field_goal_made: Mapped[int] = mapped_column(Integer)
    field_goal_attempted: Mapped[int] = mapped_column(Integer)
    three_pointers_made: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted: Mapped[int] = mapped_column(Integer)
    free_throws_made: Mapped[int] = mapped_column(Integer)
    free_throws_attempted: Mapped[int] = mapped_column(Integer)
    field_goal_made_against: Mapped[int] = mapped_column(Integer)
    field_goal_attempted_against: Mapped[int] = mapped_column(Integer)
    three_pointers_made_against: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted_against: Mapped[int] = mapped_column(Integer)
    total_points: Mapped[int] = mapped_column(Integer)
    total_points_against: Mapped[int] = mapped_column(Integer)

    def __repr__(self):
        return f"<ChampionshipTeam(id={self.id}, team_name='{self.team_name}', conference='{self.conference}')>"


class BasePlayer(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    lastname_initials: Mapped[str] = mapped_column(String(2))
    school: Mapped[str] = mapped_column(String(255))
    games_played: Mapped[int] = mapped_column(Integer)
    games_started: Mapped[int] = mapped_column(Integer)
    minutes_played: Mapped[int] = mapped_column(Integer)
    total_points: Mapped[int] = mapped_column(Integer)
    offensive_rebounds: Mapped[int] = mapped_column(Integer)
    defensive_rebounds: Mapped[int] = mapped_column(Integer)
    total_rebounds: Mapped[int] = mapped_column(Integer)
    personal_fouls: Mapped[int] = mapped_column(Integer)
    disqualifications: Mapped[int] = mapped_column(Integer)
    assists: Mapped[int] = mapped_column(Integer)
    turnovers: Mapped[int] = mapped_column(Integer)
    assist_to_turnover_ratio: Mapped[float] = mapped_column(Float)
    steals: Mapped[int] = mapped_column(Integer)
    blocks: Mapped[int] = mapped_column(Integer)
    field_goal_made: Mapped[int] = mapped_column(Integer)
    field_goal_attempted: Mapped[int] = mapped_column(Integer)
    field_goal_percentage: Mapped[float] = mapped_column(Float)
    three_pointers_made: Mapped[int] = mapped_column(Integer)
    three_pointers_attempted: Mapped[int] = mapped_column(Integer)
    three_pointers_percentage: Mapped[float] = mapped_column(Float)
    free_throws_made: Mapped[int] = mapped_column(Integer)
    free_throws_attempted: Mapped[int] = mapped_column(Integer)
    free_throws_percentage: Mapped[float] = mapped_column(Float)

    def __repr__(self):
        return (
            f"<Player(id={self.id}, first_name='{self.first_name}', "
            f"lastname_initials='{self.lastname_initials}', school='{self.school}')>"
        )


class MenTeam(BaseTeam):
    __tablename__ = BASKETBALL_MEN_TEAM_REG
    players: Mapped[list["MenPlayer"]] = relationship("MenPlayer", back_populates="team", cascade="all, delete-orphan")


class WomenTeam(BaseTeam):
    __tablename__ = BASKETBALL_WOMEN_TEAM_REG
    players: Mapped[list["WomenPlayer"]] = relationship(
        "WomenPlayer", back_populates="team", cascade="all, delete-orphan"
    )


class MenTeamPlayoffs(BasePlayoffTeam):
    __tablename__ = BASKETBALL_MEN_TEAM_PLAYOFFS
    players: Mapped[list["MenPlayerPlayoffs"]] = relationship(
        "MenPlayerPlayoffs", back_populates="team", cascade="all, delete-orphan"
    )


class WomenTeamPlayoffs(BasePlayoffTeam):
    __tablename__ = BASKETBALL_WOMEN_TEAM_PLAYOFFS
    players: Mapped[list["WomenPlayerPlayoffs"]] = relationship(
        "WomenPlayerPlayoffs", back_populates="team", cascade="all, delete-orphan"
    )


class MenChampionshipTeam(BasePlayoffTeam):
    __tablename__ = BASKETBALL_MEN_TEAM_CHAMPIONSHIP
    players: Mapped[list["MenChampionshipPlayer"]] = relationship(
        "MenChampionshipPlayer", back_populates="team", cascade="all, delete-orphan"
    )


class WomenChampionshipTeam(BasePlayoffTeam):
    __tablename__ = BASKETBALL_WOMEN_TEAM_CHAMPIONSHIP
    players: Mapped[list["WomenChampionshipPlayer"]] = relationship(
        "WomenChampionshipPlayer", back_populates="team", cascade="all, delete-orphan"
    )


class MenPlayer(BasePlayer):
    __tablename__ = BASKETBALL_MEN_PLAYERS_REG
    team_id = mapped_column(Integer, ForeignKey(f"{BASKETBALL_MEN_TEAM_REG}.id"))
    team: Mapped["MenTeam"] = relationship("MenTeam", back_populates="players")


class WomenPlayer(BasePlayer):
    __tablename__ = BASKETBALL_WOMEN_PLAYERS_REG
    team_id = mapped_column(Integer, ForeignKey(f"{BASKETBALL_WOMEN_TEAM_REG}.id"))
    team: Mapped["WomenTeam"] = relationship("WomenTeam", back_populates="players")


class MenPlayerPlayoffs(BasePlayer):
    __tablename__ = BASKETBALL_MEN_PLAYERS_PLAYOFFS
    team_id = mapped_column(Integer, ForeignKey(f"{BASKETBALL_MEN_TEAM_PLAYOFFS}.id"))
    team: Mapped["MenTeamPlayoffs"] = relationship("MenTeamPlayoffs", back_populates="players")
    regular_team_id = mapped_column(Integer, ForeignKey(f"{BASKETBALL_MEN_TEAM_REG}.id"))


class WomenPlayerPlayoffs(BasePlayer):
    __tablename__ = BASKETBALL_WOMEN_PLAYERS_PLAYOFFS
    team_id = mapped_column(Integer, ForeignKey(f"{BASKETBALL_WOMEN_TEAM_PLAYOFFS}.id"))
    team: Mapped["WomenTeamPlayoffs"] = relationship("WomenTeamPlayoffs", back_populates="players")
    regular_team_id = mapped_column(Integer, ForeignKey(f"{BASKETBALL_WOMEN_TEAM_REG}.id"))


class MenChampionshipPlayer(BasePlayer):
    __tablename__ = BASKETBALL_MEN_PLAYERS_CHAMPIONSHIP
    team_id = mapped_column(Integer, ForeignKey(f"{BASKETBALL_MEN_TEAM_CHAMPIONSHIP}.id"))
    team: Mapped["MenChampionshipTeam"] = relationship("MenChampionshipTeam", back_populates="players")


class WomenChampionshipPlayer(BasePlayer):
    __tablename__ = BASKETBALL_WOMEN_PLAYERS_CHAMPIONSHIP
    team_id = mapped_column(Integer, ForeignKey(f"{BASKETBALL_WOMEN_TEAM_CHAMPIONSHIP}.id"))
    team: Mapped["WomenChampionshipTeam"] = relationship("WomenChampionshipTeam", back_populates="players")
