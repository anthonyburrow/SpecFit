import pytest

from SpecFit.util.io import read_gaunt_params, read_gaunt_table


@pytest.fixture(scope='session')
def gaunt_params():
    return read_gaunt_params()


@pytest.fixture(scope='session')
def gaunt_table(gaunt_params):
    return read_gaunt_table(gaunt_params['N_u'])
