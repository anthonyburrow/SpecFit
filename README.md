# SpecFit

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/anthonyburrow/SpecFit/run_pytest.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`SpecFit` is designed to be a versatile spectrum-fitting tool. Utilizing the
Python package `lmfit`, this tool performs non-linear least-squares
minimization to accurately model astrophysical spectra. `SpecFit` streamlines
the process of deriving physical parameters such as blackbody temperature by
integrating an internal preprocessing pipeline. With the support of
[`pybind11`](https://github.com/pybind/pybind11) and C++, `SpecFit` allows for
the iteration of complex (non-vectorizable) models within `lmfit`, combining
Python's simplicity to perform data analysis with the computational efficiency
of C++.

## Installation

### Model Data

Prior to installing `SpecFit`, it is important to note that some data is
necessary for some models:

- Free-free emission

To retrieve this data, after cloning this repository, run the
'SpecFit/SpecFit/data/retrieve.py' script. Currently, the script downloads the
following:

- Gaunt factor table from [https://data.nublado.org/gauntff](https://data.nublado.org/gauntff)

The data will be downloaded and subsequently copied into the Python
site-packages `SpecFit` directory upon installation (the following step).

### Building

The Python bindings of the C++ modeling code must be built first before using
this package. The 'setup.py' and 'pyproject.toml' handle this automatically;
to install `SpecFit`, simply do so using:
```shell
python -m pip install path/to/SpecFit
```

Performing this step will automatically install its other Python dependencies,
which are:

- `NumPy`
- `SciPy`
- `lmfit`
- `SpectrumCore` ([My core repository for spectrum operations](https://github.com/anthonyburrow/SpectrumCore))

## Operation

See the examples in the 'SpecFit/examples' directory.

Using `SpecFit` is intended to be simple and uses the following general
approach:

1. Instantiate the `SpecFit` object by providing the file name (for simple data
with wave/flux/error as the first three columns) or just a `NumPy` array of the
with wave/flux/error(optional) in the first 3 columns:

    ```python
    from SpecFit.SpecFit import SpecFit

    fn = 'my_spectrum.dat'
    optional_read_params = {
        # ...
    }
    spec = SpecFit(fn, **optional_read_params)
    ```

2. Add submodels to the composite model to be processed by `lmfit`. Custom
functions may be passed, or strings corresponding to the available premade
models in C++:

    ```python
    # Adds a "blackbody" (Planck function) model
    spec.add_model('bb')

    # Adds a "free-free emission" model
    spec.add_model('free_free')
    ```

    Default parameters are determined during this step for premade models;
    however, one may optionally provide initial parameters to `add_model` in
    the same manner as for `lmfit`. See examples for details. If providing a
    custom callable function to `add_model`, providing initial guesses for
    parameters will be necessary.

3. Fit the parameters of the provided model.

    ```python
    spec.fit()
    ```

    This method essentially calls the `lmfit.Model.fit()` method with
    appropriate arguments provided to it. However, `SpecFit.fit()` passes any
    additional keyword-arguments given to it directly to the
    `lmfit.Model.fit()` method (see examples).

4. After fitting, data analysis can occur. Best-fit parameters can be viewed
with `SpecFit.fit_report()`, or a plot may be retrieved with `SpecFit.plot()`.
See examples for more details.

