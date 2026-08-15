"""Tests for the EMS map project."""

import pandas as pd

from main import load_data, make_map


def test_load_data_keeps_manhattan(tmp_path):
    file = tmp_path / "calls.csv"
    pd.DataFrame({
        "borough": ["MANHATTAN", "BROOKLYN"],
        "latitude": [40.75, 40.65],
        "longitude": [-73.99, -73.95],
    }).to_csv(file, index=False)

    assert len(load_data(file)) == 1


def test_load_data_returns_manhattan(tmp_path):
    file = tmp_path / "calls.csv"
    pd.DataFrame({
        "borough": ["MANHATTAN", "BROOKLYN"],
        "latitude": [40.75, 40.65],
        "longitude": [-73.99, -73.95],
    }).to_csv(file, index=False)

    assert load_data(file).iloc[0]["borough"] == "MANHATTAN"


def test_make_map_creates_file(tmp_path):
    df = pd.DataFrame({"latitude": [40.75], "longitude": [-73.99]})
    output = tmp_path / "map.html"

    make_map(df, output)

    assert output.exists()
