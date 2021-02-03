from collections import namedtuple
from . import nusselt

ConductorConstants = namedtuple(
    "ConductorConstants",
    [
        "stranded",
        "high_rs",
        "diameter",
        "cross_section",
        "absortivity",
        "emmisivity",
        "materials_heat",
        "resistance",
    ],
)

HeatMaterial = namedtuple(
    "HeatMaterial", ["name", "mass_per_unit_length", "specific_heat_20deg", "beta"]
)


def drake_resistance(conductor_temperature):
    at_25 = 7.283e-5
    at_75 = 8.688e-5

    per_1 = (at_75 - at_25) / (75 - 25)

    resistance = at_25 + (conductor_temperature - 25) * per_1
    return resistance


# From CIGRE601 examples
drake_constants = ConductorConstants(
    stranded=True,
    high_rs=True,
    diameter=28.1e-3,
    cross_section=None,
    absortivity=0.8,
    emmisivity=0.8,
    materials_heat=[
        HeatMaterial("steel", 0.5119, 481, 1.00e-4),
        HeatMaterial("aluminum", 1.116, 897, 3.80e-4),
    ],
    resistance=drake_resistance,
)

drake_constants_ieee738 = ConductorConstants(
    stranded=True,
    high_rs=True,
    diameter=28.14e-3,
    cross_section=None,
    absortivity=0.8,
    emmisivity=0.8,
    materials_heat=[
        HeatMaterial("steel", 0.5119, 481, 1.00e-4),
        HeatMaterial("aluminum", 1.116, 897, 3.80e-4),
    ],
    resistance=drake_resistance,
)

drake_constants_example_b = ConductorConstants(
    stranded=True,
    high_rs=True,
    diameter=28.1e-3,
    cross_section=None,
    absortivity=0.9,
    emmisivity=0.9,
    materials_heat=[
        HeatMaterial("steel", 0.5119, 481, 1.00e-4),
        HeatMaterial("aluminum", 1.116, 897, 3.80e-4),
    ],
    resistance=drake_resistance,
)
