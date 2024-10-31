import pytest
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FuncFormatter, NullFormatter


@pytest.fixture
def basic_opt_spectrum(test_plot_dir):
    fig, ax = plt.subplots(dpi=125)

    ax.grid(which='both', axis='x')

    ax.set_xlabel('Wavelength [A]')
    ax.set_ylabel('Flux')

    ax.set_yscale('log')

    ax.xaxis.set_major_locator(MultipleLocator(1000.))
    ax.xaxis.set_minor_locator(MultipleLocator(200.))

    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True)

    plt.tight_layout()

    return fig, ax


@pytest.fixture
def basic_opt_nir_spectrum(test_plot_dir):
    fig, ax = plt.subplots(dpi=125)

    ax.grid(which='both', axis='x')

    ax.set_xlabel(r'Wavelength [$\mu$m]')
    ax.set_ylabel('Flux')

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.xaxis.set_major_locator(MultipleLocator(0.5))
    ax.xaxis.set_minor_locator(MultipleLocator(0.1))

    def x_label_fmt(x, pos):
        # if x > 2.:
        #     return ''
        return f'{x:.1f}'

    ax.xaxis.set_major_formatter(FuncFormatter(x_label_fmt))
    ax.xaxis.set_minor_formatter(NullFormatter())

    ax.tick_params(axis='both', which='both', direction='in',
                   top=True, right=True)

    plt.tight_layout()

    return fig, ax
