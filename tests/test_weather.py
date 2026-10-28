"""Starter tests for the weather module.

These tests deliberately cover only ordinary examples. They show how pytest works,
but they are not a sufficient test suite for the specification in SPECIFICATION.md.
"""
import pytest

from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)


def test_parse_time_regular_time():
    assert parse_time("14:10") == 850
    assert parse_time("0:0") == 0

def test_parse_time_parts():
    with pytest.raises(ValueError, match="Time must have HH:MM format."):
        parse_time("2:2:2")

def test_parse_time_isdigit():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_time("abadsf:dsfdsf")

def test_parse_time_hour():
    with pytest.raises(ValueError, match="Hour must be between 0 and 23."):
        parse_time("27:12")

def test_parse_time_minute():
    with pytest.raises(ValueError, match="Minute must be between 0 and 59."):
        parse_time("00:76")



def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21") == ("Köln", 861, 21.0)

def test_parse_measurement_isstring():
    with pytest.raises(ValueError, match="Measurement must be a string."):
        parse_measurement(76)

def test_parse_measurement_isstring():
    with pytest.raises(ValueError, match= "Expected exactly three fields."):
        parse_measurement("fsdfsdfdsf")

def test_parse_measurement_isstring():
    with pytest.raises(ValueError, match= "City must not be empty."):
        parse_measurement(";14:00;12")

def test_parse_measurement_isstring():
    with pytest.raises(ValueError, match= "Temperature must be numeric."):
        parse_measurement("Dus;14:00;dedd")

def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]

    with pytest.raises(ValueError, match= "lower must not be greater than upper."):
        filter_by_temperature(measurements, 9, 6)



def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0


def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)
