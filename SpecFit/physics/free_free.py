import numpy as np
from numpy.polynomial.polynomial import Polynomial
from scipy.interpolate import lagrange

from .constants import h, c, k_B, Ryd
from .planck import planck


def read_params(fn: str) -> dict:
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


def read_table(fn: str, N_lines: int) -> np.ndarray:
    return np.loadtxt(fn, skiprows=42, max_rows=N_lines)


def interp_lagrange(
    x_interp: float | np.ndarray,
    x_table: np.ndarray,
    y_table: np.ndarray,
) -> float | np.ndarray:
    poly = lagrange(x_table, y_table)
    return Polynomial(poly.coef[::-1])(x_interp)


def interpolate_gaunt(
    wave: np.ndarray,
    T: float,
    N_interp: int = 4
) -> np.ndarray:
    u = h * c / (wave * 1e-8 * k_B * T)
    gamma2 = h * c * Ryd / (k_B * T)

    log_u = np.log10(u)
    log_gamma2 = np.log10(gamma2)

    # Setup interpolation
    fn = './data/gauntff.dat'
    table_params = read_params(fn)
    gaunt_table = read_table(fn, table_params['N_u'])

    # Interpolate Gaunt factor
    log_gamma2_min = table_params['log_gamma2_min']
    log_u_min = table_params['log_u_min']
    N_gamma2 = table_params['N_gamma2']
    N_u = table_params['N_u']
    step = table_params['step']

    ind_gamma = int((log_gamma2 - log_gamma2_min) / step)
    ind_gamma = max(ind_gamma, 1) - 1
    ind_gamma = min(ind_gamma, N_gamma2 - N_interp)
    interp_gamma = \
        log_gamma2_min + \
        np.arange(ind_gamma, ind_gamma + N_interp).astype(float) * step

    gaunt = np.zeros(wave.shape)
    for i, _log_u in enumerate(log_u):
        ind_u = int((_log_u - log_u_min) / step)
        ind_u = max(ind_u, 1) - 1
        ind_u = min(ind_u, N_u - N_interp)

        interp_gaunt = np.zeros(N_interp)
        for j in range(N_interp):
            interp_gaunt[j] = interp_lagrange(
                log_gamma2,
                interp_gamma,
                gaunt_table[ind_u:ind_u + N_interp, ind_gamma]
            )

        interp_u = \
            log_u_min + np.arange(ind_u, ind_u + N_interp).astype(float) * step

        _gaunt = interp_lagrange(_log_u, interp_u, interp_gaunt)
        gaunt[i] = _gaunt

    return gaunt


def kappa_ff(
    wave: np.ndarray,
    T: float,
) -> float | np.ndarray:
    Z = 1.   # Hydrogen
    nu = c / (wave * 1.e-8)

    gaunt = interpolate_gaunt(wave, T)
    u = h * c / (wave * 1e-8 * k_B * T)

    # Calculate
    kappa = 3.692e8 * (1. - np.exp(-u)) * Z**2 * gaunt / (np.sqrt(T) * nu**3)

    return kappa


def ff(
    wave: np.ndarray,
    T: float,
    a: float = 1.,
) -> float | np.ndarray:
    kappa = kappa_ff(wave, T)
    j_lam = a * kappa * planck(wave, T)

    return j_lam
