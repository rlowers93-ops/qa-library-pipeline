"""Tests for ingestion.py.

TODO: Implement these tests for load_csv, load_json, and load_excel in
src/data_processing/ingestion.py.
"""

import pytest
import pandas as pd
from data_processing.ingestion import load_csv, load_json, load_excel

def test_load_csv_success():
    """Test loading real CSV file."""
    df = load_csv('data/circulation_data.csv')

    assert len(df) > 0
    assert 'transaction_id' in df.columns

def test_load_csv_file_not_found():
    """Test error handling when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_csv('data/nonexistent.csv')

def test_load_json_success():
    """Test loading real JSON file."""
    df = load_json('data/events_data.json')

    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)

# Add more tests using tmp_path to create test files on the fly:

def test_load_csv_empty_file(tmp_path):
    """Test that an empty CSV raises an error."""
    empty = tmp_path / "empty.csv"
    empty.write_text("")
    with pytest.raises(pd.errors.EmptyDataError):
        load_csv(str(empty))

def test_load_json_file_not_found():
    """Test error handling when JSON file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_json('data/nonexistent.json')

def test_load_json_invalid(tmp_path):
    """Test that invalid JSON raises an error."""
    import json
    bad = tmp_path / "bad.json"
    bad.write_text("not valid json {{{")
    with pytest.raises(json.JSONDecodeError):
        load_json(str(bad))

def test_load_excel_success(tmp_path):
    df_expected = pd.DataFrame(
        {"book_id": [1, 2], "title": ["A", "B"]}
    )

    excel_file = tmp_path / "test.xlsx"
    df_expected.to_excel(excel_file, index=False)

    df_actual = load_excel(excel_file)

    assert len(df_actual) == 2
    assert "book_id" in df_actual.columns

def test_load_excel_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_excel("missing.xlsx")

def test_load_excel_invalid_sheet(tmp_path):
    df = pd.DataFrame({"a": [1]})

    excel_file = tmp_path / "test.xlsx"
    df.to_excel(excel_file, index=False)

    with pytest.raises(ValueError):
        load_excel(excel_file, sheet_name="DoesNotExist")