import numpy as np
import matplotlib.pyplot as plt

from SpectrumCore.plot import setup_plot

from SpecFitModels import gaussian, planck


def test_gaussian():
    wave = np.linspace(5000., 7000., 100)
    mean = wave.mean()
    std = 50.

    gaussian(wave, mean_gaussian=mean, std_gaussian=std)


def test_plot_gaussian(output_dir):
    fig, ax = plt.subplots(dpi=135)

    features = np.array([
        [7000., 50., 1.],
        [7050., 100., 0.5],
        [7025., 25., 2.],
    ])

    for feat_params in features:
        mean, std, a = feat_params
        wave_feat = np.linspace(mean - 3. * std, mean + 3. * std)

        feature = gaussian(wave_feat, mean, std, a)
        ax.plot(wave_feat, feature)

    fn = f'{output_dir}/gaussian.png'
    fig.savefig(fn)

    plt.close('all')


def test_plot_gaussian_feature(output_dir):
    fig, ax = setup_plot(plot_type='optical')

    wave = np.linspace(3000., 9000.)
    T_bb = 7000.

    features = np.array([
        [4000., 50., -0.1],
        [5000., 100., -0.05],
        [7000., 25., -0.2],
    ])

    for feat_params in features:
        mean, std, _ = feat_params
        wave_feat = np.linspace(mean - 3. * std, mean + 3. * std)
        wave = np.concatenate((wave, wave_feat), axis=0)

    wave.sort()

    flux = planck(wave, T_planck=T_bb)
    flux /= flux.max()

    for feat_params in features:
        feature = gaussian(wave, *feat_params)
        flux += feature

    ax.plot(wave, flux)

    fn = f'{output_dir}/gaussian_feature.png'
    fig.savefig(fn)
