"""Tests for the cleaning module"""
import sys
from unittest.mock import Mock

import pandas as pd

from life_expectancy import cli, data_io
from life_expectancy.cleaning import clean_data


def test_clean_data(eu_life_expectancy_raw, eu_life_expectancy_expected):
    """Clean the sample data and compare it with the expected output."""
    result = clean_data(eu_life_expectancy_raw)
    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), eu_life_expectancy_expected
    )


def test_main(
    monkeypatch, tmp_path, eu_life_expectancy_raw, eu_life_expectancy_expected
):
    """Run the pipeline on sample data and check its result and save call."""
    monkeypatch.setattr(sys, "argv", ["life_expectancy.cli"])
    monkeypatch.setattr(cli, "load_data", lambda: eu_life_expectancy_raw)
    monkeypatch.setattr(data_io, "DATA_DIR", tmp_path)
    to_csv = Mock(side_effect=lambda *args, **kwargs: print("to_csv mocked: no file written"))
    monkeypatch.setattr(pd.DataFrame, "to_csv", to_csv)

    result = cli.main()

    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), eu_life_expectancy_expected
    )
    to_csv.assert_called_once_with(
        tmp_path / "pt_life_expectancy.csv", index=False
    )
