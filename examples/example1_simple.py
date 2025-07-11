import numpy as np
from SpecFit import SpecFit


# Manually read spectrum data if file has unusual format
fn = 'sn2023ixf_visit1_combined_v3.dat'
data = np.loadtxt(fn, usecols=(0, 2, 3), skiprows=1)

# Load and preprocess spectrum
read_params = {
    'z': 0.0008,
    'wave_unit': 'microns',
    'smooth_method': 'boxcar',
}
spec = SpecFit(data, **read_params)

spec.add_model('bb')
spec.add_model('ff')

spec.fit()

spec.fit_report()

fn = 'test_plot.png'
spec.plot(out_filename=fn, residuals=True)
