"""Load and save life expectancy data."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
INPUT_FILE = DATA_DIR / "eu_life_expectancy_raw.tsv"


def load_data(input_file: Path = INPUT_FILE) -> pd.DataFrame:
    """Load the raw life expectancy data."""
    return pd.read_csv(input_file, sep="\t")


def save_data(life_data_country: pd.DataFrame, country: str = "PT") -> None:
    """Save the cleaned life expectancy data to a CSV file."""
    output_file = DATA_DIR / f"{country.lower()}_life_expectancy.csv"
    life_data_country.to_csv(output_file, index=False)
