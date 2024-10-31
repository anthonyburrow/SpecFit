import numpy as np

from SpecFit.physics.planck import planck
from SpecFit.physics.constants import c


def test_planck():
    ang_to_cm = 1.e-8
    wave = 5_000.
    T_bb = 10_000.
    nu = c / (wave * ang_to_cm)

    bb_wave = planck(wave, T_bb)
    bb_freq = planck(nu, T_bb, variable='frequency')

    # Check differential conversion between B_lam and B_nu (within some accuracy)
    result = (c / ang_to_cm) * bb_wave / (nu**2 * bb_freq)
    assert abs(1. - result) < 1e-10


def test_plot_planck(basic_opt_spectrum, test_plot_dir):
    fig, ax = basic_opt_spectrum

    T_arr = np.linspace(5000., 10000., 8)
    wave = np.linspace(3000., 9000.)

    for T in T_arr:
        flux = planck(wave, T)
        ax.plot(wave, flux)

    fn = f'{test_plot_dir}/planck.png'
    fig.savefig(fn)
