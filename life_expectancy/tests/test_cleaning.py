"""Tests for the cleaning module"""
import sys

import pandas as pd

from life_expectancy import cleaning, cli
from life_expectancy.cli import main


def test_main(
    monkeypatch, tmp_path, eu_life_expectancy_raw, eu_life_expectancy_expected
):
    """Run `main` on the sample input and compare with the expected output"""
    monkeypatch.setattr(sys, "argv", ["life_expectancy.cli"])
    monkeypatch.setattr(cli, "load_data", lambda: eu_life_expectancy_raw)
    monkeypatch.setattr(cleaning, "DATA_DIR", tmp_path)

    result = main()

    pd.testing.assert_frame_equal(
        result.reset_index(drop=True), eu_life_expectancy_expected
    )
