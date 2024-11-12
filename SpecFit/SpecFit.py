import numpy as np
from typing import Callable
from lmfit import Model, Parameters
from lmfit.model import ModelResult

from SpectrumCore.io import read
from SpectrumCore.processing import preprocess
from SpectrumCore.plot import plot_spectrum

from .models.wrappers import planck_wrapper, ff_wrapper
from .util.default_params import default_params


PLANCK_MODEL_KEYS = ('planck', 'bb')
FF_MODEL_KEYS = ('free_free', 'ff')


class SpecFit:

    def __init__(self, data: str | np.ndarray, wave_units: str = None,
                 *args, **kwargs):
        """Instantiate the `SpecFit` object.

        Parameters
        ----------
        data : str | np.ndarray
            Filename or `numpy.ndarray` array containing the input spectrum. If
            a filename is provided, it must be a `.fits` file readable by
            `SpectrumCore.io.read()`, or a human-readable file with the first
            three columns as wavelength, flux, and (optional) flux uncertainty
            values, respectively. If an array is provided, it must be of shape
            (N, 2) or (N, 3), with columns provided as wavelength, flux, and
            (optionally) flux uncertainty.
        wave_units : str, optional
            Units for the wavelengths provided in `data`. Options are
            'angstroms' or 'microns'; by default, 'angstroms' is assumed.
        **kwargs
            Arguments to pass to `SpectrumCore.processing.preprocess()`:
                z : float, optional
                    Redshift value for rest-frame wavelength correction.
                wave_range : tuple[float], optional
                    The wavelength range of the input spectrum to use in
                    Angstroms. By default, the full spectrum is used.
                remove_nans : bool, optional
                    Removes all rows that contain any NaN value. By default,
                    this is `True`.
                remove_nonpositive : bool, optional
                    Removes all rows with flux values less than or equal to 0.
                    By default, this is `True`.
                remove_telluric : bool, optional
                    Remove a set of telluric features (see
                    `SpectrumCore.physics.telluric`) before correcting for host
                    redshift.
                host_EBV : float, optional
                    Host galaxy color excess used for dereddening.
                host_RV : float, optional
                    Host reddening vector used for dereddening.
                MW_EBV : float, optional
                    Milky-Way galaxy color excess used for dereddening.
                MW_RV : float, optional
                    Milky-Way reddening vector used for dereddening. Default is
                    assumed as 3.1.
        """
        if isinstance(data, str):
            self.data = read(data)
        else:
            # data = data.copy()
            self.data = data

        if wave_units is None:
            wave_units = 'angstroms'

        if wave_units == 'microns':
            self.data[:, 0] *= 1.e4

        kwargs['normalize'] = True
        self.data = preprocess(self.data, *args, **kwargs)

        self.model = None
        self.params = Parameters()
        self.result = None

    def add_model(self, model: str | Callable, params: dict = None):
        """Add a model to the current overall model.

        Parameters
        ----------
        model : str | Callable
            The model to add, as a string or a callable function. If given
            a string, it must be one of the following:
            ('planck', 'free_free').
        params : dict, optional
            Initial guesses for the parameters of the corresponding model,
            given in the same dictionary format as with `lmfit`, including
            min/max values, etc. If using an internal, premade model,
            each individual parameter is optional, as a calculated guess is
            automatically provided.
        """
        model_func = self._parse_model(model)
        model_obj = Model(model_func)

        if self.model is None:
            self.model = model_obj
        else:
            self.model += model_obj

        for param in model_obj.param_names:
            if params is None:
                param_func = default_params[param]
                param_info = param_func(self.data)
                self.params.add(param, **param_info)
            elif param in params:
                param_info = params[param]
                self.params.add(param, **param_info)
            elif param in default_params:
                param_func = default_params[param]
                param_info = param_func(self.data)
                self.params.add(param, **param_info)
            else:
                print(f'{param} not given an initial value.')

    def fit(self, *args, **kwargs) -> ModelResult:
        """Fit all parameters to the composite model.

        Parameters
        ----------
        **kwargs
            Additional arguments to pass to `lmfit.Model.fit()`, including
            those such as `method` ('leastsq', 'emcee', etc.) or `max_nfev`
            (maximum number of iterations).

        Returns
        -------
        lmfit.ModelResult
            The `ModelResult` object given by `lmfit.Model.fit()`.
        """
        result = self.model.fit(
            self.data[:, 1], self.params, wave=self.data[:, 0],
            weights=1. / self.data[:, 1],
            *args, **kwargs
        )
        self.result = result
        return result

    def fit_report(self) -> str:
        """Prints and returns the `lmfit.ModelResult.fit_report()` of the
        previous fit.

        Returns
        -------
        str
            The printable fit report.
        """
        fit_report = self.result.fit_report()
        print(fit_report)
        return fit_report

    def plot(self, *args, **kwargs) -> tuple:
        """Plot the fit model along with the original (preprocessed) data.

        Parameters
        ----------
        **kwargs
            Arguments to pass to `SpectrumCore.plot.plot_spectrum()`:

            residuals : bool
                Display residuals between data and the model as a bottom panel
                in the plot. Default is `False`.
            plot_type : str
                Changes some formatting of the plot. Allowed values are:
                'optical' (linear x-axis, given in Angstroms, etc.), 'nir'
                (log x-axis, given in microns, etc.). By default, an educated
                guess is made based on `SpecFit.data`.
            out_filename : str
                Filename to save the plot as. The plot is unsaved unless this
                value is given.
            display : str
                Display the plot in a new window upon finalizing it. Default is
                `False`.

        Returns
        -------
        tuple
            A tuple of the `plt.figure` and `plt.axis` objects of the resulting
            plot (fig, ax). If `residuals=True`, a third item is returned as
            well for the residual plot `pyplot.axis` (fig, ax, ax_res).
        """
        return plot_spectrum(self.data, model_result=self.result,
                             *args, **kwargs)

    def _parse_model(self, model: str | Callable) -> Callable:
        if model in PLANCK_MODEL_KEYS:
            return planck_wrapper
        elif model in FF_MODEL_KEYS:
            return ff_wrapper

        return model
