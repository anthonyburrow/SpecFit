import pytest
from pathlib import Path

from retrieve_data import get_gaunt


OUTPUT_DIR = Path('./tests/output')


def pytest_sessionstart(session):
    # Make directory for test output
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Download required modeling data
    get_gaunt()


@pytest.fixture
def output_dir():
    return OUTPUT_DIR
