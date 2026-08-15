"""Create a simple map of Manhattan EMS calls."""

import folium
import pandas as pd


def load_data(filename):
    """Read EMS data and keep only Manhattan calls."""
    df = pd.read_csv(filename)
    return df[df["borough"].str.upper() == "MANHATTAN"]


def make_map(df, output="ems_map.html"):
    """Create and save a map from latitude and longitude columns."""
    ems_map = folium.Map(location=[40.78, -73.97], zoom_start=12)

    for _, row in df.iterrows():
        folium.Marker([row["latitude"], row["longitude"]]).add_to(ems_map)

    ems_map.save(output)
    return output


if __name__ == "__main__":
    data = load_data("sample_ems_calls.csv")
    make_map(data)
    print("Map created: ems_map.html")
