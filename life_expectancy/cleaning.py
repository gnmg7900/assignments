"""Clean life expectancy data."""

# Importing packages
import argparse
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"


def clean_data(country="PT"):
    """Load, clean, and save a country life expectancy data."""
    # Loading the raw data
    life_data = pd.read_csv(DATA_DIR / "eu_life_expectancy_raw.tsv", sep="\t")

    # Unpivoting the data to long format
    life_data_long = pd.melt(life_data, id_vars=["unit,sex,age,geo\\time"], var_name="year")

    # unstacking the first column to separate the combined values into individual columns
    life_data_long[["unit", "sex", "age", "region"]] = life_data_long["unit,sex,age,geo\\time"].str.split(",", expand=True)

    life_data_long.drop(columns=["unit,sex,age,geo\\time"], inplace=True)

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

    # Saving the filtered data to a new CSV file under the data folder
    life_data_long_country.to_csv(DATA_DIR / f"{country.lower()}_life_expectancy.csv", index=False)

    return life_data_long_country


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", type=str, default="PT", help="Country code to filter the life expectancy data")
    args = parser.parse_args()
    clean_data(country=args.country)
