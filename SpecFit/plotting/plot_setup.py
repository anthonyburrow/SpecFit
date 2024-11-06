import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter, NullFormatter


PLOT_DPI = 125


def basic_spectrum():
    fig, ax = plt.subplots(dpi=PLOT_DPI)

    ax.grid(which='both', axis='x')

    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True)

    return fig, ax


def basic_opt_spectrum():
    fig, ax = basic_spectrum()

    ax.set_xlabel('Wavelength [A]')
    ax.set_ylabel('Flux')

    ax.set_yscale('log')

    # ax.xaxis.set_major_locator(MultipleLocator(1000.))
    # ax.xaxis.set_minor_locator(MultipleLocator(200.))

    plt.tight_layout()

    return fig, ax


def basic_opt_nir_spectrum():
    fig, ax = basic_spectrum()

    ax.set_xlabel(r'Wavelength [$\mu$m]')
    ax.set_ylabel('Flux')

    ax.set_xscale('log')
    ax.set_yscale('log')

    def x_label_fmt(x, pos):
        return f'{x:.1f}'

    plt.tight_layout()

    return fig, ax


def residual_spectrum():
    fig = plt.figure(dpi=PLOT_DPI)

    ax = fig.add_axes([0.15, 0.3, 0.8, 0.6])
    ax_res = fig.add_axes([0.15, 0.15, 0.8, 0.15])

    # Main axis
    ax.grid(which='both', axis='x')

    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True)

    # Residual axis
    ax_res.grid(which='both', axis='x')

    ax_res.tick_params(axis='both', which='both', direction='in',
                       top=True, right=True)

    return fig, ax, ax_res


def residual_opt_spectrum():
    fig, ax, ax_res = residual_spectrum()

    ax.set_xlabel('Wavelength [A]')
    ax.set_ylabel('Flux')

    ax.set_yscale('log')

    # ax.xaxis.set_major_locator(MultipleLocator(1000.))
    # ax.xaxis.set_minor_locator(MultipleLocator(200.))

    plt.tight_layout()

    return fig, ax, ax_res


def residual_opt_nir_spectrum():
    fig, ax, ax_res = residual_spectrum()

    ax.set_ylabel('Flux')

    ax.set_xscale('log')
    ax.set_yscale('log')

    def x_label_fmt(x, pos):
        return f'{x:.1f}'

    ax_res.set_xlabel(r'Wavelength [$\mu$m]')
    ax_res.set_ylabel(r'Residual')

    ax_res.set_xscale('log')

    plt.tight_layout()

    return fig, ax, ax_res
