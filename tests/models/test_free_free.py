from SpectrumCore.plot import setup_plot

from SpecFitModels import ff


def test_free_free(wave_NIR, T_representative, gaunt_params, gaunt_table):
    ff(wave_NIR, T_ff=T_representative,
       gaunt_params=gaunt_params, gaunt_table=gaunt_table)


def test_plot_free_free(output_dir, wave_NIR, T_array, gaunt_params, gaunt_table):
    fig, ax = setup_plot(plot_type='nir')

    for T in T_array:
        flux = ff(wave_NIR, T_ff=T,
                  gaunt_params=gaunt_params, gaunt_table=gaunt_table)
        ax.plot(wave_NIR, flux)

    fn = f'{output_dir}/free_free.png'
    fig.savefig(fn)
