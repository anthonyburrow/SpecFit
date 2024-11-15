import numpy as np
import matplotlib.pyplot as plt

from SpectrumCore.plot import setup_plot

from SpecFitModels import lorentzian, planck


def test_lorentzian(wave_optical):
    mean = wave_optical.mean()
    fwhm = 100.

    lorentzian(wave_optical, mean_lorentzian=mean, fwhm_lorentzian=fwhm)


def test_plot_lorentzian(output_dir):
    fig, ax = plt.subplots(dpi=135)

    features = np.array([
        [7000., 100., 1.],
        [7050., 200., 0.5],
        [7025., 50., 2.],
    ])

    for feat_params in features:
        mean, fwhm, a = feat_params
        wave_feat = np.linspace(mean - 2. * fwhm, mean + 2. * fwhm)

        feature = lorentzian(wave_feat, mean, fwhm, a)
        ax.plot(wave_feat, feature)

    fn = f'{output_dir}/lorentzian.png'
    fig.savefig(fn)

    plt.close('all')


def test_plot_lorentzian_feature(output_dir, wave_optical, T_representative):
    fig, ax = setup_plot(plot_type='optical')

    wave = wave_optical.copy()

    features = np.array([
        [4000., 100., -0.1],
        [5000., 200., -0.05],
        [7000., 50., -0.1],
    ])

    for feat_params in features:
        mean, fwhm, _ = feat_params
        wave_feat = np.linspace(mean - 2. * fwhm, mean + 2. * fwhm)
        wave = np.concatenate((wave, wave_feat), axis=0)

    wave.sort()

    flux = planck(wave, T_planck=T_representative)
    flux /= flux.max()

    for feat_params in features:
        feature = lorentzian(wave, *feat_params)
        flux += feature

    ax.plot(wave, flux)

    fn = f'{output_dir}/lorentzian_feature.png'
    fig.savefig(fn)
