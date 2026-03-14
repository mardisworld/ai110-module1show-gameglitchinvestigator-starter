import sys
from pathlib import Path

# Add parent directory to path so we can import logic_utils
sys.path.insert(0, str(Path(__file__).parent.parent))

from logic_utils import check_guess, parse_guess


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

    