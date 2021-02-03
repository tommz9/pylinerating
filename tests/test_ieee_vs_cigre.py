import pytest
import numpy as np

from pylinerating import ieee738, cigre601, conductor


def test_point1():

    ambient_temperature = 40.0
    wind_speed = 0.61
    angle_of_attack = 90
    solar_irradiation = 1000
    conductor_temperature = 85.0
    horizontal_angle = 0
    elevation = 0.0

    ieee = ieee738.thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor.drake_constants,
        conductor_temperature,
        horizontal_angle,
        elevation,
    )
    cigre = cigre601.thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor.drake_constants,
        conductor_temperature,
        horizontal_angle,
        elevation=elevation,
    )

    assert ieee == pytest.approx(cigre, rel=0.05)


def test_point2():

    ambient_temperature = 20
    wind_speed = 1.66
    angle_of_attack = 90
    solar_irradiation = 0
    conductor_temperature = 85.0
    horizontal_angle = 10
    elevation = 500

    ieee = ieee738.thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor.drake_constants,
        conductor_temperature,
        horizontal_angle,
        elevation,
    )
    cigre = cigre601.thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor.drake_constants,
        conductor_temperature,
        horizontal_angle,
        elevation=elevation,
    )

    assert ieee == pytest.approx(cigre, rel=0.05)
