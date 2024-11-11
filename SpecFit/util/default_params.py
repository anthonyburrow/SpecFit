import numpy as np

from ..util.physics import wiens


def default_T_planck(data: np.ndarray, *args, **kwargs) -> dict:
    wave = data[data[:, 1].argmax(), 0]
    T = wiens(wave)

    param_info = {
        'value': T,
        'min': 3000.,
        'max': 20000.,
    }

    return param_info


def default_a_planck(data: np.ndarray, *args, **kwargs) -> dict:
    param_info = {
        'value': data[:, 1].max(),
        'min': 0.,
    }

    return param_info


def default_T_ff(data: np.ndarray, *args, **kwargs) -> dict:
    wave = data[data[:, 1].argmax(), 0]
    T = wiens(wave)

    param_info = {
        'value': T,
        'min': 0.,
        'max': 20000.,
    }

    return param_info


def default_a_ff(data: np.ndarray, *args, **kwargs) -> dict:
    param_info = {
        'value': data[:, 1].max(),
        'min': 0.,
    }

    return param_info


default_params = {
    'T_planck': default_T_planck,
    'a_planck': default_a_planck,
    'T_ff': default_T_ff,
    'a_ff': default_a_ff,
}
