# ai-sports

Python starter project for AI + sports experiments.

## Quick start

```bash
cd /Users/jeffliu/Documents/ai-sports
python3 -m venv .venv
source .venv/bin/activate
PYTHONPATH=src python3 -m ai_sports.main
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Web frontend

```bash
cd /Users/jeffliu/Documents/ai-sports/web
python3 -m http.server 8080
```

Open: http://localhost:8080

## Current scope

- Player management
- Physical metrics management
- Session management (training and matches)
- GPS vest records linked to session

## Data model

- Player
- `player_id`, `name`, `position`, `date_of_birth`
- `physical_metrics`

- PhysicalMetrics
- `height_cm`, `weight_kg`, `body_fat_pct`, `resting_heart_rate_bpm`

- Session
- `session_id`, `session_type` (`training`/`match`), `session_date`, `title`
- optional: `location`, `opponent`, `notes`

- GPSRecord
- `record_id`, `player_id`, `session_id`
- `session_type` (`training`/`match`), `session_date`
- `distance_m`, `max_speed_mps`, `duration_min`
- `sprint_count`, `avg_heart_rate_bpm`, `created_at`

## Project structure

- `src/ai_sports/`: core package
- `tests/`: unit tests
- `pyproject.toml`: package metadata
