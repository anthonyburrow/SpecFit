import numpy as np

from .constants import h, c, k_B


def planck_freq(
    nu: float | np.ndarray,
    T: float,
    a: float = 1.,
) -> float | np.ndarray:
    """Planck function as a function of wavelength.

    Parameters
    ----------
    nu : float or np.ndarray
        Frequency given in Hz.
    T : float
        Blackbody temperature.
    a : float

    Returns
    -------
    planck : float or np.ndarray
        Output of Planck function (in per Hz).
    """
    exp = np.exp(-h * nu / (k_B * T))
    planck = a * (2. * h * nu**3 / c**2) * exp / (1. - exp)

    # Remove negative output
    if isinstance(planck, float):
        if planck < 0.:
            return 0.
    elif isinstance(planck, np.ndarray):
        mask = planck < 0.
        planck[mask] = 0.

    return planck


def planck_wave(
    wave: float | np.ndarray,
    T: float,
    a: float = 1.,
) -> float | np.ndarray:
    """Planck function as a function of wavelength.

    Parameters
    ----------
    wave : float or np.ndarray
        Wavelength given in Angstroms.
    T : float
        Blackbody temperature.
    a : float

    Returns
    -------
    planck : float or np.ndarray
        Output of Planck function (in per Angstrom).
    """
    wave_cm = wave * 1.e-8

    exp = np.exp(-h * c / (wave_cm * k_B * T))
    planck = a * (2. * h * c**2 / wave_cm**5) * exp / (1. - exp)
    planck *= 1.e-8

    # Remove negative output
    if isinstance(planck, float):
        if planck < 0.:
            return 0.
    elif isinstance(planck, np.ndarray):
        mask = planck < 0.
        planck[mask] = 0.

    return planck


def planck(*args, variable='wavelength', **kwargs) -> float | np.ndarray:
    if variable == 'wavelength':
        return planck_wave(*args, **kwargs)
    if variable == 'frequency':
        return planck_freq(*args, **kwargs)
