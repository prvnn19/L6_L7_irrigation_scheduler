import pytest

from irrigation_scheduler import schedule, should_irrigate, water_volume


def test_irrigation_rejections_and_stage_thresholds():
    assert should_irrigate(60, 0, "seedling") is False
    assert should_irrigate(20, 10, "seedling") is False
    assert should_irrigate(44, 0, "seedling") is True
    assert should_irrigate(45, 0, "seedling") is False
    assert should_irrigate(54, 0, "flowering") is True
    assert should_irrigate(55, 0, "flowering") is False


def test_irrigation_for_other_stages():
    assert should_irrigate(30, 5, "mature") is False
    assert should_irrigate(39, 0, "mature") is True
    assert should_irrigate(40, 0, "mature") is False


def test_water_volume_validation_stages_and_temperatures():
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)

    assert water_volume(10, "seedling", 20) == 20
    assert water_volume(2, "flowering", 36) == 15
    assert water_volume(2, "mature", 9) == 4
    assert water_volume(2, "mature", 10) == 8


def test_schedule_skip_add_and_budget_stop():
    zones = [
        ("wet", 1, 60, 0, "seedling", 20),
        ("first", 1, 20, 0, "seedling", 20),
        ("over-budget", 1, 20, 0, "flowering", 20),
    ]

    assert schedule(zones, 2) == ["first"]
    assert schedule([], 2) == []
    assert schedule([("first", 1, 20, 0, "seedling", 20)], 2) == ["first"]
