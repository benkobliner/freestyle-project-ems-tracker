"""Functions for retrieving and analyzing FDNY EMS incident data."""

import requests
import pandas as pd


API_URL = "https://data.cityofnewyork.us/resource/76xm-jjuj.json"


def query_api(params):
    """Send a query to NYC Open Data and return the results as a DataFrame."""
    response = requests.get(API_URL, params=params, timeout=60)
    response.raise_for_status()
    return pd.DataFrame(response.json())


def year_filter(year):
    """Create a SoQL date filter for a calendar year."""
    start = f"{year}-01-01T00:00:00.000"
    end = f"{year + 1}-01-01T00:00:00.000"

    return (
        f"incident_datetime >= '{start}' "
        f"AND incident_datetime < '{end}'"
    )


def borough_filter(borough):
    """Return an optional borough filter."""
    if borough == "All NYC":
        return ""

    return f" AND borough='{borough.upper()}'"


def get_call_type_counts(year, call_type, borough="All NYC"):
    """
    Return EMS incident counts by ZIP code for a selected final call type.
    """
    where = (
        f"{year_filter(year)} "
        f"AND final_call_type='{call_type.upper()}' "
        f"AND zipcode IS NOT NULL"
        f"{borough_filter(borough)}"
    )

    params = {
        "$select": "zipcode, count(*) AS call_count",
        "$where": where,
        "$group": "zipcode",
        "$order": "call_count DESC",
        "$limit": 5000,
    }

    df = query_api(params)

    if df.empty:
        return df

    df["call_count"] = pd.to_numeric(df["call_count"])
    return df


def get_response_times(
    year,
    borough="All NYC",
    high_severity_only=False,
    minimum_calls=50,
):
    """
    Return average valid EMS response time by ZIP code.

    If high_severity_only is True, only final severity levels 1-3
    are included.
    """
    where = (
        f"{year_filter(year)} "
        "AND zipcode IS NOT NULL "
        "AND incident_response_seconds_qy IS NOT NULL "
        "AND valid_incident_rspns_time_indc='Y'"
        f"{borough_filter(borough)}"
    )

    if high_severity_only:
        where += (
            " AND final_severity_level_code "
            "IN ('1','2','3')"
        )

    params = {
        "$select": (
            "zipcode, "
            "avg(incident_response_seconds_qy) AS avg_response_seconds, "
            "count(*) AS call_count"
        ),
        "$where": where,
        "$group": "zipcode",
        "$having": f"count(*) >= {minimum_calls}",
        "$order": "avg_response_seconds DESC",
        "$limit": 5000,
    }

    df = query_api(params)

    if df.empty:
        return df

    df["avg_response_seconds"] = pd.to_numeric(
        df["avg_response_seconds"]
    )
    df["call_count"] = pd.to_numeric(df["call_count"])

    df["avg_response_minutes"] = (
        df["avg_response_seconds"] / 60
    ).round(2)

    return df


def classify_day_night(hour):
    """
    Classify an hour as Day or Night.

    Day is defined as 08:00 through 19:59.
    Night is defined as 20:00 through 07:59.
    """
    hour = int(hour)

    if 8 <= hour < 20:
        return "Day"

    return "Night"


def get_day_night_counts(year, borough="All NYC"):
    """
    Return EMS incident counts by ZIP code for daytime and nighttime.
    """
    where = (
        f"{year_filter(year)} "
        "AND zipcode IS NOT NULL"
        f"{borough_filter(borough)}"
    )

    params = {
        "$select": (
            "zipcode, "
            "date_extract_hh(incident_datetime) AS hour, "
            "count(*) AS call_count"
        ),
        "$where": where,
        "$group": (
            "zipcode, date_extract_hh(incident_datetime)"
        ),
        "$limit": 5000,
    }

    df = query_api(params)

    if df.empty:
        return df

    df["hour"] = pd.to_numeric(df["hour"])
    df["call_count"] = pd.to_numeric(df["call_count"])

    df["period"] = df["hour"].apply(classify_day_night)

    summary = (
        df.groupby(["zipcode", "period"], as_index=False)["call_count"]
        .sum()
    )

    return summary


if __name__ == "__main__":
    print("Testing connection to NYC Open Data...")

    sample = get_call_type_counts(
        year=2025,
        call_type="DROWN",
    )

    print(sample.head(10))
