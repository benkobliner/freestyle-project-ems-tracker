"""Tests for FDNY EMS Data Explorer analysis functions."""

from main import (
    year_filter,
    borough_filter,
)


def test_year_filter():
    result = year_filter(2025)

    assert (
        "incident_datetime >= "
        "'2025-01-01T00:00:00.000'"
        in result
    )

    assert (
        "incident_datetime < "
        "'2026-01-01T00:00:00.000'"
        in result
    )


def test_all_nyc_borough_filter():
    result = borough_filter("All NYC")

    assert result == ""


def test_manhattan_borough_filter():
    result = borough_filter("Manhattan")

    assert result == " AND borough='MANHATTAN'"


def test_brooklyn_borough_filter():
    result = borough_filter("Brooklyn")

    assert result == " AND borough='BROOKLYN'"


def test_staten_island_borough_filter():
    result = borough_filter("Staten Island")

    assert (
        result
        == " AND borough='RICHMOND / STATEN ISLAND'"
    )
