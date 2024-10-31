import numpy as np
from SpecFit.SpecFit import SpecFit


fn = 'sn2023ixf_visit1_combined_v3.dat'
data = np.loadtxt(fn, usecols=(0, 2, 3), skiprows=1)
data[:, 0] *= 1e4
read_params = {
    'z': 0.0008,
}
spec = SpecFit(data, **read_params)

params_bb = {
    'T_planck': {
        'value': 5000.,
        'min': 1000.,
        'max': 20000.,
    },
    'a_planck': {
        'value': 1.e-7,
    },
}
spec.add_model('bb', params_bb)

# params_ff = {
#     'a_ff': {
#         'value': 1e-17,
#         'min': 0.,
#     },
#     'T_ff': {
#         'value': 6000.,
#         'min': 1000.,
#         'max': 20000.,
#     },
# }
# spec.add_model('ff', params_ff)

spec.fit()

spec.fit_report()

fn = 'test_plot.png'
spec.plot(fn, plot_type='nir')
