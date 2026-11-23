import pytest

from irrigation_scheduler import schedule, should_irrigate, water_volume


@pytest.mark.parametrize(
    ("moisture", "rain_mm", "stage", "expected"),
    [
        (60, 0, "seedling", False),
        (20, 10, "seedling", False),
        (44, 0, "seedling", True),
        (45, 0, "seedling", False),
        (54, 0, "flowering", True),
        (55, 0, "flowering", False),
        (30, 5, "mature", False),
        (39, 0, "mature", True),
        (40, 0, "mature", False),
    ],
)
def test_should_irrigate_decision_branches(moisture, rain_mm, stage, expected):
    assert should_irrigate(moisture, rain_mm, stage) is expected


def test_water_volume_validation_stage_and_temperature_branches():
    with pytest.raises(ValueError, match="invalid area"):
        water_volume(0, "seedling", 20)

    assert water_volume(1, "seedling", 36) == 3
    assert water_volume(1, "flowering", 9) == 2.5
    assert water_volume(1, "mature", 10) == 4
    assert water_volume(1, "flowering", 20) == 5


def test_schedule_skip_add_budget_stop_and_natural_completion():
    zones = [
        ("wet", 1, 60, 0, "seedling", 20),
        ("within-budget", 1, 20, 0, "seedling", 20),
        ("over-budget", 1, 20, 0, "flowering", 20),
    ]
    assert schedule(zones, 2) == ["within-budget"]

    assert schedule([], 2) == []
    assert schedule(
        [("completed", 1, 20, 0, "seedling", 20)],
        2,
    ) == ["completed"]
