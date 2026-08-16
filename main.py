"""Retrieve live FDNY EMS incident data from NYC Open Data."""

import requests
import pandas as pd


API_URL = "https://data.cityofnewyork.us/resource/76xm-jjuj.json"


def load_data(limit=100):
    """Retrieve a sample of Manhattan EMS incidents from NYC Open Data."""
    params = {
        "$limit": limit,
        "$where": "borough='MANHATTAN'",
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    return pd.DataFrame(response.json())


if __name__ == "__main__":
    data = load_data()

    print(f"Retrieved {len(data)} EMS incidents.")
    print()
    print("Columns returned by NYC Open Data:")
    print(data.columns.tolist())
    print()
    print("First five rows:")
    print(data.head())
