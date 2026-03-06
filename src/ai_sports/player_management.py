from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Literal
from uuid import uuid4

SessionType = Literal["training", "match"]


@dataclass
class PhysicalMetrics:
    """Basic body metrics for a football player."""

    height_cm: float
    weight_kg: float
    body_fat_pct: float | None = None
    resting_heart_rate_bpm: int | None = None


@dataclass
class Player:
    """Core profile for a football player."""

    name: str
    position: str
    physical_metrics: PhysicalMetrics
    player_id: str = field(default_factory=lambda: str(uuid4()))
    date_of_birth: date | None = None


@dataclass
class Session:
    """A scheduled football activity session (training or match)."""

    session_type: SessionType
    session_date: date
    title: str
    session_id: str = field(default_factory=lambda: str(uuid4()))
    location: str | None = None
    opponent: str | None = None
    notes: str | None = None


@dataclass
class GPSRecord:
    """GPS vest record generated from training or match sessions."""

    player_id: str
    session_type: SessionType
    session_date: date
    distance_m: float
    max_speed_mps: float
    duration_min: float
    record_id: str = field(default_factory=lambda: str(uuid4()))
    session_id: str | None = None
    sprint_count: int = 0
    avg_heart_rate_bpm: int | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)


class PlayerManager:
    """In-memory manager for player profiles, sessions, and GPS data."""

    def __init__(self) -> None:
        self._players: dict[str, Player] = {}
        self._gps_records: dict[str, list[GPSRecord]] = {}
        self._sessions: dict[str, Session] = {}

    def add_player(self, player: Player) -> None:
        if player.player_id in self._players:
            raise ValueError(f"Player id already exists: {player.player_id}")
        self._players[player.player_id] = player
        self._gps_records.setdefault(player.player_id, [])

    def get_player(self, player_id: str) -> Player:
        try:
            return self._players[player_id]
        except KeyError as err:
            raise KeyError(f"Player not found: {player_id}") from err

    def list_players(self) -> list[Player]:
        return list(self._players.values())

    def update_physical_metrics(self, player_id: str, metrics: PhysicalMetrics) -> None:
        player = self.get_player(player_id)
        player.physical_metrics = metrics

    def add_session(self, session: Session) -> None:
        if session.session_id in self._sessions:
            raise ValueError(f"Session id already exists: {session.session_id}")
        self._sessions[session.session_id] = session

    def get_session(self, session_id: str) -> Session:
        try:
            return self._sessions[session_id]
        except KeyError as err:
            raise KeyError(f"Session not found: {session_id}") from err

    def list_sessions(self, session_type: SessionType | None = None) -> list[Session]:
        sessions = list(self._sessions.values())
        if session_type is None:
            return sessions
        return [session for session in sessions if session.session_type == session_type]

    def add_gps_record(self, record: GPSRecord) -> None:
        if record.player_id not in self._players:
            raise KeyError(f"Player not found: {record.player_id}")

        if record.session_id is not None:
            session = self.get_session(record.session_id)
            if session.session_type != record.session_type:
                raise ValueError("GPS record session_type does not match linked session")
            if session.session_date != record.session_date:
                raise ValueError("GPS record session_date does not match linked session")

        self._gps_records.setdefault(record.player_id, []).append(record)

    def list_gps_records(
        self,
        player_id: str,
        session_type: SessionType | None = None,
        session_id: str | None = None,
    ) -> list[GPSRecord]:
        if player_id not in self._players:
            raise KeyError(f"Player not found: {player_id}")

        records = self._gps_records.get(player_id, [])
        filtered = list(records)
        if session_type is not None:
            filtered = [record for record in filtered if record.session_type == session_type]
        if session_id is not None:
            filtered = [record for record in filtered if record.session_id == session_id]
        return filtered

    def total_distance_m(
        self,
        player_id: str,
        session_type: SessionType | None = None,
        session_id: str | None = None,
    ) -> float:
        records = self.list_gps_records(
            player_id,
            session_type=session_type,
            session_id=session_id,
        )
        return sum(record.distance_m for record in records)
