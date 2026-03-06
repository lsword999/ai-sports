import sys
import unittest
from datetime import date
from pathlib import Path

# Allow running tests without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_sports import GPSRecord, PhysicalMetrics, Player, PlayerManager, Session


class PlayerManagerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = PlayerManager()
        self.player = Player(
            player_id="p001",
            name="Lionel Messi",
            position="FW",
            physical_metrics=PhysicalMetrics(
                height_cm=170,
                weight_kg=72,
                body_fat_pct=10.1,
                resting_heart_rate_bpm=52,
            ),
        )
        self.manager.add_player(self.player)

        self.training_session = Session(
            session_id="s_training_001",
            session_type="training",
            session_date=date(2026, 3, 6),
            title="Conditioning",
            location="Main Field",
        )
        self.match_session = Session(
            session_id="s_match_001",
            session_type="match",
            session_date=date(2026, 3, 7),
            title="League Matchday 1",
            opponent="FC Demo",
            location="Stadium A",
        )
        self.manager.add_session(self.training_session)
        self.manager.add_session(self.match_session)

    def test_add_and_get_player(self) -> None:
        got = self.manager.get_player("p001")
        self.assertEqual(got.name, "Lionel Messi")

    def test_update_physical_metrics(self) -> None:
        new_metrics = PhysicalMetrics(height_cm=170, weight_kg=73.5, body_fat_pct=10.4)
        self.manager.update_physical_metrics("p001", new_metrics)

        self.assertEqual(self.manager.get_player("p001").physical_metrics.weight_kg, 73.5)

    def test_add_and_filter_sessions(self) -> None:
        all_sessions = self.manager.list_sessions()
        match_sessions = self.manager.list_sessions(session_type="match")

        self.assertEqual(len(all_sessions), 2)
        self.assertEqual(len(match_sessions), 1)
        self.assertEqual(match_sessions[0].session_id, "s_match_001")

    def test_add_gps_record_and_aggregate_distance(self) -> None:
        self.manager.add_gps_record(
            GPSRecord(
                record_id="g1",
                player_id="p001",
                session_id="s_training_001",
                session_type="training",
                session_date=date(2026, 3, 6),
                distance_m=7800,
                max_speed_mps=8.1,
                duration_min=90,
            )
        )
        self.manager.add_gps_record(
            GPSRecord(
                record_id="g2",
                player_id="p001",
                session_id="s_match_001",
                session_type="match",
                session_date=date(2026, 3, 7),
                distance_m=10300,
                max_speed_mps=8.9,
                duration_min=95,
            )
        )

        self.assertEqual(self.manager.total_distance_m("p001"), 18100)
        self.assertEqual(self.manager.total_distance_m("p001", session_type="match"), 10300)
        self.assertEqual(self.manager.total_distance_m("p001", session_id="s_training_001"), 7800)

    def test_unknown_player_for_gps_should_fail(self) -> None:
        with self.assertRaises(KeyError):
            self.manager.add_gps_record(
                GPSRecord(
                    player_id="unknown",
                    session_id="s_training_001",
                    session_type="training",
                    session_date=date(2026, 3, 8),
                    distance_m=1000,
                    max_speed_mps=5.5,
                    duration_min=20,
                )
            )

    def test_unknown_session_for_gps_should_fail(self) -> None:
        with self.assertRaises(KeyError):
            self.manager.add_gps_record(
                GPSRecord(
                    player_id="p001",
                    session_id="missing_session",
                    session_type="training",
                    session_date=date(2026, 3, 6),
                    distance_m=1000,
                    max_speed_mps=5.5,
                    duration_min=20,
                )
            )

    def test_mismatched_session_type_should_fail(self) -> None:
        with self.assertRaises(ValueError):
            self.manager.add_gps_record(
                GPSRecord(
                    player_id="p001",
                    session_id="s_training_001",
                    session_type="match",
                    session_date=date(2026, 3, 6),
                    distance_m=1000,
                    max_speed_mps=5.5,
                    duration_min=20,
                )
            )


if __name__ == "__main__":
    unittest.main()
