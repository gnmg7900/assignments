"""Clean life expectancy data."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"
RAW_FILE = "eu_life_expectancy_raw.tsv"
COMBINED_COLUMN = "unit,sex,age,geo\\time"


def load_data() -> pd.DataFrame:
    """Load the raw life expectancy data."""
    return pd.read_csv(DATA_DIR / RAW_FILE, sep="\t")


def clean_data(life_data: pd.DataFrame, country: str = "PT") -> pd.DataFrame:
    """Cleaning and filtering life expectancy data for a specific country."""
    # Unpivoting the data to long format
    life_data_long = pd.melt(life_data, id_vars=[COMBINED_COLUMN], var_name="year")

    # unstacking the first column to separate the combined values into individual columns
    life_data_long[["unit", "sex", "age", "region"]] = life_data_long[COMBINED_COLUMN].str.split(",", expand=True)

    life_data_long.drop(columns=[COMBINED_COLUMN], inplace=True)

    # Reordering the columns to match the expected output
    life_data_long = life_data_long[["unit", "sex", "age", "region", "year", "value"]].copy()

    # Ensuring "year" column is of integer type (column names have trailing spaces)
    life_data_long["year"] = life_data_long["year"].str.strip().astype(int)

    # Ensuring "value" column is of numeric type: keep only the number (e.g. "84.3 b" -> 84.3), ": " becomes NaN
    life_data_long["value"] = pd.to_numeric(life_data_long["value"].str.extract(r"(\d+\.?\d*)")[0], errors="coerce")

    # Removing rows without a value
    life_data_long = life_data_long.dropna(subset=["value"])

    # Filtering the data in which the "region" is the chosen country
    life_data_long_country = life_data_long[life_data_long["region"] == country]

    return life_data_long_country


def save_data(life_data_country: pd.DataFrame, country: str = "PT") -> None:
    """Saving the cleaned life expectancy data to a CSV file."""
    life_data_country.to_csv(DATA_DIR / f"{country.lower()}_life_expectancy.csv", index=False)
