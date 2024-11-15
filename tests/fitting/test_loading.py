from SpecFit.SpecFit import SpecFit


def check_near_match(val_1, val_2):
    pct_change = abs(val_1 - val_2) / val_2
    is_match = pct_change < 1e-2
    if not is_match:
        print(f'\nUnmatched: {val_1:.3f}, {val_2:.3f}')
    return is_match


def test_smoothing(spectrum_optical, T_representative):
    read_params = {
        'smooth_method': 'boxcar',
    }
    spec = SpecFit(spectrum_optical, **read_params)

    assert spec.data[:, 1].max() == 1.

    spec.add_model('bb')
    spec.fit()

    params = spec.best_params
    assert check_near_match(params['M0_T_planck'], T_representative)
