import numpy as np
from SpecFitModels import planck, ff


def planck_wrapper(
    wave: np.ndarray,
    T_planck: float,
    a_planck: float
) -> np.ndarray:
    return planck(wave, T_planck, a_planck)


def ff_wrapper(
    wave: np.ndarray,
    T_ff: float,
    a_ff: float
) -> np.ndarray:
    return ff(wave, T_ff, a_ff)
