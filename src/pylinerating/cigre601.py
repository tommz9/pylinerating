import numpy as np
from . import nusselt


def horizontal_correction(conductor, angle):
    """Equation 24, page 28"""
    if conductor.stranded:
        return 1 - 1.76e-6 * angle ** 2.5
    else:
        return 1 - 1.58e-4 * angle ** 1.5


def specific_heat(conductor, temperature):
    total_mass = 0.0
    total_heat = 0.0

    for metal in conductor.materials_heat:
        c = metal.specific_heat_20deg
        m = metal.mass_per_unit_length
        beta = metal.beta

        c_modified = c * (1 + beta * (temperature - 20.0))

        total_mass += m
        total_heat += m * c_modified

    return total_heat / total_mass


def temperature_film(conductor_temperature, ambient_temperature):
    return 0.5 * (conductor_temperature + ambient_temperature)


def thermal_conductivity_of_air(t_f):
    """Section 3.5, eq 18, page 24."""
    return 2.368e-2 + 7.23e-5 * t_f - 2.763e-8 * t_f ** 2


def dynamic_viscosity(t_f):
    """Eq 19, page 25"""
    return (17.239 + 4.635e-2 * t_f - 2.03e-5 * t_f ** 2) * 1e-6


def air_density(t_f, elevation):
    """Eq 20, page 25"""
    return (1.293 - 1.525e-4 * elevation + 6.379e-9 * elevation ** 2) / (
        1 + 0.00367 * t_f
    )


def kinematic_viscosity(t_f, elevation):
    return dynamic_viscosity(t_f) / air_density(t_f, elevation)


def reynolds_number(wind_speed, conductor, t_f, elevation):
    """Page 25, in text."""
    return wind_speed * conductor.diameter / kinematic_viscosity(t_f, elevation)


def forced_convection(
    ambient_temperature,
    wind_speed,
    angle_of_attack,
    conductor,
    conductor_temperature,
    elevation,
):

    t_f = temperature_film(conductor_temperature, ambient_temperature)

    # Page 25, in text
    Re = reynolds_number(wind_speed, conductor, t_f, elevation)

    nusselt_number = nusselt.get_nusselt_function(conductor)(Re, angle_of_attack)

    # Eq 17, page 24
    forced_convection = (
        np.pi
        * thermal_conductivity_of_air(t_f)
        * (conductor_temperature - ambient_temperature)
        * nusselt_number
    )

    return forced_convection


def grashof(conductor, conductor_temperature, ambient_temperature, t_f, elevation):
    return (
        conductor.diameter ** 3
        * (conductor_temperature - ambient_temperature)
        * 9.807
        / ((t_f + 273) * kinematic_viscosity(t_f, elevation) ** 2)
    )


def prandtl(conductor, conductor_temperature, t_f):
    return (
        # TODO: Veruify this assumption
        1005.0  # specific_heat(conductor, conductor_temperature)  # This should be the specific heat of air?, not the metal
        * dynamic_viscosity(t_f)
        / thermal_conductivity_of_air(t_f)
    )


def natural_convection(
    ambient_temperature, conductor, conductor_temperature, horizontal_angle, elevation
):

    t_f = temperature_film(conductor_temperature, ambient_temperature)

    # From List of Symbols on page 7
    gr = grashof(conductor, conductor_temperature, ambient_temperature, t_f, elevation)

    # From List of Symbols on page 7
    pr = prandtl(conductor, conductor_temperature, t_f)

    gp = gr * pr

    condition = [gp < 1e2, gp < 1e4, gp < 1e7, gp < 1e12]

    A_choices = [1.02, 0.850, 0.480, 0.125]
    m_choices = [0.148, 0.188, 0.250, 0.333]

    A = np.select(condition, A_choices)
    m = np.select(condition, m_choices)

    nusselt_number_natural = (
        A * gp ** m * horizontal_correction(conductor, horizontal_angle)
    )

    natural_convection = (
        np.pi
        * thermal_conductivity_of_air(t_f)
        * (conductor_temperature - ambient_temperature)
        * nusselt_number_natural
    )

    return natural_convection


def power_convective(
    ambient_temperature,
    wind_speed,
    angle_of_attack,
    conductor,
    conductor_temperature,
    horizontal_angle,
    elevation,
):
    """Convective cooling is the higher of forced and natural convection.

    Based on text in "Low wind speeds" on page 28.
    """

    forced = forced_convection(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        conductor,
        conductor_temperature,
        elevation,
    )

    natural = natural_convection(
        ambient_temperature,
        conductor,
        conductor_temperature,
        horizontal_angle,
        elevation,
    )

    P = np.maximum(forced, natural)

    return P


def power_radiation(ambient_temperature, conductor, conductor_temperature):
    """Eq 27, page 30"""
    return (
        np.pi
        * conductor.diameter
        * 5.6697e-8  # Stefan-Boltzmann
        * conductor.emmisivity
        * ((conductor_temperature + 273) ** 4 - (ambient_temperature + 273) ** 4)
    )


# def power_joule(self, current):
#    # TODO: Account for Skin Effect
#    return current ** 2 * self.material.resistance(self.temperature)


def power_solar(solar_irradiation, conductor):
    """Section 3.3, Eq 8, page 18."""
    return conductor.absortivity * solar_irradiation * conductor.diameter


def thermal_rating(
    ambient_temperature,
    wind_speed,
    angle_of_attack,
    solar_irradiation,
    conductor,
    conductor_temperature=80.0,
    horizontal_angle=0,
    elevation=500,
):
    """Calculate the rating using CIGRE-601.

    ambient_temperature:   temperature of air in [°C]
    wind_speed:            in [m/s]
    angle_of_attack:       the angle between the wind and the conductor in [°]. 0° is parallel wind, 90° is perpendicular
    solar_irradiation:     in [W/m^2]
    conductor:             the conductor structure with details about the material. from pylinerating.conductor
    conductor_temperature: the target conductor temperature [°C]
    horizontal_angle:      not used
    elevation:             the see level elevation in [m]
    """

    # angle_of_attack = np.where(
    #     angle_of_attack >= 180.0, angle_of_attack - 180, angle_of_attack
    # )

    angle_of_attack = 90 - np.abs((angle_of_attack % 180) - 90)

    Pc = power_convective(
        ambient_temperature,
        wind_speed,
        angle_of_attack,
        conductor,
        conductor_temperature,
        horizontal_angle,
        elevation,
    )
    Pr = power_radiation(ambient_temperature, conductor, conductor_temperature)
    Ps = power_solar(solar_irradiation, conductor)

    current = np.sqrt((Pr + Pc - Ps) / conductor.resistance(conductor_temperature))

    return current
