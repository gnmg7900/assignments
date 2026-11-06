"""Tests for the cleaning module."""

import shutil
import sys

import pandas as pd

from life_expectancy import cleaning
from life_expectancy.cli import main


def test_main_defaults_to_portugal(
    tmp_path, monkeypatch, pt_life_expectancy_expected
):
    """Run the CLI with its default country and check the output."""
    raw_file = cleaning.DATA_DIR / cleaning.RAW_FILE
    shutil.copyfile(raw_file, tmp_path / cleaning.RAW_FILE)

    monkeypatch.setattr(cleaning, "DATA_DIR", tmp_path)
    monkeypatch.setattr(sys, "argv", ["life_expectancy.cli"])

    main()

    actual = pd.read_csv(tmp_path / "pt_life_expectancy.csv")
    pd.testing.assert_frame_equal(actual, pt_life_expectancy_expected)


def test_main_accepts_country_argument(tmp_path, monkeypatch):
    """Run the CLI for France and check the output."""
    raw_file = cleaning.DATA_DIR / cleaning.RAW_FILE
    shutil.copyfile(raw_file, tmp_path / cleaning.RAW_FILE)

    monkeypatch.setattr(cleaning, "DATA_DIR", tmp_path)
    monkeypatch.setattr(
        sys, "argv", ["life_expectancy.cli", "--country", "FR"]
    )

    main()

    actual = pd.read_csv(tmp_path / "fr_life_expectancy.csv")
    assert not actual.empty
    assert set(actual["region"]) == {"FR"}
