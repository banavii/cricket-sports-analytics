from datetime import date

from sqlalchemy import (
    Boolean,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ============================================================
# BASE
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# TEAM
# ============================================================

class Team(Base):
    __tablename__ = "teams"

    team_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    team_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    team_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    season: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    coach_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Relationships
    players = relationship(
        "Player",
        back_populates="team",
    )

    matches = relationship(
        "Match",
        back_populates="team",
    )

    training_sessions = relationship(
        "TrainingSession",
        back_populates="team",
    )


# ============================================================
# PLAYER
# ============================================================

class Player(Base):
    __tablename__ = "players"

    player_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.team_id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_of_birth: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    gender: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    batting_style: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    bowling_style: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    joined_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="Active",
    )

    # Relationships
    team = relationship(
        "Team",
        back_populates="players",
    )

    batting_performances = relationship(
        "BattingPerformance",
        back_populates="player",
    )

    bowling_performances = relationship(
        "BowlingPerformance",
        back_populates="player",
    )

    training_records = relationship(
        "TrainingRecord",
        back_populates="player",
    )

    injuries = relationship(
        "Injury",
        back_populates="player",
    )

    equipment = relationship(
        "Equipment",
        back_populates="assigned_player",
    )


# ============================================================
# MATCH
# ============================================================

class Match(Base):
    __tablename__ = "matches"

    match_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.team_id"),
        nullable=False,
    )

    match_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    opponent: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    venue: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    competition: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    match_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    result: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    team_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    opponent_score: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Relationships
    team = relationship(
        "Team",
        back_populates="matches",
    )

    batting_performances = relationship(
        "BattingPerformance",
        back_populates="match",
    )

    bowling_performances = relationship(
        "BowlingPerformance",
        back_populates="match",
    )


# ============================================================
# BATTING PERFORMANCE
# ============================================================

class BattingPerformance(Base):
    __tablename__ = "batting_performances"

    performance_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.match_id"),
        nullable=False,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.player_id"),
        nullable=False,
    )

    runs: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    balls: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    fours: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    sixes: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    dismissal_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    not_out: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    # Relationships
    player = relationship(
        "Player",
        back_populates="batting_performances",
    )

    match = relationship(
        "Match",
        back_populates="batting_performances",
    )


# ============================================================
# BOWLING PERFORMANCE
# ============================================================

class BowlingPerformance(Base):
    __tablename__ = "bowling_performances"

    performance_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    match_id: Mapped[int] = mapped_column(
        ForeignKey("matches.match_id"),
        nullable=False,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.player_id"),
        nullable=False,
    )

    balls: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    runs_conceded: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    wickets: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    maidens: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    dot_balls: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Relationships
    player = relationship(
        "Player",
        back_populates="bowling_performances",
    )

    match = relationship(
        "Match",
        back_populates="bowling_performances",
    )


# ============================================================
# TRAINING SESSION
# ============================================================

class TrainingSession(Base):
    __tablename__ = "training_sessions"

    session_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.team_id"),
        nullable=False,
    )

    session_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    session_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    intensity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    coach_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    team = relationship(
        "Team",
        back_populates="training_sessions",
    )

    training_records = relationship(
        "TrainingRecord",
        back_populates="session",
    )


# ============================================================
# TRAINING RECORD
# ============================================================

class TrainingRecord(Base):
    __tablename__ = "training_records"

    record_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("training_sessions.session_id"),
        nullable=False,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.player_id"),
        nullable=False,
    )

    attendance: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    workload: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    fitness_rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    session = relationship(
        "TrainingSession",
        back_populates="training_records",
    )

    player = relationship(
        "Player",
        back_populates="training_records",
    )


# ============================================================
# INJURY
# ============================================================

class Injury(Base):
    __tablename__ = "injuries"

    injury_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.player_id"),
        nullable=False,
    )

    injury_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    body_part: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    injury_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    recovery_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    expected_return: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    actual_return: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    player = relationship(
        "Player",
        back_populates="injuries",
    )


# ============================================================
# EQUIPMENT
# ============================================================

class Equipment(Base):
    __tablename__ = "equipment"

    equipment_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.team_id"),
        nullable=False,
    )

    equipment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    brand: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    model: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    serial_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    assigned_player_id: Mapped[int | None] = mapped_column(
        ForeignKey("players.player_id"),
        nullable=True,
    )

    purchase_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    condition: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    last_maintenance: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    next_maintenance: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Relationships
    team = relationship(
        "Team",
    )

    assigned_player = relationship(
        "Player",
        back_populates="equipment",
    )