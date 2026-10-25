
import json
import random

import main


def test_difficulty_settings():
    """Verify that all difficulty levels have the correct maximum."""
    game = main.NumberGuessingGame.__new__(main.NumberGuessingGame)

    game.difficulties = {
        "Easy (1-50)": 50,
        "Medium (1-100)": 100,
        "Hard (1-500)": 500,
    }

    assert game.difficulties["Easy (1-50)"] == 50
    assert game.difficulties["Medium (1-100)"] == 100
    assert game.difficulties["Hard (1-500)"] == 500


def test_random_number_is_within_range():
    """Verify random numbers stay within the selected range."""
    for maximum in (50, 100, 500):
        number = random.randint(1, maximum)
        assert 1 <= number <= maximum


def test_guess_is_too_low():
    assert main.evaluate_guess(20, 50, 100) == "low"


def test_guess_is_too_high():
    assert main.evaluate_guess(80, 50, 100) == "high"


def test_guess_is_correct():
    assert main.evaluate_guess(50, 50, 100) == "correct"


def test_guess_outside_range_is_invalid():
    assert main.evaluate_guess(0, 50, 100) == "invalid"
    assert main.evaluate_guess(101, 50, 100) == "invalid"


def test_load_best_scores_when_file_does_not_exist(tmp_path, monkeypatch):
    """A missing score file should return an empty dictionary."""
    score_file = tmp_path / "scores.json"
    monkeypatch.setattr(main, "SCORE_FILE", score_file)

    assert main.load_best_scores() == {}


def test_save_and_load_best_scores(tmp_path, monkeypatch):
    """Best scores should survive saving and loading."""
    score_file = tmp_path / "scores.json"
    monkeypatch.setattr(main, "SCORE_FILE", score_file)

    scores = {
        "Easy (1-50)": 3,
        "Medium (1-100)": 5,
    }

    assert main.save_best_scores(scores) is True
    assert main.load_best_scores() == scores


def test_load_best_scores_ignores_invalid_entries(tmp_path, monkeypatch):
    """Invalid score entries should not be loaded."""
    score_file = tmp_path / "scores.json"
    monkeypatch.setattr(main, "SCORE_FILE", score_file)

    score_file.write_text(
        json.dumps({
            "Easy (1-50)": 3,
            "Medium (1-100)": -2,
            "Hard (1-500)": "five",
            "Unknown": True,
        }),
        encoding="utf-8",
    )

    assert main.load_best_scores() == {
        "Easy (1-50)": 3,
    }


def test_save_best_scores_handles_write_error(tmp_path, monkeypatch):
    """A file write error should not crash the game."""
    score_file = tmp_path / "missing_folder" / "scores.json"
    monkeypatch.setattr(main, "SCORE_FILE", score_file)

    assert main.save_best_scores({"Easy (1-50)": 2}) is False
