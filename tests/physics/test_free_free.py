import numpy as np

from SpecFit.physics.free_free import ff


def test_free_free():
    wave = np.linspace(5000., 10000.)
    T = 7000.

    j = ff(wave, T)
