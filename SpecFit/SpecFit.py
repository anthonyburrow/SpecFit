import numpy as np
from typing import Callable
from lmfit import Model, Parameters

from spextractor.util.io import load_spectra
from spextractor.util.preprocessing import preprocess

from .models.wrappers import planck_wrapper, ff_wrapper
from .plotting.plot import plot_spectrum


class SpecFit:

    def __init__(self, data: str | np.ndarray, *args, **kwargs):
        if isinstance(data, str):
            self.data = load_spectra(data)
        else:
            # data = data.copy()
            self.data = data

        self.data = preprocess(self.data, *args, **kwargs)
        self.data[:, 1] /= self.data[:, 1].max()
        self.data[:, 2] /= self.data[:, 1].max()

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

        for param_key, param_info in params.items():
            self.params.add(param_key, **param_info)

    def fit(self, *args, **kwargs):
        result = self.model.fit(
            self.data[:, 1], self.params, wave=self.data[:, 0],
            *args, **kwargs
        )
        self.result = result
        return result

    def fit_report(self):
        fit_report = self.result.fit_report()
        print(fit_report)
        return fit_report

    def plot(self, *args, **kwargs):
        return plot_spectrum(data=self.data, model_result=self.result,
                             *args, **kwargs)

    def _parse_model(self, model: str | Callable) -> Callable:
        if model in ('planck', 'bb'):
            return planck_wrapper
        elif model in ('free_free', 'ff'):
            return ff_wrapper

        return model
