import numpy as np

from SpecFitModels import planck, ff, gaussian, lorentzian
from ..util.io import read_gaunt_params, read_gaunt_table


GAUNT_PARAMS = read_gaunt_params()
GAUNT_TABLE = read_gaunt_table(GAUNT_PARAMS['N_u'])


def planck_wrapper(
    wave: np.ndarray,
    T_planck: float,
    a_planck: float,
) -> np.ndarray:
    return planck(wave, T_planck, a_planck)


def ff_wrapper(
    wave: np.ndarray,
    T_ff: float,
    a_ff: float,
) -> np.ndarray:
    return ff(wave, T_ff, a_ff, GAUNT_PARAMS, GAUNT_TABLE)


def gaussian_wrapper(
    wave: np.ndarray,
    mean_gaussian: float,
    std_gaussian: float,
    a_gaussian: float,
) -> np.ndarray:
    return gaussian(wave, mean_gaussian, std_gaussian, a_gaussian)


def lorentzian_wrapper(
    wave: np.ndarray,
    mean_lorentzian: float,
    fwhm_lorentzian: float,
    a_lorentzian: float,
) -> np.ndarray:
    return lorentzian(wave, mean_lorentzian, fwhm_lorentzian, a_lorentzian)


model_from_key = {
    # Planck function
    'planck': planck_wrapper,
    'bb': planck_wrapper,
    # Free-free emission
    'free_free': ff_wrapper,
    'ff': ff_wrapper,
    # Gaussian
    'gaussian': gaussian_wrapper,
    'gauss': gaussian_wrapper,
    # Lorentzian
    'lorentzian': lorentzian_wrapper,
    'lorentz': lorentzian_wrapper,
}
