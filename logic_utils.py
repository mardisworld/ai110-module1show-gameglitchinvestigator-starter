def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """
    Return the numeric range for a given difficulty level.
    
    Determines the lower and upper bounds for the secret number based on
    the selected difficulty. Higher difficulty levels increase the range,
    making the guessing game more challenging.
    
    Args:
        difficulty (str): The difficulty level. Must be one of "Easy", "Normal", or "Hard".
    
    Returns:
        tuple: A tuple of (low, high) representing the inclusive numeric range.
            - Easy: (1, 20) - smallest range for beginners
            - Normal: (1, 100) - standard range
            - Hard: (1, 500) - largest range for experienced players
            - Default/Unknown: (1, 100) - falls back to Normal
    
    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 500)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """
    Parse and validate user input into an integer guess.
    
    Converts raw string input from the user into an integer, handling edge cases
    like empty input, non-numeric values, and decimal numbers. Returns a tuple
    indicating success/failure along with the parsed value or error message.
    
    Args:
        raw (str): The raw user input string to parse.
    
    Returns:
        tuple: A tuple of (ok, guess_int, error_message) where:
            - ok (bool): True if parsing succeeded, False otherwise
            - guess_int (int or None): The parsed integer if ok is True, None if ok is False
            - error_message (str or None): An error message if ok is False, None if ok is True
    
    Raises:
        None: This function does not raise exceptions; it returns errors as part of the tuple.
    
    Examples:
        >>> parse_guess("50")
        (True, 50, None)
        >>> parse_guess("50.5")
        (True, 50, None)
        >>> parse_guess("")
        (False, None, "Enter a guess.")
        >>> parse_guess("abc")
        (False, None, "That is not a number.")
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """
    Compare a guess against the secret number and provide feedback.
    
    Evaluates whether the user's guess matches the secret number and provides
    appropriate feedback. Returns both a categorical outcome and a friendly
    message to guide the user.
    
    Args:
        guess: The user's guess (typically an integer).
        secret: The secret number to compare against (typically an integer).
    
    Returns:
        tuple: A tuple of (outcome, message) where:
            - outcome (str): One of "Win", "Too High", or "Too Low"
            - message (str): A friendly message with emoji to display to the user
                * "Win" returns "🎉 Correct!"
                * "Too High" returns "📉 Go LOWER!"
                * "Too Low" returns "📈 Go HIGHER!"
    
    Notes:
        - Handles TypeError gracefully by converting to strings for comparison
        - Includes emoji to make feedback more engaging
    
    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(60, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(40, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go LOWER!"
        else:
            return "Too Low", "📉 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Calculate and return the updated score based on game outcome and attempt number.
    
    Updates the player's score according to the result of their guess. Winning
    quickly (fewer attempts) awards more points. Incorrect guesses may earn or
    lose points based on their feedback direction.
    
    Scoring Rules:
        - Win: Base 100 points minus 10 per attempt. Minimum 10 points.
            Example: Win on attempt 3 = 100 - (10 * 4) = 60 points
        - Too High (even attempt): +5 points
        - Too High (odd attempt): -5 points
        - Too Low: -5 points
        - Any other outcome: No change
    
    Args:
        current_score (int): The player's current score before this update.
        outcome (str): The result of the guess. Expected values:
            * "Win" - player guessed correctly
            * "Too High" - player's guess was higher than the secret
            * "Too Low" - player's guess was lower than the secret
        attempt_number (int): The attempt number (1-indexed).
    
    Returns:
        int: The updated score after applying points for this outcome.
    
    Examples:
        >>> update_score(0, "Win", 1)
        90
        >>> update_score(0, "Win", 5)
        50
        >>> update_score(50, "Too High", 2)
        55
        >>> update_score(50, "Too High", 3)
        45
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
