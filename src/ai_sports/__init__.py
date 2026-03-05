"""ai-sports package."""

__all__ = ["analyze_match"]


def analyze_match(home_score: int, away_score: int) -> str:
    """Return a simple summary for a match result."""
    if home_score > away_score:
        return "home_win"
    if home_score < away_score:
        return "away_win"
    return "draw"
