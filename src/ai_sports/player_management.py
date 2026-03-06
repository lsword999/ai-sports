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
class GPSRecord:
    """GPS vest record generated from training or match sessions."""

    player_id: str
    session_type: SessionType
    session_date: date
    distance_m: float
    max_speed_mps: float
    duration_min: float
    record_id: str = field(default_factory=lambda: str(uuid4()))
    sprint_count: int = 0
    avg_heart_rate_bpm: int | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)


class PlayerManager:
    """In-memory manager for player profiles and GPS data."""

    def __init__(self) -> None:
        self._players: dict[str, Player] = {}
        self._gps_records: dict[str, list[GPSRecord]] = {}

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

    def add_gps_record(self, record: GPSRecord) -> None:
        if record.player_id not in self._players:
            raise KeyError(f"Player not found: {record.player_id}")
        self._gps_records.setdefault(record.player_id, []).append(record)

    def list_gps_records(
        self, player_id: str, session_type: SessionType | None = None
    ) -> list[GPSRecord]:
        if player_id not in self._players:
            raise KeyError(f"Player not found: {player_id}")

        records = self._gps_records.get(player_id, [])
        if session_type is None:
            return list(records)
        return [record for record in records if record.session_type == session_type]

    def total_distance_m(
        self, player_id: str, session_type: SessionType | None = None
    ) -> float:
        records = self.list_gps_records(player_id, session_type=session_type)
        return sum(record.distance_m for record in records)
