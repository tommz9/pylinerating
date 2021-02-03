import numpy as np


def wind_direction_correction_stranded(angle_of_attack):
    correction_low = 0.42 + 0.68 * np.sin(angle_of_attack / 180 * np.pi) ** 1.08
    correction_high = 0.42 + 0.58 * np.sin(angle_of_attack / 180 * np.pi) ** 0.90

    correction = np.where(angle_of_attack <= 24, correction_low, correction_high)

    return correction


def nusselt_smooth_conductor(reynolds_number, angle_of_attack):
    re = reynolds_number

    conditions = [re < 5000, (5000 <= re) & (re < 50000), (50000 <= re) & (re < 200000)]

    B_options = [0.583, 0.148, 0.0208]
    n_options = [0.471, 0.633, 0.814]

    B = np.select(conditions, B_options)
    n = np.select(conditions, n_options)

    wind_direction_correction = (
        np.sin(angle_of_attack / 180 * np.pi) ** 2
        + 0.0169 * np.cos(angle_of_attack / 180 * np.pi) ** 2
    ) ** 0.225

    return B * re ** n * wind_direction_correction


def nusselt_stranded_small_Rs_conductor(reynolds_number, angle_of_attack):
    re = reynolds_number

    conditions = [re < 2650, (2650 <= re) & (re < 50000), (50000 <= re) & (re < 200000)]

    B_options = [0.641, 0.178, 0.0208]
    n_options = [0.471, 0.633, 0.814]

    B = np.select(conditions, B_options)
    n = np.select(conditions, n_options)

    wind_direction_correction = wind_direction_correction_stranded(angle_of_attack)

    return B * re ** n * wind_direction_correction


def nusselt_stranded_high_Rs_conductor(reynolds_number, angle_of_attack):
    re = reynolds_number

    conditions = [re < 2650, (2650 <= re) & (re < 50000), (50000 <= re) & (re < 200000)]

    B_options = [0.641, 0.048, 0.0208]
    n_options = [0.471, 0.800, 0.814]

    B = np.select(conditions, B_options)
    n = np.select(conditions, n_options)

    wind_direction_correction = wind_direction_correction_stranded(angle_of_attack)

    nusselt = B * re ** n * wind_direction_correction

    return nusselt


def get_nusselt_function(conductor=None, stranded=None, high_rs=None):
    """Returns the appropriate function based on if the conductor is stranded, smooth and has high rs.

    Page 25 and 26.
    """

    if conductor:
        stranded = conductor.stranded
        high_rs = conductor.high_rs

    nusselt_functions = {
        (True, False): nusselt_stranded_small_Rs_conductor,
        (True, True): nusselt_stranded_high_Rs_conductor,
        (False, False): nusselt_smooth_conductor,
        (False, True): nusselt_smooth_conductor,
    }

    return nusselt_functions[(stranded, high_rs)]
