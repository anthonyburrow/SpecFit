from SpecFit.SpecFit import SpecFit


def check_near_match(val_1, val_2):
    pct_change = abs(val_1 - val_2) / val_2
    is_match = pct_change < 1e-2
    if not is_match:
        print(f'\nUnmatched: {val_1:.3f}, {val_2:.3f}')
    return is_match


def test_params_default(spectrum_optical, T_representative):
    spec = SpecFit(spectrum_optical)

    spec.add_model('bb')
    spec.fit()

    params = spec.best_params
    assert check_near_match(params['M0_T_planck'], T_representative)


def test_params_both(spectrum_optical, T_representative):
    spec = SpecFit(spectrum_optical)

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
    spec.fit()

    params = spec.best_params
    assert check_near_match(params['M0_T_planck'], T_representative)


def test_params_one(spectrum_optical, T_representative):
    spec = SpecFit(spectrum_optical)

    params_bb = {
        'T_planck': {
            'value': 6000.,
            'min': 4000.,
            'max': 10000.,
        },
    }
    spec.add_model('bb', params_bb)
    spec.fit()

    params = spec.best_params
    assert check_near_match(params['M0_T_planck'], T_representative)


def test_params_none(spectrum_optical, T_representative):
    spec = SpecFit(spectrum_optical)

    params_bb = {}
    spec.add_model('bb', params_bb)
    spec.fit()

    params = spec.best_params
    assert check_near_match(params['M0_T_planck'], T_representative)


def test_params_wrong(spectrum_optical, T_representative):
    spec = SpecFit(spectrum_optical)

    params_bb = {
        'T_planc': {
            'value': 6000.,
            'min': 4000.,
            'max': 10000.,
        },
    }
    spec.add_model('bb', params_bb)
    spec.fit()

    params = spec.best_params
    assert len(params) == 2
    assert check_near_match(params['M0_T_planck'], T_representative)
