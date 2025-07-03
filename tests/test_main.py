import pytest
from main import parse_expression


def test_parse_expression_valid():
    expr = "age>30"
    pattern = r"(.+?)([!<>=]{1,2})(.+)"
    assert parse_expression(expr, pattern) == ["age", ">", "30"]


def test_parse_expression_invalid():
    expr = "age30"
    pattern = r"(.+?)([!<>=]{1,2})(.+)"
    with pytest.raises(ValueError):
        parse_expression(expr, pattern)


def test_parse_expression_aggregate():
    expr = "salary=avg"
    pattern = r"(.+?)=(avg|min|max)"
    assert parse_expression(expr, pattern) == ["salary", "avg"]
