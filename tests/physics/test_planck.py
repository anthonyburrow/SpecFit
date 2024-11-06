import numpy as np

from SpecFitModels import planck


def test_planck():
    wave = np.linspace(5000., 7000., 100)
    T_bb = 10_000.

    planck(wave, T_planck=T_bb)


def test_plot_planck(basic_opt_spectrum, test_plot_dir):
    fig, ax = basic_opt_spectrum

    T_arr = np.linspace(5000., 10000., 8)
    wave = np.linspace(3000., 9000.)

    for T in T_arr:
        flux = planck(wave, T_planck=T)
        ax.plot(wave, flux)

    fn = f'{test_plot_dir}/planck.png'
    fig.savefig(fn)
