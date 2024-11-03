import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).parents[2].absolute() / 'data'
FILE_GAUNT_TABLE = DATA_DIR / 'gauntff.dat'


def read_gaunt_params(fn: str = None) -> dict:
    if fn is None:
        fn = FILE_GAUNT_TABLE

    params = {}
    with open(fn, 'r') as file:
        count = 0
        for line in file.readlines():
            if line[0] == '#':
                continue

            line = line.split()

            if count == 0:
                params['magic'] = int(line[0])
            elif count == 1:
                params['N_gamma2'] = int(line[0])
                params['N_u'] = int(line[1])
            elif count == 2:
                params['log_gamma2_min'] = float(line[0])
            elif count == 3:
                params['log_u_min'] = float(line[0])
            elif count == 4:
                params['step'] = float(line[0])

            if count < 4:
                count += 1
                continue

            return params


def read_gaunt_table(N_lines: int, fn: str = None) -> np.ndarray:
    if fn is None:
        fn = FILE_GAUNT_TABLE

    return np.loadtxt(fn, skiprows=42, max_rows=N_lines)
