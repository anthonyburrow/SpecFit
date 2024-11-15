import numpy as np

from SpectrumCore.plot import setup_plot

from SpecFitModels import planck


def test_planck(wave_optical, T_representative):
    p = planck(wave_optical, T_planck=T_representative)

    expected = np.array([
        0.5191479, 0.5210742, 0.5229895, 0.5248939, 0.5267874
    ])
    actual = np.around(p[:5], 7)

    assert np.array_equal(actual, expected)


def test_planck_args(wave_optical, T_representative):
    p = planck(wave_optical, T_representative, 1.0)

    expected = np.array([
        0.5191479, 0.5210742, 0.5229895, 0.5248939, 0.5267874
    ])
    actual = np.around(p[:5], 7)

    assert np.array_equal(actual, expected)


def test_plot_planck(wave_optical, T_array, output_dir):
    fig, ax = setup_plot(plot_type='optical')

    for T in T_array:
        flux = planck(wave_optical, T_planck=T)
        ax.plot(wave_optical, flux)

    fn = f'{output_dir}/planck.png'
    fig.savefig(fn)
