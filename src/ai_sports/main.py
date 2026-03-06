from datetime import date

from ai_sports import GPSRecord, PhysicalMetrics, Player, PlayerManager, Session


if __name__ == "__main__":
    manager = PlayerManager()

    player = Player(
        name="Demo Striker",
        position="FW",
        physical_metrics=PhysicalMetrics(height_cm=182, weight_kg=77, body_fat_pct=10.8),
    )
    manager.add_player(player)

    training_session = Session(
        session_id="s-training-001",
        session_type="training",
        session_date=date.today(),
        title="Morning Conditioning",
        location="Field A",
    )
    manager.add_session(training_session)

    manager.add_gps_record(
        GPSRecord(
            player_id=player.player_id,
            session_id=training_session.session_id,
            session_type="training",
            session_date=training_session.session_date,
            distance_m=8200,
            max_speed_mps=8.4,
            duration_min=86,
            sprint_count=18,
        )
    )

    print(f"Player: {player.name} ({player.position})")
    print(
        "Training distance for session"
        f" {training_session.title}: {manager.total_distance_m(player.player_id, session_id=training_session.session_id)} m"
    )
