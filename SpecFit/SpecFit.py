import numpy as np
from typing import Callable
from lmfit import Model, Parameters
from lmfit.model import ModelResult

from SpectrumCore import Spectrum
from SpectrumCore.plot import plot_spectrum

from .models.wrappers import model_from_key
from .util.default_params import default_params


class SpecFit:

    def __init__(self, data: str | np.ndarray, *args, **kwargs):
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
        **kwargs
            wave_unit : str, optional
                Unit of wavelength for the input data. Available units are
                'angstrom' and 'micron'. If None, this defaults to 'angstrom'.
            remove_telluric: bool, optional
                Remove telluric features. Default is False.
            z : float, optional
                Redshift value for rest-frame wavelength correction.
            wave_range : tuple, optional
                Manually-set pruning window in Angstroms. Default is None.
            host_EBV : float, optional
                Host galaxy color excess used for dereddening.
            host_RV : float, optional
                Host reddening vector used for dereddening.
            MW_EBV : float, optional
                MW galaxy color excess used for dereddening.
            MW_RV : float, optional
                MW reddening vector used for dereddening. Default is 3.1.
            smooth_method: str, optional
                Method of smoothing the input spectrum. Can use 'boxcar' or
                'sg' (Savitzky–Golay filter).
        """
        self.spectrum = Spectrum(data, *args, **kwargs)
        self._preprocess_spectrum()

        self.model = None
        self.params = Parameters()
        self.result = None

        self.model_count = 0

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
        model_name = model if isinstance(model, str) else model.__name__
        model_prefix = f'M{self.model_count}_'

        model_obj = Model(model_func, name=model_name, prefix=model_prefix)

        if self.model is None:
            self.model = model_obj
        else:
            self.model += model_obj

        for param in model_obj.param_names:
            param_no_prefix = self._remove_prefix(param)
            if params is None:
                param_func = default_params[param_no_prefix]
                param_info = param_func(self.spectrum.data)
                self.params.add(param, **param_info)
            elif param_no_prefix in params:
                param_info = params[param_no_prefix]
                self.params.add(param, **param_info)
            elif param_no_prefix in default_params:
                param_func = default_params[param_no_prefix]
                param_info = param_func(self.spectrum.data)
                self.params.add(param, **param_info)
            else:
                print(f'{param} not given an initial value.')

        self.model_count += 1

    def fit(
        self,
        weights: str | np.ndarray = None,
        *args, **kwargs
    ) -> ModelResult:
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
        if weights is None or weights == 'log':
            weights = 1. / self.spectrum.flux
        elif weights == 'none':
            weights = None

        result = self.model.fit(
            self.spectrum.flux, self.params, wave=self.spectrum.wave,
            weights=weights,
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
        return plot_spectrum(self.spectrum.data, model_result=self.result,
                             *args, **kwargs)

    @property
    def best_fit(self):
        return self.result.best_fit

    @property
    def best_params(self):
        return self.result.best_values

    def _preprocess_spectrum(
        self,
        z: float | None = None,
        wave_range: tuple[float] | None = None,
        remove_telluric=False,
        host_EBV: float | None = None,
        host_RV: float | None = None,
        MW_EBV: float | None = None,
        MW_RV: float = 3.1,
        *args,
        **kwargs,
    ) -> None:
        self.spectrum.remove_nans()
        self.spectrum.remove_nonpositive()

        if remove_telluric:
            self.spectrum.remove_telluric()   # TODO: AFTER MANGLING

        if z is not None and z != 0.:
            self.spectrum.deredshift(z)

        if wave_range is not None:
            self.spectrum.prune(wave_range)

        # Milky Way extinction
        if MW_EBV is not None and MW_EBV != 0. and MW_RV is not None:
            self.spectrum.deredden(E_BV=MW_EBV, R_V=MW_RV)

        # Host extinction
        if host_EBV is not None and host_EBV != 0. and host_RV is not None:
            self.spectrum.deredden(E_BV=host_EBV, R_V=host_RV)

        self.spectrum.smooth(*args, **kwargs)

        self.spectrum.normalize_flux(method='max')

    def _parse_model(self, model: str | Callable) -> Callable:
        """Retrieve the function from premade function keys."""
        if model in model_from_key:
            return model_from_key[model]

        return model

    def _remove_prefix(self, param):
        return '_'.join(param.split('_')[1:])
