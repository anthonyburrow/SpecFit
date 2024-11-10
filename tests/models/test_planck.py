import numpy as np

from SpectrumCore.plot import setup_plot

from SpecFitModels import planck


def test_planck():
    wave = np.linspace(5000., 7000., 100)
    T_bb = 10_000.

    planck(wave, T_planck=T_bb)


def test_plot_planck(output_dir):
    fig, ax = setup_plot(plot_type='optical')

    T_arr = np.linspace(5000., 10000., 8)
    wave = np.linspace(3000., 9000.)

    for T in T_arr:
        flux = planck(wave, T_planck=T)
        ax.plot(wave, flux)

    fn = f'{output_dir}/planck.png'
    fig.savefig(fn)
