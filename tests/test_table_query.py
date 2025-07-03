import pytest


def test_column_types(table_from_csv):
    assert table_from_csv.column_types == {"name": str, "brand": str, "price": int, "rating": float}


def test_aggregate_invalid_function(table_from_csv):
    with pytest.raises(ValueError):
        table_from_csv.aggregate('price', 'sum')
