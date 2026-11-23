"""Tests for life expectancy data input and output."""

from unittest.mock import Mock

import pandas as pd

from life_expectancy import data_io


def test_load_data(monkeypatch):
    """Load the TSV file using pandas."""
    expected = pd.DataFrame({"region": ["PT"]})
    read_csv = Mock(return_value=expected)
    monkeypatch.setattr(data_io.pd, "read_csv", read_csv)

    result = data_io.load_data()

    assert result is expected
    read_csv.assert_called_once_with(data_io.INPUT_FILE, sep="\t")


def test_save_data(monkeypatch, tmp_path):
    """Save data without writing a file during the test."""
    monkeypatch.setattr(data_io, "DATA_DIR", tmp_path)
    to_csv = Mock(side_effect=lambda *args, **kwargs: print("to_csv mocked: no file written"))
    monkeypatch.setattr(pd.DataFrame, "to_csv", to_csv)
    data = pd.DataFrame({"region": ["PT"]})

    data_io.save_data(data)

    to_csv.assert_called_once_with(
        tmp_path / "pt_life_expectancy.csv", index=False
    )
