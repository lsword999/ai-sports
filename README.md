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

## Current scope

- Player management
- Physical metrics management
- GPS vest records for training and matches

## Data model

- Player
- `player_id`, `name`, `position`, `date_of_birth`
- `physical_metrics`

- PhysicalMetrics
- `height_cm`, `weight_kg`, `body_fat_pct`, `resting_heart_rate_bpm`

- GPSRecord
- `record_id`, `player_id`, `session_type` (`training`/`match`)
- `session_date`, `distance_m`, `max_speed_mps`, `duration_min`
- `sprint_count`, `avg_heart_rate_bpm`, `created_at`

## Project structure

- `src/ai_sports/`: core package
- `tests/`: unit tests
- `pyproject.toml`: package metadata
