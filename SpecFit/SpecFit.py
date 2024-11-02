import numpy as np
from typing import Callable
from lmfit import Model, Parameters

from spextractor.util.io import load_spectra
from spextractor.util.preprocessing import preprocess

from .models.wrappers import planck_wrapper, ff_wrapper
# from .physics.planck import planck_wave
# from .physics.free_free import ff
from .plotting.plot import plot_spectrum


class SpecFit:

    def __init__(self, data: str | np.ndarray, *args, **kwargs):
        if isinstance(data, str):
            self.data = load_spectra(data)
        else:
            # data = data.copy()
            self.data = data

        self.data = preprocess(self.data, *args, **kwargs)

        self.model = None
        self.params = Parameters()
        self.result = None

    def add_model(self, model: str | Callable, params: dict):
        """Add a model to the current overall model.

        Parameters
        ----------
        model : str or Callable
            The model to add, as a string or a callable function. If given
            a string, it must be one of the following:
            ('planck', 'free_free').
        """
        model_func = self._parse_model(model)
        model = Model(model_func)

        if self.model is None:
            self.model = model
        else:
            self.model += model

        for param_key in model.param_names:
            if param_key not in params:
                raise Exception(f'{param_key} parameter not provided.')
            self.params.add(param_key, **params[param_key])

    def fit(self):
        result = self.model.fit(
            self.data[:, 1], self.params, wave=self.data[:, 0]
        )
        self.result = result
        return result

    def fit_report(self):
        fit_report = self.result.fit_report()
        print(fit_report)
        return fit_report

    def plot(self, *args, **kwargs):
        return plot_spectrum(self.data, self.result, *args, **kwargs)

    def _parse_model(self, model: str | Callable) -> Callable:
        if model in ('planck', 'bb'):
            return planck_wrapper
            # return planck_wave
        elif model in ('free_free', 'ff'):
            # return ff
            return ff_wrapper

        return model
