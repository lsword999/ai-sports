from datetime import date

from ai_sports import GPSRecord, PhysicalMetrics, Player, PlayerManager


if __name__ == "__main__":
    manager = PlayerManager()

    player = Player(
        name="Demo Striker",
        position="FW",
        physical_metrics=PhysicalMetrics(height_cm=182, weight_kg=77, body_fat_pct=10.8),
    )
    manager.add_player(player)

    manager.add_gps_record(
        GPSRecord(
            player_id=player.player_id,
            session_type="training",
            session_date=date.today(),
            distance_m=8200,
            max_speed_mps=8.4,
            duration_min=86,
            sprint_count=18,
        )
    )

    print(f"Player: {player.name} ({player.position})")
    print(f"Training distance today: {manager.total_distance_m(player.player_id)} m")
