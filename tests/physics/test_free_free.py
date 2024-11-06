import numpy as np

from SpecFitModels import ff
from SpecFit.util.io import read_gaunt_params, read_gaunt_table


def test_free_free():
    wave = np.linspace(5000., 10000.)
    T = 7000.

    gaunt_params = read_gaunt_params()
    gaunt_table = read_gaunt_table(gaunt_params['N_u'])

    j = ff(wave, T_ff=T,
           gaunt_params=gaunt_params, gaunt_table=gaunt_table)


def test_plot_free_free(basic_opt_nir_spectrum, test_plot_dir):
    fig, ax = basic_opt_nir_spectrum

    T_arr = np.linspace(5000., 10000., 8)
    wave = np.linspace(0.3, 3.)

    gaunt_params = read_gaunt_params()
    gaunt_table = read_gaunt_table(gaunt_params['N_u'])

    for T in T_arr:
        flux = ff(wave * 1e4, T_ff=T,
                  gaunt_params=gaunt_params, gaunt_table=gaunt_table)
        ax.plot(wave, flux)

    fn = f'{test_plot_dir}/free_free.png'
    fig.savefig(fn)
