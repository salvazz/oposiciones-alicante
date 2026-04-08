import pytest

# Example validation functions

def is_valid_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_positive_integer(value):
    return isinstance(value, int) and value > 0

# Test cases for validation functions

def test_is_valid_email():
    assert is_valid_email("test@example.com") == True
    assert is_valid_email("invalid-email") == False
    assert is_valid_email("@example.com") == False
    assert is_valid_email("test@.com") == False


def test_is_positive_integer():
    assert is_positive_integer(10) == True
    assert is_positive_integer(-1) == False
    assert is_positive_integer(0) == False
    assert is_positive_integer("string") == False
    assert is_positive_integer(3.5) == False
