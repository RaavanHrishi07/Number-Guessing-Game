
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

