import sys
import unittest
from pathlib import Path

# Allow running tests without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from ai_sports import analyze_match


class AnalyzeMatchTests(unittest.TestCase):
    def test_home_win(self) -> None:
        self.assertEqual(analyze_match(3, 1), "home_win")

    def test_away_win(self) -> None:
        self.assertEqual(analyze_match(0, 2), "away_win")

    def test_draw(self) -> None:
        self.assertEqual(analyze_match(1, 1), "draw")


if __name__ == "__main__":
    unittest.main()
