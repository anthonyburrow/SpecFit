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
        'value': 4000.,
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
        'min': 1000.,
        'max': 20000.,
        # 'vary': False
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
spec.plot(out_filename=fn, plot_type='nir', residuals=True)
