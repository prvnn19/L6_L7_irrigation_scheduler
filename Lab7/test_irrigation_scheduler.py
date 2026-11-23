import math
import string

from hypothesis import given, strategies as st
import pytest

from irrigation_scheduler import moisture_average, parse_zone, water_needed


ZONE_NAMES = st.text(
    alphabet=string.ascii_letters + " _-",
    min_size=1,
    max_size=20,
).filter(lambda name: bool(name.strip()))
FINITE_NONNEGATIVE = st.floats(
    min_value=0,
    max_value=10000,
    allow_nan=False,
    allow_infinity=False,
)
FINITE_POSITIVE = st.floats(
    min_value=0.01,
    max_value=10000,
    allow_nan=False,
    allow_infinity=False,
)


@given(ZONE_NAMES, FINITE_POSITIVE)
def test_parse_zone_valid_input(name, area):
    assert parse_zone("{}:{}".format(name, area)) == (name.strip().title(), area)


@given(st.one_of(st.text(), st.none()))
def test_parse_zone_rejects_or_correctly_parses_fuzzed_input(value):
    try:
        result = parse_zone(value)
    except ValueError:
        return

    assert isinstance(value, str)
    parts = value.split(":")
    assert len(parts) == 2
    name, area_text = parts
    area = float(area_text)
    assert name.strip()
    assert math.isfinite(area) and area > 0
    assert result == (name.strip().title(), area)


@pytest.mark.parametrize(
    "value",
    [None, "", ":10", "north:", "north:0", "north:-1", "north:nan", "north:1:2"],
)
def test_parse_zone_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        parse_zone(value)


@given(st.lists(st.integers(min_value=0, max_value=100), min_size=1, max_size=50))
def test_moisture_average_valid_input(readings):
    csv = ",".join(str(reading) for reading in readings)
    assert moisture_average(csv) == sum(readings) // len(readings)


@given(st.one_of(st.text(), st.none()))
def test_moisture_average_rejects_or_correctly_averages_fuzzed_input(value):
    try:
        result = moisture_average(value)
    except ValueError:
        return

    assert isinstance(value, str)
    readings = [int(token) for token in value.split(",")]
    assert all(0 <= reading <= 100 for reading in readings)
    assert result == sum(readings) // len(readings)


@pytest.mark.parametrize(
    "value",
    [None, "", "1,,2", "1,", "101", "-1", "1.5", "one"],
)
def test_moisture_average_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        moisture_average(value)


@given(FINITE_POSITIVE, FINITE_NONNEGATIVE)
def test_water_needed_valid_input(area, rainfall):
    result = water_needed("{}|{}".format(area, rainfall))
    assert math.isclose(result, max(area * 5 - rainfall, 0))


@given(st.one_of(st.text(), st.none()))
def test_water_needed_rejects_or_correctly_calculates_fuzzed_input(value):
    try:
        result = water_needed(value)
    except ValueError:
        return

    assert isinstance(value, str)
    parts = value.split("|")
    assert len(parts) == 2
    area, rainfall = (float(part) for part in parts)
    assert math.isfinite(area) and area > 0
    assert math.isfinite(rainfall) and rainfall >= 0
    assert math.isclose(result, max(area * 5 - rainfall, 0))


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "|1",
        "1|",
        "0|0",
        "-1|0",
        "1|-1",
        "nan|1",
        "1|inf",
        "1|2|3",
        "1e308|0",
    ],
)
def test_water_needed_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        water_needed(value)
