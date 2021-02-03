from numpy.lib.function_base import angle
from pylinerating import cigre601, conductor, nusselt
import numpy as np
import pytest


def test_does_not_crash():
    wind_speed = np.array([0, 2, 5, 10])
    wind_direction = np.array([0, 91, 181, 359])
    ambient_temperature = np.array([5, 5, 5, 5])
    solar_irradiation = np.array([0, 400, 600, 1100])

    rating = cigre601.thermal_rating(
        ambient_temperature,
        wind_speed,
        wind_direction,
        solar_irradiation,
        conductor.drake_constants,
    )


def test_thermal_conductivity_of_air():
    ambient_temperature = 40
    conductor_temperature = 100

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    c = cigre601.thermal_conductivity_of_air(tf)
    assert c == pytest.approx(0.0286, abs=0.0001)

    ambient_temperature = 20

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    c = cigre601.thermal_conductivity_of_air(tf)
    assert c == pytest.approx(0.0279, abs=0.0001)


def test_dynamic_viscosity():
    ambient_temperature = 40
    conductor_temperature = 100

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    v = cigre601.dynamic_viscosity(tf)
    assert v == pytest.approx(20.384e-6, abs=0.001e-6)

    ambient_temperature = 20

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    v = cigre601.dynamic_viscosity(tf)
    assert v == pytest.approx(1.9947e-5, abs=0.0001e-5)


def test_reynolds_number():

    ambient_temperature = 40
    conductor_temperature = 100
    wind_speed = 0.61
    elevation = 0

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    Re = cigre601.reynolds_number(wind_speed, conductor.drake_constants, tf, elevation)

    assert Re == pytest.approx(865, abs=0.5)

    ambient_temperature = 20
    wind_speed = 1.66
    elevation = 500

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    Re = cigre601.reynolds_number(wind_speed, conductor.drake_constants, tf, elevation)

    assert Re == pytest.approx(2335, abs=0.5)


def test_nusselt_number():

    ambient_temperature = 40
    conductor_temperature = 100
    wind_speed = 0.61
    angle_of_attack = 60
    elevation = 0

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    Re = cigre601.reynolds_number(wind_speed, conductor.drake_constants, tf, elevation)

    Nu = cigre601.nusselt_number = nusselt.get_nusselt_function(
        conductor.drake_constants
    )(Re, 90)

    assert Nu == pytest.approx(15.495, abs=0.001)

    Nu = cigre601.nusselt_number = nusselt.get_nusselt_function(
        conductor.drake_constants
    )(Re, angle_of_attack)

    assert Nu == pytest.approx(14.40, abs=0.01)

    ambient_temperature = 20
    wind_speed = 1.66
    angle_of_attack = 80
    elevation = 500

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    Re = cigre601.reynolds_number(wind_speed, conductor.drake_constants, tf, elevation)

    Nu = cigre601.nusselt_number = nusselt.get_nusselt_function(
        conductor.drake_constants
    )(Re, 90)

    assert Nu == pytest.approx(24.73, abs=0.01)

    Nu = cigre601.nusselt_number = nusselt.get_nusselt_function(
        conductor.drake_constants
    )(Re, angle_of_attack)

    assert Nu == pytest.approx(24.53, abs=0.01)


def test_forced_convection():

    ambient_temperature = 40
    conductor_temperature = 100
    wind_speed = 0.61
    angle_of_attack = 60
    elevation = 0

    forced = cigre601.forced_convection(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        conductor.drake_constants,
        conductor_temperature,
        elevation,
    )

    assert forced == pytest.approx(77.6, abs=0.1)

    ambient_temperature = 20
    wind_speed = 1.66
    angle_of_attack = 80
    elevation = 500

    forced = cigre601.forced_convection(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        conductor.drake_constants_example_b,
        conductor_temperature,
        elevation,
    )

    assert forced == pytest.approx(172.1, abs=0.1)


def test_grashof():

    ambient_temperature = 40
    conductor_temperature = 100
    elevation = 0

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    gr = cigre601.grashof(
        conductor.drake_constants,
        conductor_temperature,
        ambient_temperature,
        tf,
        elevation,
    )

    assert gr == pytest.approx(96.95e3, abs=0.01e3)

    ambient_temperature = 20
    elevation = 500

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    gr = cigre601.grashof(
        conductor.drake_constants_example_b,
        conductor_temperature,
        ambient_temperature,
        tf,
        elevation,
    )

    assert gr == pytest.approx(131e3, abs=0.1e3)


def test_prandtl():

    ambient_temperature = 40
    conductor_temperature = 100

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    pr = cigre601.prandtl(conductor.drake_constants, conductor_temperature, tf)

    assert pr == pytest.approx(0.716, abs=0.001)

    ambient_temperature = 20
    conductor_temperature = 100

    tf = cigre601.temperature_film(conductor_temperature, ambient_temperature)
    pr = cigre601.prandtl(conductor.drake_constants, conductor_temperature, tf)

    assert pr == pytest.approx(0.718, abs=0.001)


# def test_specific_heat():
#     conductor_temperature = 100
#     heat = cigre601.specific_heat(conductor.drake_constants, conductor_temperature)
#     assert heat == pytest.approx(1005, abs=1)


def test_natural_convection():
    ambient_temperature = 40
    conductor_temperature = 100
    horizontal_angle = 0
    elevation = 0

    natural = cigre601.natural_convection(
        ambient_temperature,
        conductor.drake_constants,
        conductor_temperature,
        horizontal_angle,
        elevation,
    )

    assert natural == pytest.approx(42.0, abs=0.1)

    ambient_temperature = 20
    conductor_temperature = 100
    horizontal_angle = 10
    elevation = 500

    natural = cigre601.natural_convection(
        ambient_temperature,
        conductor.drake_constants_example_b,
        conductor_temperature,
        horizontal_angle,
        elevation,
    )

    assert natural == pytest.approx(58.9, abs=0.1)


def test_radiative_heat_loss():

    ambient_temperature = 40
    conductor_temperature = 100

    heat_loss = cigre601.power_radiation(
        ambient_temperature, conductor.drake_constants, conductor_temperature
    )

    assert heat_loss == pytest.approx(39.1, abs=0.1)

    ambient_temperature = 20
    conductor_temperature = 100

    heat_loss = cigre601.power_radiation(
        ambient_temperature, conductor.drake_constants_example_b, conductor_temperature
    )

    assert heat_loss == pytest.approx(54, abs=0.1)


def test_solar_heat_gain():
    solar_irradiation = 1210.0
    Ps = cigre601.power_solar(solar_irradiation, conductor.drake_constants)
    assert Ps == pytest.approx(27.2, abs=0.1)

    solar_irradiation = 540.6
    Ps = cigre601.power_solar(solar_irradiation, conductor.drake_constants_example_b)
    assert Ps == pytest.approx(13.7, abs=0.1)


def test_cigre601_steady_state_example_A():
    wind_speed = np.array([0.61])
    angle_of_attack = np.array([60.0])
    ambient_temperature = np.array([40.0])
    solar_irradiation = np.array([1210])
    horizontal_angle = np.array([0])
    elevation = np.array([0])

    conductor_constants = conductor.drake_constants

    rating = cigre601.thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor_constants,
        horizontal_angle=horizontal_angle,
        conductor_temperature=100,
        elevation=elevation,
    )

    assert len(rating) == 1

    assert pytest.approx([976], abs=0.5) == rating


def test_cigre601_steady_state_example_B():
    wind_speed = np.array([1.66])
    angle_of_attack = np.array([80.0])
    ambient_temperature = np.array([20.0])
    solar_irradiation = np.array([540.6])
    horizontal_angle = np.array([10.0])
    elevation = np.array([500])

    conductor_constants = conductor.drake_constants_example_b

    rating = cigre601.thermal_rating(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        solar_irradiation,
        conductor_constants,
        horizontal_angle=horizontal_angle,
        conductor_temperature=100,
        elevation=elevation,
    )

    assert len(rating) == 1

    assert pytest.approx([1504], abs=0.5) == rating


def test_angle():
    ambient_temperature = np.array([40.0])
    wind_speed = np.array([5.0])
    solar_irradiation = np.array([1000])
    conductor_temperature = np.array([100.0])
    horizontal_angle = np.array([0])
    elevation = np.array([0.0])

    angles = np.array([0, 45, 89, 90, 91, 135, 180, 15, -15])

    A = cigre601.thermal_rating(
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
