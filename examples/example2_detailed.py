import numpy as np
from SpecFit.SpecFit import SpecFit


# Manually read spectrum data if file has unusual format
fn = 'sn2023ixf_visit1_combined_v3.dat'
data = np.loadtxt(fn, usecols=(0, 2, 3), skiprows=1)

# Load and preprocess spectrum
read_params = {
    'z': 0.0008,
    'wave_units': 'microns',
}
spec = SpecFit(data, **read_params)

params_bb = {
    'T_planck': {
        'value': 6000.,
        'min': 4000.,
        'max': 10000.,
    },
    'a_planck': {
        'value': 1.,
    },
}
spec.add_model('bb', params_bb)

params_ff = {
    'T_ff': {
        'value': 6197.,
        'min': 0.,
        'max': 20000.,
    },
    'a_ff': {
        'value': 1.,
        'min': 0.,
    },
}
spec.add_model('ff', params_ff)

fit_params = {
    # 'method': 'emcee',
}
spec.fit(**fit_params)

spec.fit_report()

fn = 'test_plot.png'
spec.plot(out_filename=fn, residuals=True)
