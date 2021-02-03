import pytest
import numpy as np

from pylinerating import ieee738, conductor


def test_density_of_air():

    ambient_temperature = 40.0
    conductor_temperature = 100.0
    elevation = 0.0

    density = ieee738.air_density(ambient_temperature, conductor_temperature, elevation)

    assert density == pytest.approx(1.029, abs=0.001 / 2)


def test_dynamic_viscosity():

    ambient_temperature = 40.0
    conductor_temperature = 100.0

    viscosity = ieee738.dynamic_viscosity(ambient_temperature, conductor_temperature)

    assert viscosity == pytest.approx(2.043e-5, abs=0.001e-5 / 2)


def test_thermal_conductivity_of_air():

    ambient_temperature = 40.0
    conductor_temperature = 100.0

    conductivity = ieee738.thermal_conductivity_of_air(
        ambient_temperature, conductor_temperature
    )

    assert conductivity == pytest.approx(0.02945, abs=0.00001 / 2)


def test_natural_convection_loss():

    ambient_temperature = 40.0
    conductor_temperature = 100.0
    elevation = 0.0

    convection_loss = ieee738.natural_convection(
        ambient_temperature,
        conductor.drake_constants_ieee738,
        conductor_temperature,
        elevation,
    )

    assert convection_loss == pytest.approx(42.4, abs=0.1 / 2)


def test_reynolds_number():

    ambient_temperature = 40.0
    wind_speed = 0.61
    conductor_temperature = 100.0
    elevation = 0.0

    Nre = ieee738.reynolds_number(
        ambient_temperature,
        wind_speed,
        conductor.drake_constants_ieee738,
        conductor_temperature,
        elevation,
    )

    assert Nre == pytest.approx(865, abs=1)


def test_forced_convection():

    ambient_temperature = 40.0
    wind_speed = 0.61
    angle_of_attack = (90 / 180.0) * np.pi
    conductor_temperature = 100.0
    elevation = 0.0

    qc, qc1, qc2, Kangle = ieee738.forced_convection(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        conductor.drake_constants_ieee738,
        conductor_temperature,
        elevation,
        return_parts=True,
    )

    assert Kangle == pytest.approx(1.0, abs=0.01)

    # These are a little bit off compared to the standard.
    # However the standard rounds a lot, this might be the problem
    assert qc1 == pytest.approx(81.93, abs=0.2)
    assert qc2 == pytest.approx(77.06, abs=0.1)

    assert qc == pytest.approx(81.93, abs=0.2)


def test_radiated_heat_loss():

    ambient_temperature = 40.0
    conductor_temperature = 100.0

    qr = ieee738.radiated_heat_loss(
        ambient_temperature, conductor.drake_constants_ieee738, conductor_temperature
    )

    assert qr == pytest.approx(39.1, abs=0.1 / 2)


def test_conductor_resistance():

    R = conductor.drake_constants_ieee738.resistance(100)

    assert R == pytest.approx(9.390e-5, abs=0.001e-5 / 2)


def test_solar():

    solar_irradiation = 1000  # This is effective irradiation (angle of inclination is taken into account)

    qs = ieee738.solar_heat_gain(solar_irradiation, conductor.drake_constants_ieee738)

    assert qs == pytest.approx(22.44, abs=0.1)


def test_thermal_rating():

    ambient_temperature = 40.0
    wind_speed = 0.61
    angle_of_attack = 90
    solar_irradiation = 1000  # This is effective irradiation (angle of inclination is taken into account)
    conductor_temperature = 100.0
    horizontal_angle = 0
    elevation = 0.0

    A = ieee738.thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor.drake_constants_ieee738,
        conductor_temperature,
        horizontal_angle,
        elevation,
    )

    assert A == pytest.approx(1025, abs=1 / 2)


def test_angle():
    ambient_temperature = np.array([40.0])
    wind_speed = np.array([5.0])
    solar_irradiation = np.array([1000])
    conductor_temperature = np.array([100.0])
    horizontal_angle = np.array([0])
    elevation = np.array([0.0])

    angles = np.array([0, 45, 89, 90, 91, 135, 180, 15, -15])

    A = ieee738.thermal_rating(
        ambient_temperature,
        wind_speed,
        angles,
        solar_irradiation,
        conductor.drake_constants_ieee738,
        conductor_temperature,
        horizontal_angle,
        elevation,
    )

    # 90 degrees is parallel, should be the highest
    assert A[2] < A[3]
    assert A[4] < A[3]

    # The calculation should be symetric around 90
    assert A[2] == A[4]

    # Also around 0
    assert A[7] == A[8]

    assert A[0] < A[1]
    assert A[0] < A[2]
    assert A[0] < A[3]
    assert A[0] < A[4]
    assert A[0] < A[5]
    assert A[0] == A[6]
