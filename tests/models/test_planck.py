from SpectrumCore.plot import setup_plot

from SpecFitModels import planck


def test_planck(wave_optical, T_representative):
    planck(wave_optical, T_planck=T_representative)


def test_plot_planck(wave_optical, T_array, output_dir):
    fig, ax = setup_plot(plot_type='optical')

    for T in T_array:
        flux = planck(wave_optical, T_planck=T)
        ax.plot(wave_optical, flux)

    fn = f'{output_dir}/planck.png'
    fig.savefig(fn)
