import pytest
from type_detect import detect_type


@pytest.mark.parametrize("input_str, expected_type", [
    ("123", int),
    ("3.14", float),
    ("abc", str),
    ("1e3", float),
    ("", str),
    (" ", str),
    ("0", int),
    ("0.0", float)
])
def test_detect_type(input_str, expected_type):
    assert detect_type(input_str) == expected_type
