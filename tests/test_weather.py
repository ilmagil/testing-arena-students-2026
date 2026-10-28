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


def test_parse_time_regular_time():
    assert parse_time("14:10") == 850
    assert parse_time("0:0") == 0

    with pytest.raises(ValueError):
        parse_time("267")

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

def test_parse_time_regular_time():
    with pytest.raises(ValueError):
        parse_time("14.23:21.45")
    with pytest.raises(ValueError):
        parse_time("00:60")
    with pytest.raises(ValueError):
        parse_time("24:00")

def test_parse_time_midnight():
    assert parse_time("00:00") == 0


def test_parse_time_last_minute_of_day():
    assert parse_time("23:59") == 1439


def test_parse_time_hour_boundary_zero():
    assert parse_time("0:30") == 30


def test_parse_time_hour_boundary_twenty_three():
    assert parse_time("23:00") == 1380


def test_parse_time_empty_string():
    with pytest.raises(ValueError, match="Time must have HH:MM format."):
        parse_time("")


def test_parse_time_missing_hour():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_time(":30")


def test_parse_time_missing_minute():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_time("12:")


def test_parse_time_negative_hour():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_time("-1:30")


def test_parse_time_negative_minute():
    with pytest.raises(ValueError, match="Hour and minute must be numeric."):
        parse_time("12:-1")


def test_parse_measurement_negative_temperature():
    assert parse_measurement("Berlin;00:00;-12.5") == (
        "Berlin", 0, -12.5
    )


def test_parse_measurement_zero_temperature():
    assert parse_measurement("Berlin;12:00;0") == (
        "Berlin", 720, 0.0
    )


def test_parse_measurement_decimal_temperature():
    assert parse_measurement("Berlin;12:30;18.75") == (
        "Berlin", 750, 18.75
    )


def test_parse_measurement_too_few_fields():
    with pytest.raises(ValueError, match="Expected exactly three fields."):
        parse_measurement("Berlin;12:30")


def test_parse_measurement_too_many_fields():
    with pytest.raises(ValueError, match="Expected exactly three fields."):
        parse_measurement("Berlin;12:30;18;extra")


def test_parse_measurement_empty_line():
    with pytest.raises(ValueError, match="Expected exactly three fields."):
        parse_measurement("")


def test_parse_measurement_whitespace_only_city():
    with pytest.raises(ValueError, match="City must not be empty."):
        parse_measurement("   ;12:30;18")


def test_parse_measurement_temperature_empty():
    with pytest.raises(ValueError, match="Temperature must be numeric."):
        parse_measurement("Berlin;12:30;")


def test_parse_measurement_temperature_whitespace():
    with pytest.raises(ValueError, match="Temperature must be numeric."):
        parse_measurement("Berlin;12:30;   ")


def test_parse_measurement_temperature_with_whitespace():
    assert parse_measurement("Berlin;12:30; 18.5 ") == (
        "Berlin", 750, 18.5
    )


def test_filter_by_temperature_includes_both_boundaries():
    measurements = [
        ("Berlin", 600, 10.0),
        ("Hamburg", 660, 15.0),
        ("Munich", 720, 20.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 20.0) == measurements


def test_filter_by_temperature_equal_bounds():
    measurements = [
        ("Berlin", 600, 10.0),
        ("Hamburg", 660, 15.0),
        ("Munich", 720, 10.0),
    ]

    assert filter_by_temperature(measurements, 10.0, 10.0) == [
        ("Berlin", 600, 10.0),
        ("Munich", 720, 10.0),
    ]


def test_filter_by_temperature_empty_input():
    assert filter_by_temperature([], 0.0, 100.0) == []


def test_filter_by_temperature_no_matches():
    measurements = [
        ("Berlin", 600, -10.0),
        ("Hamburg", 660, 50.0),
    ]

    assert filter_by_temperature(measurements, 0.0, 30.0) == []


def test_filter_by_temperature_negative_range():
    measurements = [
        ("Berlin", 600, -20.0),
        ("Hamburg", 660, -10.0),
        ("Munich", 720, 0.0),
    ]

    assert filter_by_temperature(measurements, -20.0, -10.0) == [
        ("Berlin", 600, -20.0),
        ("Hamburg", 660, -10.0),
    ]


def test_filter_by_temperature_preserves_original_order():
    measurements = [
        ("Munich", 720, 15.0),
        ("Berlin", 600, 12.0),
        ("Hamburg", 660, 18.0),
    ]

    assert filter_by_temperature(measurements, 12.0, 18.0) == measurements


def test_average_temperature_ignores_other_cities():
    measurements = [
        ("Berlin", 600, 10.0),
        ("Hamburg", 660, 100.0),
        ("Berlin", 720, 20.0),
        ("Munich", 780, 200.0),
    ]

    assert average_temperature(measurements, "Berlin") == 15.0


def test_average_temperature_single_measurement():
    measurements = [
        ("Berlin", 600, 17.5),
        ("Hamburg", 660, 30.0),
    ]

    assert average_temperature(measurements, "Berlin") == 17.5


def test_average_temperature_negative_values():
    measurements = [
        ("Berlin", 600, -10.0),
        ("Berlin", 720, -20.0),
    ]

    assert average_temperature(measurements, "Berlin") == -15.0


def test_average_temperature_zero_result():
    measurements = [
        ("Berlin", 600, -10.0),
        ("Berlin", 720, 10.0),
    ]

    assert average_temperature(measurements, "Berlin") == 0.0


def test_average_temperature_empty_input():
    with pytest.raises(ValueError, match="No measurements found for city."):
        average_temperature([], "Berlin")


def test_average_temperature_missing_city():
    measurements = [
        ("Berlin", 600, 10.0),
        ("Hamburg", 660, 20.0),
    ]

    with pytest.raises(ValueError, match="No measurements found for city."):
        average_temperature(measurements, "Munich")


def test_average_temperature_city_matching_is_exact():
    measurements = [
        ("Berlin", 600, 10.0),
        ("berlin", 660, 30.0),
    ]

    assert average_temperature(measurements, "Berlin") == 10.0


def test_hottest_measurement_empty_list():
    with pytest.raises(ValueError, match="No measurements available."):
        hottest_measurement([])


def test_hottest_measurement_single_item():
    measurements = [("Berlin", 600, 25.0)]

    assert hottest_measurement(measurements) == measurements[0]


def test_hottest_measurement_maximum_at_start():
    measurements = [
        ("Berlin", 600, 35.0),
        ("Hamburg", 660, 20.0),
        ("Munich", 720, 15.0),
    ]

    assert hottest_measurement(measurements) == measurements[0]


def test_hottest_measurement_maximum_at_end():
    measurements = [
        ("Berlin", 600, 15.0),
        ("Hamburg", 660, 20.0),
        ("Munich", 720, 35.0),
    ]

    assert hottest_measurement(measurements) == measurements[2]


def test_hottest_measurement_all_equal_temperatures():
    measurements = [
        ("Berlin", 600, 25.0),
        ("Hamburg", 660, 25.0),
        ("Munich", 720, 25.0),
    ]

    assert hottest_measurement(measurements) == measurements[0]


def test_hottest_measurement_tie_chooses_earliest_time():
    measurements = [
        ("Berlin", 900, 30.0),
        ("Hamburg", 600, 30.0),
        ("Munich", 720, 25.0),
    ]

    assert hottest_measurement(measurements) == measurements[1]


def test_hottest_measurement_tie_earliest_time_not_first():
    measurements = [
        ("Berlin", 900, 30.0),
        ("Hamburg", 720, 25.0),
        ("Munich", 600, 30.0),
        ("Bonn", 840, 30.0),
    ]

    assert hottest_measurement(measurements) == measurements[2]


def test_hottest_measurement_negative_temperatures():
    measurements = [
        ("Berlin", 600, -10.0),
        ("Hamburg", 660, -5.0),
        ("Munich", 720, -20.0),
    ]

    assert hottest_measurement(measurements) == measurements[1]


def test_hottest_measurement_does_not_modify_input():
    measurements = [
        ("Berlin", 900, 30.0),
        ("Hamburg", 600, 35.0),
        ("Munich", 720, 25.0),
    ]
    original = measurements.copy()

    hottest_measurement(measurements)

    assert measurements == original