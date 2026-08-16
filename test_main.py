"""Tests for FDNY EMS Data Explorer analysis functions."""

from main import (
    year_filter,
    borough_filter,
    classify_day_night,
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


def test_day_classification():
    assert classify_day_night(8) == "Day"
    assert classify_day_night(12) == "Day"
    assert classify_day_night(19) == "Day"


def test_night_classification():
    assert classify_day_night(20) == "Night"
    assert classify_day_night(23) == "Night"
    assert classify_day_night(0) == "Night"
    assert classify_day_night(7) == "Night"
