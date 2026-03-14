import sys
from pathlib import Path

# Add parent directory to path so we can import logic_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"


# ============================================================================
# Unit Tests for check_guess function
# ============================================================================


class TestCheckGuessWinCondition:
    """Test check_guess when the guess matches the secret."""

    def test_check_guess_exact_match(self):
        """Test when guess exactly matches the secret."""
        outcome, message = check_guess(50, 50)
        assert outcome == "Win"
        assert message == "🎉 Correct!"

    def test_check_guess_match_zero(self):
        """Test when both guess and secret are zero."""
        outcome, message = check_guess(0, 0)
        assert outcome == "Win"
        assert message == "🎉 Correct!"

    def test_check_guess_match_negative(self):
        """Test when guess and secret are negative numbers."""
        outcome, message = check_guess(-25, -25)
        assert outcome == "Win"
        assert message == "🎉 Correct!"

    def test_check_guess_match_large_number(self):
        """Test when both numbers are large."""
        outcome, message = check_guess(9999, 9999)
        assert outcome == "Win"
        assert message == "🎉 Correct!"


class TestCheckGuessTooHigh:
    """Test check_guess when the guess is higher than the secret."""

    def test_check_guess_too_high_single_digit(self):
        """Test guess too high with single digits."""
        outcome, message = check_guess(7, 3)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"

    def test_check_guess_too_high_multi_digit(self):
        """Test guess too high with multi-digit numbers."""
        outcome, message = check_guess(100, 50)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"

    def test_check_guess_too_high_just_above(self):
        """Test guess just one above the secret."""
        outcome, message = check_guess(51, 50)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"

    def test_check_guess_too_high_much_higher(self):
        """Test guess much higher than secret."""
        outcome, message = check_guess(500, 50)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"

    def test_check_guess_too_high_with_negatives(self):
        """Test when guess is higher but both are negative."""
        outcome, message = check_guess(-10, -50)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"


class TestCheckGuessTooLow:
    """Test check_guess when the guess is lower than the secret."""

    def test_check_guess_too_low_single_digit(self):
        """Test guess too low with single digits."""
        outcome, message = check_guess(3, 7)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"

    def test_check_guess_too_low_multi_digit(self):
        """Test guess too low with multi-digit numbers."""
        outcome, message = check_guess(25, 100)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"

    def test_check_guess_too_low_just_below(self):
        """Test guess just one below the secret."""
        outcome, message = check_guess(49, 50)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"

    def test_check_guess_too_low_much_lower(self):
        """Test guess much lower than secret."""
        outcome, message = check_guess(1, 500)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"

    def test_check_guess_too_low_with_negatives(self):
        """Test when guess is lower with negative numbers."""
        outcome, message = check_guess(-100, -50)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"


class TestCheckGuessEdgeCases:
    """Test check_guess with edge cases and boundary conditions."""

    def test_check_guess_with_zero_secret(self):
        """Test when secret is zero."""
        outcome, message = check_guess(5, 0)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"

    def test_check_guess_zero_against_positive(self):
        """Test when guess is zero and secret is positive."""
        outcome, message = check_guess(0, 50)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"

    def test_check_guess_negative_vs_positive(self):
        """Test when guess is negative and secret is positive."""
        outcome, message = check_guess(-10, 50)
        assert outcome == "Too Low"
        assert message == "📈 Go HIGHER!"

    def test_check_guess_positive_vs_negative(self):
        """Test when guess is positive and secret is negative."""
        outcome, message = check_guess(10, -50)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"

    def test_check_guess_large_positive_numbers(self):
        """Test with large positive numbers."""
        outcome, message = check_guess(1000000, 999999)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"

    def test_check_guess_large_negative_numbers(self):
        """Test with large negative numbers."""
        outcome, message = check_guess(-999999, -1000000)
        assert outcome == "Too High"
        assert message == "📉 Go LOWER!"


# ============================================================================
# Unit Tests for parse_guess function
# ============================================================================

class TestParseGuessValidInput:
    """Test parse_guess with valid integer inputs."""

    def test_parse_single_digit(self):
        """Test parsing a single digit number."""
        ok, guess_int, err = parse_guess("5")
        assert ok is True
        assert guess_int == 5
        assert err is None

    def test_parse_multi_digit(self):
        """Test parsing a multi-digit number."""
        ok, guess_int, err = parse_guess("150")
        assert ok is True
        assert guess_int == 150
        assert err is None

    def test_parse_large_number(self):
        """Test parsing a large number."""
        ok, guess_int, err = parse_guess("9999")
        assert ok is True
        assert guess_int == 9999
        assert err is None

    def test_parse_zero(self):
        """Test parsing zero."""
        ok, guess_int, err = parse_guess("0")
        assert ok is True
        assert guess_int == 0
        assert err is None

    def test_parse_negative_number(self):
        """Test parsing a negative number."""
        ok, guess_int, err = parse_guess("-50")
        assert ok is True
        assert guess_int == -50
        assert err is None


class TestParseGuessDecimalInput:
    """Test parse_guess with decimal inputs (should convert to int)."""

    def test_parse_decimal_whole_number(self):
        """Test parsing a decimal that represents a whole number."""
        ok, guess_int, err = parse_guess("50.0")
        assert ok is True
        assert guess_int == 50
        assert err is None

    def test_parse_decimal_with_fraction(self):
        """Test parsing a decimal with fractional part (should truncate)."""
        ok, guess_int, err = parse_guess("50.5")
        assert ok is True
        assert guess_int == 50
        assert err is None

    def test_parse_decimal_round_down(self):
        """Test that decimal fractions are truncated, not rounded."""
        ok, guess_int, err = parse_guess("99.9")
        assert ok is True
        assert guess_int == 99
        assert err is None

    def test_parse_decimal_negative(self):
        """Test parsing a negative decimal."""
        ok, guess_int, err = parse_guess("-25.7")
        assert ok is True
        assert guess_int == -25
        assert err is None
    
    def test_parse_whitespace_with_number(self):
        """Test parsing with whitespace around number (should succeed)."""
        ok, guess_int, err = parse_guess(" 50 ")
        assert ok is True
        assert guess_int == 50
        assert err is None


class TestParseGuessEmptyInput:
    """Test parse_guess with empty/null inputs."""

    def test_parse_empty_string(self):
        """Test parsing an empty string."""
        ok, guess_int, err = parse_guess("")
        assert ok is False
        assert guess_int is None
        assert err == "Enter a guess."

    def test_parse_none(self):
        """Test parsing None input."""
        ok, guess_int, err = parse_guess(None)
        assert ok is False
        assert guess_int is None
        assert err == "Enter a guess."


class TestParseGuessInvalidInput:
    """Test parse_guess with invalid inputs that are not numbers."""

    def test_parse_alphabetic(self):
        """Test parsing pure alphabetic input."""
        ok, guess_int, err = parse_guess("abc")
        assert ok is False
        assert guess_int is None
        assert err == "That is not a number."

    def test_parse_mixed_alphanumeric(self):
        """Test parsing mixed alphanumeric input."""
        ok, guess_int, err = parse_guess("50x")
        assert ok is False
        assert guess_int is None
        assert err == "That is not a number."

    def test_parse_special_characters(self):
        """Test parsing special characters."""
        ok, guess_int, err = parse_guess("@#$")
        assert ok is False
        assert guess_int is None
        assert err == "That is not a number."

    def test_parse_space_only(self):
        """Test parsing spaces."""
        ok, guess_int, err = parse_guess("   ")
        assert ok is False
        assert guess_int is None
        assert err == "That is not a number."

    def test_parse_multiple_decimal_points(self):
        """Test parsing input with multiple decimal points."""
        ok, guess_int, err = parse_guess("50.25.5")
        assert ok is False
        assert guess_int is None
        assert err == "That is not a number."


class TestParseGuessEdgeCases:
    """Test parse_guess with edge cases and boundary conditions."""

    def test_parse_leading_zeros(self):
        """Test parsing numbers with leading zeros."""
        ok, guess_int, err = parse_guess("007")
        assert ok is True
        assert guess_int == 7
        assert err is None

    def test_parse_very_small_decimal(self):
        """Test parsing very small decimal values."""
        ok, guess_int, err = parse_guess("0.1")
        assert ok is True
        assert guess_int == 0
        assert err is None

    def test_parse_scientific_notation(self):
        """Test parsing scientific notation (should fail)."""
        ok, guess_int, err = parse_guess("1e5")
        assert ok is False
        assert guess_int is None
        assert err == "That is not a number."


# ============================================================================
# Unit Tests for get_range_for_difficulty function
# ============================================================================


class TestGetRangeForDifficultyValidInput:
    """Test get_range_for_difficulty with valid difficulty levels."""

    def test_get_range_easy(self):
        """Test that Easy difficulty returns the correct range."""
        low, high = get_range_for_difficulty("Easy")
        assert low == 1
        assert high == 20

    def test_get_range_normal(self):
        """Test that Normal difficulty returns the correct range."""
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 100

    def test_get_range_hard(self):
        """Test that Hard difficulty returns the correct range."""
        low, high = get_range_for_difficulty("Hard")
        assert low == 1
        assert high == 500

    def test_range_is_tuple(self):
        """Test that the return value is a tuple."""
        result = get_range_for_difficulty("Easy")
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_range_values_are_integers(self):
        """Test that range values are integers."""
        low, high = get_range_for_difficulty("Normal")
        assert isinstance(low, int)
        assert isinstance(high, int)


class TestGetRangeForDifficultyOrdering:
    """Test that difficulty levels have increasing ranges."""

    def test_easy_less_than_normal(self):
        """Test that Easy range is smaller than Normal."""
        easy_low, easy_high = get_range_for_difficulty("Easy")
        normal_low, normal_high = get_range_for_difficulty("Normal")
        assert easy_high < normal_high

    def test_normal_less_than_hard(self):
        """Test that Normal range is smaller than Hard."""
        normal_low, normal_high = get_range_for_difficulty("Normal")
        hard_low, hard_high = get_range_for_difficulty("Hard")
        assert normal_high < hard_high

    def test_all_start_at_one(self):
        """Test that all difficulties start at 1."""
        easy_low, _ = get_range_for_difficulty("Easy")
        normal_low, _ = get_range_for_difficulty("Normal")
        hard_low, _ = get_range_for_difficulty("Hard")
        assert easy_low == 1
        assert normal_low == 1
        assert hard_low == 1

    def test_low_is_always_less_than_high(self):
        """Test that low is always less than high for all difficulties."""
        for difficulty in ["Easy", "Normal", "Hard"]:
            low, high = get_range_for_difficulty(difficulty)
            assert low < high


class TestGetRangeForDifficultyInvalidInput:
    """Test get_range_for_difficulty with invalid/unknown difficulty levels."""

    def test_unknown_difficulty_defaults_to_normal(self):
        """Test that unknown difficulty defaults to Normal range."""
        low, high = get_range_for_difficulty("Unknown")
        assert low == 1
        assert high == 100

    def test_empty_string_defaults_to_normal(self):
        """Test that empty string defaults to Normal range."""
        low, high = get_range_for_difficulty("")
        assert low == 1
        assert high == 100

    def test_none_defaults_to_normal(self):
        """Test that None defaults to Normal range."""
        low, high = get_range_for_difficulty(None)
        assert low == 1
        assert high == 100

    def test_lowercase_easy(self):
        """Test that lowercase 'easy' does not match (case-sensitive)."""
        low, high = get_range_for_difficulty("easy")
        # Should default to Normal since it doesn't match "Easy"
        assert low == 1
        assert high == 100

    def test_lowercase_hard(self):
        """Test that lowercase 'hard' does not match (case-sensitive)."""
        low, high = get_range_for_difficulty("hard")
        # Should default to Normal since it doesn't match "Hard"
        assert low == 1
        assert high == 100


class TestGetRangeForDifficultyEdgeCases:
    """Test get_range_for_difficulty with edge cases."""

    def test_range_consistency_easy(self):
        """Test that Easy range is consistent across multiple calls."""
        result1 = get_range_for_difficulty("Easy")
        result2 = get_range_for_difficulty("Easy")
        assert result1 == result2

    def test_range_consistency_hard(self):
        """Test that Hard range is consistent across multiple calls."""
        result1 = get_range_for_difficulty("Hard")
        result2 = get_range_for_difficulty("Hard")
        assert result1 == result2

    def test_range_with_extra_whitespace(self):
        """Test that extra whitespace is not trimmed (case-sensitive)."""
        low, high = get_range_for_difficulty(" Easy ")
        # Should default to Normal since " Easy " != "Easy"
        assert low == 1
        assert high == 100

    def test_range_with_typo(self):
        """Test that typos default to Normal range."""
        low, high = get_range_for_difficulty("Eazy")
        assert low == 1
        assert high == 100

    def test_range_normal_specific_values(self):
        """Test that Normal range has specific expected values."""
        low, high = get_range_for_difficulty("Normal")
        assert low == 1
        assert high == 100
        assert high - low + 1 == 100  # Inclusive range has 100 numbers


class TestGetRangeForDifficultyRangeSize:
    """Test the size and properties of each difficulty range."""

    def test_easy_range_size(self):
        """Test that Easy range has 20 numbers."""
        low, high = get_range_for_difficulty("Easy")
        range_size = high - low + 1
        assert range_size == 20

    def test_normal_range_size(self):
        """Test that Normal range has 100 numbers."""
        low, high = get_range_for_difficulty("Normal")
        range_size = high - low + 1
        assert range_size == 100

    def test_hard_range_size(self):
        """Test that Hard range has 500 numbers."""
        low, high = get_range_for_difficulty("Hard")
        range_size = high - low + 1
        assert range_size == 500

    def test_difficulty_progression(self):
        """Test that difficulty ranges increase proportionally."""
        easy_low, easy_high = get_range_for_difficulty("Easy")
        normal_low, normal_high = get_range_for_difficulty("Normal")
        hard_low, hard_high = get_range_for_difficulty("Hard")
        
        easy_size = easy_high - easy_low + 1
        normal_size = normal_high - normal_low + 1
        hard_size = hard_high - hard_low + 1
        
        # Hard is 5x Normal, Normal is 5x Easy
        assert normal_size == easy_size * 5
        assert hard_size == normal_size * 5


# ============================================================================
# Unit Tests for update_score function
# ============================================================================


class TestUpdateScoreWin:
    """Test update_score when the outcome is "Win"."""

    def test_win_first_attempt(self):
        """Test winning on first attempt gives maximum points."""
        new_score = update_score(0, "Win", 1)
        # 100 - 10 * (1 + 1) = 100 - 20 = 80
        assert new_score == 80

    def test_win_second_attempt(self):
        """Test winning on second attempt."""
        new_score = update_score(0, "Win", 2)
        # 100 - 10 * (2 + 1) = 100 - 30 = 70
        assert new_score == 70

    def test_win_third_attempt(self):
        """Test winning on third attempt."""
        new_score = update_score(0, "Win", 3)
        # 100 - 10 * (3 + 1) = 100 - 40 = 60
        assert new_score == 60

    def test_win_fifth_attempt(self):
        """Test winning on fifth attempt."""
        new_score = update_score(0, "Win", 5)
        # 100 - 10 * (5 + 1) = 100 - 60 = 40
        assert new_score == 40

    def test_win_tenth_attempt(self):
        """Test winning on tenth attempt."""
        new_score = update_score(0, "Win", 10)
        # 100 - 10 * (10 + 1) = 100 - 110 = -10, but minimum is 10
        assert new_score == 10

    def test_win_many_attempts(self):
        """Test winning after many attempts caps at minimum."""
        new_score = update_score(0, "Win", 20)
        # 100 - 10 * (20 + 1) = 100 - 210 = -110, but minimum is 10
        assert new_score == 10

    def test_win_with_existing_score(self):
        """Test winning when player already has a score."""
        new_score = update_score(50, "Win", 1)
        # 50 + (100 - 10 * 2) = 50 + 80 = 130
        assert new_score == 130

    def test_win_accumulates_score(self):
        """Test that win points accumulate with existing score."""
        score = 0
        score = update_score(score, "Too High", 1)  # -5
        score = update_score(score, "Too Low", 2)   # -5
        score = update_score(score, "Win", 3)       # +60
        assert score == 50  # -5 - 5 + 60 = 50


class TestUpdateScoreTooHigh:
    """Test update_score when the outcome is "Too High"."""

    def test_too_high_first_attempt_odd(self):
        """Test Too High on odd attempt gives negative points."""
        new_score = update_score(0, "Too High", 1)
        assert new_score == -5

    def test_too_high_second_attempt_even(self):
        """Test Too High on even attempt gives positive points."""
        new_score = update_score(0, "Too High", 2)
        assert new_score == 5

    def test_too_high_third_attempt_odd(self):
        """Test Too High on odd attempt gives negative points."""
        new_score = update_score(0, "Too High", 3)
        assert new_score == -5

    def test_too_high_fourth_attempt_even(self):
        """Test Too High on even attempt gives positive points."""
        new_score = update_score(0, "Too High", 4)
        assert new_score == 5

    def test_too_high_pattern_odd_attempts(self):
        """Test that odd attempts always lose 5 points."""
        for attempt in [1, 3, 5, 7, 9]:
            new_score = update_score(100, "Too High", attempt)
            assert new_score == 95, f"Failed for attempt {attempt}"

    def test_too_high_pattern_even_attempts(self):
        """Test that even attempts always gain 5 points."""
        for attempt in [2, 4, 6, 8, 10]:
            new_score = update_score(100, "Too High", attempt)
            assert new_score == 105, f"Failed for attempt {attempt}"

    def test_too_high_with_existing_score(self):
        """Test Too High with existing score."""
        new_score = update_score(50, "Too High", 2)
        assert new_score == 55


class TestUpdateScoreTooLow:
    """Test update_score when the outcome is "Too Low"."""

    def test_too_low_first_attempt(self):
        """Test Too Low always gives negative points."""
        new_score = update_score(0, "Too Low", 1)
        assert new_score == -5

    def test_too_low_second_attempt(self):
        """Test Too Low always gives negative points."""
        new_score = update_score(0, "Too Low", 2)
        assert new_score == -5

    def test_too_low_all_attempts_same(self):
        """Test that Too Low always gives -5 regardless of attempt."""
        for attempt in [1, 2, 3, 4, 5, 10]:
            new_score = update_score(100, "Too Low", attempt)
            assert new_score == 95, f"Failed for attempt {attempt}"

    def test_too_low_with_existing_score(self):
        """Test Too Low with existing score."""
        new_score = update_score(50, "Too Low", 3)
        assert new_score == 45

    def test_too_low_can_go_negative(self):
        """Test that score can go negative."""
        new_score = update_score(0, "Too Low", 1)
        assert new_score == -5


class TestUpdateScoreUnknownOutcome:
    """Test update_score with unknown or invalid outcomes."""

    def test_unknown_outcome_no_change(self):
        """Test that unknown outcome doesn't change score."""
        new_score = update_score(50, "Unknown", 1)
        assert new_score == 50

    def test_empty_string_outcome_no_change(self):
        """Test that empty string outcome doesn't change score."""
        new_score = update_score(50, "", 1)
        assert new_score == 50

    def test_none_outcome_no_change(self):
        """Test that None outcome doesn't change score."""
        new_score = update_score(50, None, 1)
        assert new_score == 50

    def test_lowercase_win_no_change(self):
        """Test that lowercase 'win' doesn't match (case-sensitive)."""
        new_score = update_score(50, "win", 1)
        assert new_score == 50

    def test_lowercase_too_high_no_change(self):
        """Test that lowercase 'too high' doesn't match (case-sensitive)."""
        new_score = update_score(50, "too high", 1)
        assert new_score == 50


class TestUpdateScoreEdgeCases:
    """Test update_score with edge cases and boundary conditions."""

    def test_zero_initial_score(self):
        """Test starting with zero score."""
        new_score = update_score(0, "Win", 1)
        assert new_score == 80

    def test_negative_initial_score(self):
        """Test starting with negative score."""
        new_score = update_score(-50, "Win", 1)
        assert new_score == 30  # -50 + 80 = 30

    def test_large_initial_score(self):
        """Test with very large initial score."""
        new_score = update_score(9999, "Win", 1)
        assert new_score == 10079  # 9999 + 80 = 10079

    def test_win_bonus_minimum_boundary(self):
        """Test that win bonus respects minimum of 10."""
        # Attempt 11 would give 100 - 10*12 = -20, but min is 10
        new_score = update_score(0, "Win", 11)
        assert new_score == 10

    def test_negative_score_after_too_low(self):
        """Test that multiple Too Low can drive score very negative."""
        score = 0
        score = update_score(score, "Too Low", 1)  # -5
        score = update_score(score, "Too Low", 2)  # -5
        score = update_score(score, "Too Low", 3)  # -5
        assert score == -15

    def test_alternating_outcomes(self):
        """Test alternating Too High (even/odd) pattern."""
        score = 0
        score = update_score(score, "Too High", 1)  # -5 (odd)
        score = update_score(score, "Too High", 2)  # +5 (even)
        score = update_score(score, "Too High", 3)  # -5 (odd)
        score = update_score(score, "Too High", 4)  # +5 (even)
        assert score == 0  # -5 + 5 - 5 + 5 = 0

    def test_mixed_outcomes_sequence(self):
        """Test sequence of different outcomes."""
        score = 0
        score = update_score(score, "Too High", 1)  # -5
        score = update_score(score, "Too Low", 2)   # -5
        score = update_score(score, "Too High", 3)  # -5
        score = update_score(score, "Too High", 4)  # +5
        score = update_score(score, "Win", 5)       # +40
        assert score == 30  # -5 - 5 - 5 + 5 + 40 = 30


class TestUpdateScoreAttemptNumberEdgeCases:
    """Test update_score with various attempt numbers."""

    def test_attempt_zero(self):
        """Test with attempt number 0."""
        new_score = update_score(0, "Win", 0)
        # 100 - 10 * (0 + 1) = 100 - 10 = 90
        assert new_score == 90

    def test_large_attempt_number(self):
        """Test with very large attempt number."""
        new_score = update_score(0, "Win", 1000)
        # 100 - 10 * (1000 + 1) = 100 - 10010, but min is 10
        assert new_score == 10

    def test_attempt_number_determines_too_high_outcome(self):
        """Test that attempt number determines Too High outcome."""
        # Odd attempts should lose points
        for attempt in range(1, 20, 2):
            score = update_score(100, "Too High", attempt)
            assert score == 95, f"Odd attempt {attempt} should lose 5 points"
        
        # Even attempts should gain points
        for attempt in range(2, 20, 2):
            score = update_score(100, "Too High", attempt)
            assert score == 105, f"Even attempt {attempt} should gain 5 points"
