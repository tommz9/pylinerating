# Line rating calculation for Python

This package contains functions to calculate the rating according to IEEE-738 or CIGRE-601.

What is implemented?

- Steady state calculation of rating (ampacity) 

What is missing

- Dynamic calculation
- Line temperature calculation

## Installation

1. Clone the repository
2. Make a virtual environment
3. cd to the downloaded repository
4. install: `pip install .`

## Usage

```python

from pylinerating import thermal_rating,

ambient_temperature = 40.0
wind_speed = 0.61
angle_of_attack = 90
solar_irradiation = 1000
conductor_temperature = 85.0
horizontal_angle = 0
elevation = 0.0

ieee = thermal_rating(
    ambient_temperature,
    wind_speed,
    angle_of_attack,
    solar_irradiation,
    conductor.drake_constants,
    conductor_temperature,
    horizontal_angle,
    elevation,
    standard="ieee"
)

cigre = thermal_rating(
    ambient_temperature,
    wind_speed,
    angle_of_attack,
    solar_irradiation,
    conductor.drake_constants,
    conductor_temperature,
    horizontal_angle,
    elevation=elevation,
    standard="cigre"
)
```

The module `pylinerating.conductor` contains conductor definition from the example in the standard.
