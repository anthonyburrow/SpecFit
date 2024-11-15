import numpy as np

from ..util.physics import wiens


default_params = {}


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


default_params['T_planck'] = default_T_planck
default_params['a_planck'] = default_a_planck


# Free-free
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


default_params['T_ff'] = default_T_ff
default_params['a_ff'] = default_a_ff


# Gaussian
def default_mean_gaussian(data: np.ndarray, *args, **kwargs) -> dict:
    wave = data[:, 0]

    param_info = {
        'value': (wave[-1] - wave[0]) * 0.5,
        'min': wave[0],
        'max': wave[-1],
    }

    return param_info


def default_std_gaussian(data: np.ndarray, *args, **kwargs) -> dict:
    wave = data[:, 0]

    param_info = {
        'value': 20.,
        'min': 0.,
        'max': wave[-1] - wave[0],
    }

    return param_info


def default_a_gaussian(data: np.ndarray, *args, **kwargs) -> dict:
    param_info = {
        'value': 0.,
    }

    return param_info


default_params['mean_gaussian'] = default_mean_gaussian
default_params['std_gaussian'] = default_std_gaussian
default_params['a_gaussian'] = default_a_gaussian


# Lorentzian
def default_mean_lorentzian(data: np.ndarray, *args, **kwargs) -> dict:
    wave = data[:, 0]

    param_info = {
        'value': (wave[-1] - wave[0]) * 0.5,
        'min': wave[0],
        'max': wave[-1],
    }

    return param_info


def default_fwhm_lorentzian(data: np.ndarray, *args, **kwargs) -> dict:
    wave = data[:, 0]

    param_info = {
        'value': 40.,
        'min': 0.,
        'max': wave[-1] - wave[0],
    }

    return param_info


def default_a_lorentzian(data: np.ndarray, *args, **kwargs) -> dict:
    param_info = {
        'value': 0.,
    }

    return param_info


default_params['mean_gaussian'] = default_mean_gaussian
default_params['std_gaussian'] = default_std_gaussian
default_params['a_gaussian'] = default_a_gaussian
