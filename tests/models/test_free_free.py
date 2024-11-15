import numpy as np

from SpectrumCore.plot import setup_plot

from SpecFitModels import ff


def test_ff(wave_NIR, T_representative, gaunt_params, gaunt_table):
    j = ff(wave_NIR, T_ff=T_representative,
           gaunt_params=gaunt_params, gaunt_table=gaunt_table)

    expected = np.array([
        1.4556626, 1.4710085, 1.4862883, 1.5015004, 1.5166433
    ])
    actual = np.around(j[:5], 7)

    assert np.array_equal(actual, expected)


def test_ff_args(wave_NIR, T_representative, gaunt_params, gaunt_table):
    j = ff(wave_NIR, T_representative, 1.0, gaunt_params, gaunt_table)

    expected = np.array([
        1.4556626, 1.4710085, 1.4862883, 1.5015004, 1.5166433
    ])
    actual = np.around(j[:5], 7)

    assert np.array_equal(actual, expected)


def test_ff_plot(output_dir, wave_NIR, T_array, gaunt_params, gaunt_table):
    fig, ax = setup_plot(plot_type='nir')

    for T in T_array:
        flux = ff(wave_NIR, T_ff=T,
                  gaunt_params=gaunt_params, gaunt_table=gaunt_table)
        ax.plot(wave_NIR, flux)

    fn = f'{output_dir}/free_free.png'
    fig.savefig(fn)
