import pytest
from pathlib import Path

from SpecFit.data.retrieve import get_gaunt

# Do not remove...needed for plot fixtures
from tests.plot_fixtures import basic_opt_spectrum, basic_opt_nir_spectrum


TEST_PLOT_DIR = './tests/output'


def pytest_sessionstart(session):
    # Make directory for test output
    Path(TEST_PLOT_DIR).mkdir(exist_ok=True)

    # Download required modeling data
    get_gaunt()


@pytest.fixture
def test_plot_dir():
    return TEST_PLOT_DIR
