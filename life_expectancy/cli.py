"""Command-line entry point for cleaning life expectancy data"""

import argparse

from life_expectancy.cleaning import clean_data, load_data, save_data

def main() -> None:
    """Parse command-line options and run the cleaning process"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--country",
        default="PT",
        help="Country code to filter the life expectancy data",
    )
    args = parser.parse_args()

    life_data=load_data()
    cleaned_data = clean_data(life_data, country=args.country)
    save_data(cleaned_data, country=args.country)

if __name__ == "__main__": # pragma: no cover
    main()
