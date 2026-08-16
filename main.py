"""Functions for retrieving and analyzing FDNY EMS incident data."""

import requests
import pandas as pd


API_URL = "https://data.cityofnewyork.us/resource/76xm-jjuj.json"


def query_api(params):
    """Send a query to NYC Open Data and return the results as a DataFrame."""
    response = requests.get(
        API_URL,
        params=params,
        timeout=120,
    )
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

    borough_map = {
        "Manhattan": "MANHATTAN",
        "Bronx": "BRONX",
        "Brooklyn": "BROOKLYN",
        "Queens": "QUEENS",
        "Staten Island": "RICHMOND / STATEN ISLAND",
    }

    api_borough = borough_map.get(
        borough,
        borough.upper(),
    )

    return f" AND borough='{api_borough}'"


def clean_borough_name(borough):
    """Convert FDNY borough labels into presentation-friendly names."""
    borough_names = {
        "MANHATTAN": "Manhattan",
        "BRONX": "Bronx",
        "BROOKLYN": "Brooklyn",
        "QUEENS": "Queens",
        "RICHMOND / STATEN ISLAND": "Staten Island",
        "RICHMOND": "Staten Island",
    }

    return borough_names.get(
        borough,
        borough.title(),
    )


def get_call_type_counts(
    year,
    call_type,
    borough="All NYC",
):
    """
    Return EMS incident counts by ZIP code for a selected final call type.
    """
    where = (
        f"{year_filter(year)} "
        f"AND final_call_type='{call_type.upper()}' "
        "AND zipcode IS NOT NULL"
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

    df["call_count"] = pd.to_numeric(
        df["call_count"]
    )

    return df


def get_response_times_by_borough(
    year,
    high_severity_only=False,
):
    """
    Return average valid EMS incident response time by borough.

    If high_severity_only is True, only final severity levels 1-3
    are included.
    """
    where = (
        f"{year_filter(year)} "
        "AND borough IS NOT NULL "
        "AND incident_response_seconds_qy IS NOT NULL "
        "AND valid_incident_rspns_time_indc='Y'"
    )

    if high_severity_only:
        where += (
            " AND final_severity_level_code "
            "IN ('1','2','3')"
        )

    params = {
        "$select": (
            "borough, "
            "avg(incident_response_seconds_qy) "
            "AS avg_response_seconds, "
            "count(*) AS call_count"
        ),
        "$where": where,
        "$group": "borough",
        "$order": "avg_response_seconds DESC",
        "$limit": 100,
    }

    df = query_api(params)

    if df.empty:
        return df

    df["avg_response_seconds"] = pd.to_numeric(
        df["avg_response_seconds"]
    )

    df["call_count"] = pd.to_numeric(
        df["call_count"]
    )

    df["avg_response_minutes"] = (
        df["avg_response_seconds"] / 60
    ).round(2)

    df["borough"] = df["borough"].apply(
        clean_borough_name
    )

    return df


def get_held_incident_rates(
    year,
    borough="All NYC",
    high_severity_only=False,
    minimum_calls=100,
):
    """
    Return total incidents, held incidents, and held percentage by ZIP.

    HELD_INDICATOR is reported descriptively because the public
    dataset does not provide a detailed operational definition
    of what causes an incident to be marked held.
    """

    base_where = (
        f"{year_filter(year)} "
        "AND zipcode IS NOT NULL"
        f"{borough_filter(borough)}"
    )

    if high_severity_only:
        base_where += (
            " AND final_severity_level_code "
            "IN ('1','2','3')"
        )

    # Query 1: total qualifying EMS incidents by ZIP
    total_params = {
        "$select": "zipcode, count(*) AS total_calls",
        "$where": base_where,
        "$group": "zipcode",
        "$limit": 5000,
    }

    total_df = query_api(total_params)

    if total_df.empty:
        return total_df

    # Query 2: incidents marked held by ZIP
    held_where = (
        base_where
        + " AND held_indicator='Y'"
    )

    held_params = {
        "$select": "zipcode, count(*) AS held_calls",
        "$where": held_where,
        "$group": "zipcode",
        "$limit": 5000,
    }

    held_df = query_api(held_params)

    total_df["total_calls"] = pd.to_numeric(
        total_df["total_calls"]
    )

    if held_df.empty:
        total_df["held_calls"] = 0
        result = total_df

    else:
        held_df["held_calls"] = pd.to_numeric(
            held_df["held_calls"]
        )

        result = total_df.merge(
            held_df,
            on="zipcode",
            how="left",
        )

        result["held_calls"] = (
            result["held_calls"]
            .fillna(0)
            .astype(int)
        )

    # Exclude ZIP codes with too few qualifying calls
    result = result[
        result["total_calls"] >= minimum_calls
    ].copy()

    if result.empty:
        return result

    # Calculate percentage locally in Pandas
    result["held_percentage"] = (
        result["held_calls"]
        / result["total_calls"]
        * 100
    ).round(2)

    result = result.sort_values(
        "held_percentage",
        ascending=False,
    )

    return result


if __name__ == "__main__":
    print("Testing connection to NYC Open Data...")

    sample = get_call_type_counts(
        year=2025,
        call_type="DROWN",
    )

    print(sample.head(10))
