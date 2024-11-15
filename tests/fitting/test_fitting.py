from SpecFit import SpecFit


def test_default(output_dir, spectrum_optical):
    spec = SpecFit(spectrum_optical)
    spec.add_model('bb')
    spec.fit()

    fn = f'{output_dir}/fitting_default.png'
    spec.plot(out_filename=fn)
