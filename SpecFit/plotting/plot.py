from .plot_setup import \
    basic_opt_spectrum, basic_opt_nir_spectrum, \
    residual_opt_spectrum, residual_opt_nir_spectrum


PLOT_PARAMS = {
    'lw': 1.
}


def plot_main_panel(ax, data=None, model_result=None, *args, **kwargs):
    if data is None:
        return ax

    wave = data[:, 0]
    flux = data[:, 1]

    ax.plot(wave, flux, **PLOT_PARAMS)

    if model_result is None:
        return ax

    ax.plot(wave, model_result.best_fit, **PLOT_PARAMS)

    return ax


def plot_residual_panel(ax, data=None, model_result=None, *args, **kwargs):
    if data is None and model_result is None:
        return ax

    wave = data[:, 0]
    flux = data[:, 1]
    res = flux - model_result.best_fit

    ax.plot(wave, res, 'r-', **PLOT_PARAMS)
    ax.axhline(0., color='k', **PLOT_PARAMS)

    return ax


def plot_basic_spectrum(plot_type=None, out_filename=None, display=False,
                        *args, **kwargs):
    if plot_type == 'nir' or plot_type is None:
        fig, ax, ax_res = basic_opt_nir_spectrum()
    elif plot_type == 'optical':
        fig, ax, ax_res = basic_opt_spectrum()

    plot_main_panel(ax, *args, **kwargs)
    plot_residual_panel(ax_res, *args, **kwargs)

    if out_filename is not None:
        fig.savefig(out_filename)

    if display:
        fig.show()

    return fig, ax, ax_res


def plot_residual_spectrum(plot_type=None, out_filename=None, display=False,
                           *args, **kwargs):
    if plot_type == 'nir' or plot_type is None:
        fig, ax, ax_res = residual_opt_nir_spectrum()
    elif plot_type == 'optical':
        fig, ax, ax_res = residual_opt_spectrum()

    plot_main_panel(ax, *args, **kwargs)
    plot_residual_panel(ax_res, *args, **kwargs)

    if out_filename is not None:
        fig.savefig(out_filename)

    if display:
        fig.show()

    return fig, ax, ax_res


def plot_spectrum(residuals=False, *args, **kwargs):
    if residuals:
        return plot_residual_spectrum(*args, **kwargs)
    else:
        return plot_basic_spectrum(*args, **kwargs)
