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
