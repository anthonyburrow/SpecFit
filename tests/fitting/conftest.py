import pytest
import numpy as np

from SpecFitModels import planck, gaussian


@pytest.fixture(scope='session')
def feature_params():
    features = np.array([
        [5000., 15., -0.03],
        [6000., 15., -0.03],
        [7000., 15., -0.03],
    ])
    return features


@pytest.fixture(scope='session')
def spectrum_optical(wave_optical, T_representative, feature_params):
    wave = wave_optical.copy()

    for feature_param in feature_params:
        mean, std, a = feature_param
        wave_feat = np.linspace(mean - 3. * std, mean + 3. * std)
        wave = np.concatenate((wave, wave_feat), axis=0)
    wave.sort()

    flux = planck(wave, T_planck=T_representative)
    flux /= flux.max()

    for feature_param in feature_params:
        feature = gaussian(wave, *feature_param)
        flux += feature

    flux_err = flux * np.random.normal(0.05, 0.01, size=len(flux))

    return np.c_[wave, flux, flux_err]


@pytest.fixture(scope='session')
def spectrum_NIR(wave_NIR, T_representative, feature_params):
    wave = wave_NIR.copy()

    for feature_param in feature_params:
        mean, std, a = feature_param
        wave_feat = np.linspace(mean - 3. * std, mean + 3. * std)
        wave = np.concatenate((wave, wave_feat), axis=0)
    wave.sort()

    flux = planck(wave, T_planck=T_representative)
    flux /= flux.max()

    for feature_param in feature_params:
        feature = gaussian(wave, *feature_param)
        flux += feature

    flux_err = flux * np.random.normal(0.05, 0.01, size=len(flux))

    return np.c_[wave * 1e-4, flux, flux_err]
