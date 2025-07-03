import subprocess
import tempfile
import csv
import pytest
import sys
import os


@pytest.fixture
def csv_file(tmp_path, sample_data):
    file_path = tmp_path / "test.csv"
    with file_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=sample_data[0].keys())
        writer.writeheader()
        writer.writerows(sample_data)
    return file_path


def run_main_cli(args):
    full_path = os.path.join(os.path.dirname(__file__), "..", "main.py")
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return subprocess.run([sys.executable, full_path] + args, capture_output=True, text=True, env=env)


def test_cli_no_args(csv_file):
    result = run_main_cli([str(csv_file)])
    assert result.returncode == 0
    assert "iphone 15 pro" in result.stdout


def test_cli_where_filter(csv_file):
    result = run_main_cli([str(csv_file), "--where", "brand=apple"])
    assert result.returncode == 0
    assert "iphone 15 pro" in result.stdout
    assert "galaxy s23 ultra" not in result.stdout


def test_cli_aggregate_valid(csv_file):
    expected = {
        "avg": "674",
        "min": "199",
        "max": "1199"
    }
    for func, value in expected.items():
        result = run_main_cli([str(csv_file), "--aggregate", f"price={func}"])
        assert result.returncode == 0
        assert func in result.stdout
        assert value in result.stdout


def test_cli_aggregate_non_numeric(csv_file):
    tests = ["name=avg", "brand=min", "brand=max"]
    for expression in tests:
        result = run_main_cli([str(csv_file), "--aggregate", expression])
        assert result.returncode != 0
        assert "Ошибка агрегирования" in result.stderr


def test_cli_invalid_operator(csv_file):
    result = run_main_cli([str(csv_file), "--where", "price!=999"])
    assert result.returncode != 0
    assert "Ошибка фильтрации" in result.stderr


def test_cli_invalid_aggregate_func(csv_file):
    result = run_main_cli([str(csv_file), "--aggregate", "price=sum"])
    assert result.returncode != 0
    assert "Ошибка агрегирования" in result.stderr


def test_cli_empty_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("name,brand,price,rating\n")  # только заголовки
    result = run_main_cli([str(empty_file)])
    assert result.returncode == 0
    assert result.stdout.strip() == ""


def test_cli_no_filename():
    result = run_main_cli([])
    assert result.returncode != 0
    assert "Необходимо указать CSV-файл" in result.stderr
