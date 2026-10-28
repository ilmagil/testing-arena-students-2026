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

    with pytest.raises(ValueError):
        parse_time("267")

def test_parse_time_parts():
    with pytest.raises(ValueError, match="Time must have HH:MM format."):
        parse_time("2:2:2")
    with pytest.raises(ValueError):
        parse_time("14.23:21.45")
    with pytest.raises(ValueError):
        parse_time("00:60")
    with pytest.raises(ValueError):
        parse_time("24:00")

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
        ("Köln", 600, 15),
        ("Köln", 720, 15),
    ]

    assert average_temperature(measurements, "Köln") == 15.0

    with pytest.raises(ValueError, match= "No measurements found for city."):
        average_temperature("Kölnfdsfd", 6)

def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)

    with pytest.raises(ValueError, match= "No measurements available."):
        hottest_measurement("")

def test_parse_time_input_text():
    with pytest.raises(AttributeError):
        assert parse_time(22)

def test_parse_time_input_text_2():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        assert parse_time("1s:e2")

def test_parse_time_input_colums_1():
    with pytest.raises(ValueError, match="Time must have HH:MM format."):
        assert parse_time("1:1:1")

def test_parse_time_input_colums_2():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        assert parse_time(":")

def test_parse_time_input_whitespace():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        assert parse_time(" 1 : 33 ")

def test_parse_time_input_format():
    assert parse_time("1:2") == 62

def test_parse_time_input_range1():
    with pytest.raises(ValueError, match="Hour must be between 0 and 23."):
        assert parse_time("44:22")

def test_parse_time_input_range2():
    with pytest.raises(ValueError, match="Minute must be between 0 and 59."):
        assert parse_time("22:99")

def test_parse_time_input_range3():
    with pytest.raises(ValueError):
        assert parse_time("-44:-33")

def test_parse_time_regular_time():
    assert parse_time("14:21") == 861

#####
##

def test_parse_measurement_input():
    with pytest.raises(ValueError, match="Measurement must be a string."):
        assert parse_measurement(22)

def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)

def test_parse_measurement_input_format():
    with pytest.raises(ValueError, match="Expected exactly three fields."):
        assert parse_measurement("Köln,14;21.7;;")

def test_parse_measurement_input_whitespace_1():
    assert parse_measurement(" Köln;14:21;21.7 ") == ("Köln", 861, 21.7)

def test_parse_measurement_input_whitespace_2():
    with pytest.raises(ValueError, match="City must not be empty."):
        assert parse_measurement(" ;14:21;21.7 ")

def test_parse_measurement_input_whitespace_3():
    assert parse_measurement(" Köln ; 14:21 ; 21.7 ") == ("Köln", 861, 21.7)

def test_parse_measurement_type_1():
    assert parse_measurement("Köln;14:21;21") == ("Köln", 861, 21.0)

def test_parse_measurement_type_2():
    with pytest.raises(ValueError, match="Temperature must be numeric."):
        assert parse_measurement("Köln;14:21;i")

def test_parse_measurement_parse_time():
    with pytest.raises(ValueError, match="Time must have HH:MM format."):
        assert parse_measurement("Köln;14,44;43.2")

def test_parse_measurement_extreme():
    assert parse_measurement("Köln;14:21;999") == ("Köln", 861, 999)

#####
##

def test_filter_by_temperature():
    with pytest.raises(ValueError, match="lower must not be greater than upper."):
        assert filter_by_temperature(67, 99, 2)

def test_filter_by_temperature_input_1():
    with pytest.raises(TypeError):
        assert filter_by_temperature([11,22], [22], [33])


def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]

def test_filter_by_temperature_order_rows():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 20.0) == [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5)
    ]

def test_filter_by_temperature_duplicates():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 20.0) == [
        ("Köln", 600, 10.0),
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5)
    ]

def test_filter_by_temperature_not_modified():
    measurements = [
        ("Berlin", 600, 15.0),
        ("Hamburg", 540, 25.0),
        ("Munich", 660, 18.0),
    ]
    original_measurements = measurements.copy()

    filter_by_temperature(measurements, 15.0, 20.0)

    assert measurements == original_measurements

#####
##

def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0

def test_average_temperature_regular_values_1():
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

