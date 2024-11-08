import numpy as np
from typing import Callable
from lmfit import Model, Parameters

from SpectrumCore.io import read
from SpectrumCore.processing import preprocess
from SpectrumCore.plot import plot_spectrum

from .models.wrappers import planck_wrapper, ff_wrapper
from .util.default_params import default_params


PLANCK_MODEL_KEYS = ('planck', 'bb')
FF_MODEL_KEYS = ('free_free', 'ff')


class SpecFit:

    def __init__(self, data: str | np.ndarray, *args, **kwargs):
        if isinstance(data, str):
            self.data = read(data)
        else:
            # data = data.copy()
            self.data = data

        kwargs['normalize'] = True
        self.data = preprocess(self.data, *args, **kwargs)

        self.model = None
        self.params = Parameters()
        self.result = None

    def add_model(self, model: str | Callable, params: dict = None):
        """Add a model to the current overall model.

        Parameters
        ----------
        model : str or Callable
            The model to add, as a string or a callable function. If given
            a string, it must be one of the following:
            ('planck', 'free_free').
        """
        model_func = self._parse_model(model)
        model_obj = Model(model_func)

        if self.model is None:
            self.model = model_obj
        else:
            self.model += model_obj

        for param in self.model.param_names:
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
        if model in PLANCK_MODEL_KEYS:
            return planck_wrapper
        elif model in FF_MODEL_KEYS:
            return ff_wrapper

        return model
