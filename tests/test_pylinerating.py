import pytest

from pylinerating import __version__, thermal_rating, conductor

from pylinerating import ieee738, cigre601


def test_invalid_standard():
    with pytest.raises(ValueError):
        thermal_rating(standard="something")


def test_valid_standard():
    # Should raise type error because there will be arguments missing

    with pytest.raises(TypeError):
        thermal_rating(standard="cigre")

    with pytest.raises(TypeError):
        thermal_rating(standard="ieee")


def test_switching_ieee():

    ambient_temperature = 40.0
    wind_speed = 0.61
    angle_of_attack = 90
    solar_irradiation = 1000
    conductor_temperature = 85.0
    horizontal_angle = 0
    elevation = 0.0

    ieee1 = thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor.drake_constants,
        conductor_temperature,
        horizontal_angle,
        elevation,
        standard="ieee",
    )

    ieee2 = ieee738.thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor.drake_constants,
        conductor_temperature,
        horizontal_angle,
        elevation=elevation,
    )

    assert ieee1 == ieee2


def test_switching_cigre():

    ambient_temperature = 40.0
    wind_speed = 0.61
    angle_of_attack = 90
    solar_irradiation = 1000
    conductor_temperature = 85.0
    horizontal_angle = 0
    elevation = 0.0

    cigre1 = thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor.drake_constants,
        conductor_temperature,
        horizontal_angle,
        elevation,
        standard="cigre",
    )

    cigre2 = cigre601.thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor.drake_constants,
        conductor_temperature,
        horizontal_angle,
        elevation=elevation,
    )

    assert cigre1 == cigre2
