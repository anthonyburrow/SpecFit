import numpy as np

from SpecFitModels import planck, ff
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
    # gaunt_params: dict,
    # gaunt_table: np.ndarray,
) -> np.ndarray:
    return ff(wave, T_ff, a_ff, GAUNT_PARAMS, GAUNT_TABLE)


model_from_key = {
    # Planck function
    'planck': planck_wrapper,
    'bb': planck_wrapper,
    # Free-free emission
    'free_free': ff_wrapper,
    'ff': ff_wrapper,
}
