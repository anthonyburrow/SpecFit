import numpy as np

from SpecFit.physics.free_free import ff


def test_free_free():
    wave = np.linspace(5000., 10000.)
    T = 7000.

    j = ff(wave, T)


def test_plot_planck(basic_opt_nir_spectrum, test_plot_dir):
    fig, ax = basic_opt_nir_spectrum

    T_arr = np.linspace(5000., 10000., 8)
    wave = np.linspace(0.3, 3.)

    for T in T_arr:
        flux = ff(wave * 1e4, T)
        ax.plot(wave, flux)

    fn = f'{test_plot_dir}/free_free.png'
    fig.savefig(fn)
