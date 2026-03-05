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

## Project structure

- `src/ai_sports/`: core package
- `tests/`: basic unit tests
- `pyproject.toml`: package metadata
