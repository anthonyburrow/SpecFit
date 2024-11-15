import pytest
import numpy as np


@pytest.fixture(scope='session')
def wave_optical():
    return np.linspace(3000., 9000., 1000)


@pytest.fixture(scope='session')
def wave_NIR():
    return np.linspace(5000., 30000., 1000)


@pytest.fixture(scope='session')
def T_representative():
    return 7000.


@pytest.fixture(scope='session')
def T_array():
    return np.linspace(5000., 15000., 10)
