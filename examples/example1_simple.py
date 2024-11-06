import numpy as np
from SpecFit.SpecFit import SpecFit


# Get spectrum data if file has unusual format
fn = 'sn2023ixf_visit1_combined_v3.dat'
data = np.loadtxt(fn, usecols=(0, 2, 3), skiprows=1)
data[:, 0] *= 1e4

# Load and preprocess spectrum
read_params = {
    'z': 0.0008,
}
spec = SpecFit(data, **read_params)

spec.add_model('bb')
spec.add_model('ff')

spec.fit()

spec.fit_report()

fn = 'test_plot.png'
spec.plot(out_filename=fn, plot_type='nir', residuals=True)
