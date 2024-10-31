import pytest
from pathlib import Path

from tests.plot_fixtures import basic_opt_spectrum, basic_opt_nir_spectrum


TEST_PLOT_DIR = './tests/output'


def pytest_sessionstart(session):
    Path(TEST_PLOT_DIR).mkdir(exist_ok=True)


@pytest.fixture
def test_plot_dir():
    return TEST_PLOT_DIR
