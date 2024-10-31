from .plot_setup import basic_opt_spectrum, basic_opt_nir_spectrum


def plot_spectrum(data, model_result,
                  out_filename=None, display=False, plot_type=None):
    if plot_type == 'nir' or plot_type is None:
        fig, ax = basic_opt_nir_spectrum()
    elif plot_type == 'optical':
        fig, ax = basic_opt_spectrum()

    wave = data[:, 0]
    flux = data[:, 1]

    ax.plot(wave, flux)
    ax.plot(wave, model_result.best_fit)

    if out_filename is not None:
        fig.savefig(out_filename)

    if display:
        fig.show()

    return fig, ax
