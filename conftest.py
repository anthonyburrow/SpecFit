import pytest
from pathlib import Path

from SpecFit.data.retrieve import get_gaunt


OUTPUT_DIR = './tests/output'


def pytest_sessionstart(session):
    # Make directory for test output
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    # Download required modeling data
    get_gaunt()


@pytest.fixture
def output_dir():
    return OUTPUT_DIR
