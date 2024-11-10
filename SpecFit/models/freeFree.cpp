#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <iostream>

#include "constants.hpp"
#include "planck.hpp"

using namespace std;
namespace py = pybind11;

double calcFreq(const double& wave)
{
    const double nu = c / (wave * 1e-8);
    return nu;
}

double interpLagrange(
    const double &x,
    const vector<double>& xTable,
    const vector<double>& yTable)
{
    double y = 0.0;

    const size_t N = xTable.size();
    for (int i = 0; i < N; i++)
    {
        double coeff = 1.0;
        for (int j = 0; j < N; j++)
        {
            if (i == j) { continue; }
            coeff *= (x - xTable[j]) / (xTable[i] - xTable[j]);
        }
        y += yTable[i] * coeff;
    }

    return y;
}

double interpolateGaunt(
    const double& wave,
    const double& TFF,
    const py::dict& gauntParams,
    const py::array_t<double>& gauntTable)
{
    const int NInterp = 4;

    const double& logGamma2Min = gauntParams["log_gamma2_min"].cast<double>();
    const double& logUMin = gauntParams["log_u_min"].cast<double>();
    const int& NGamma2 = gauntParams["N_gamma2"].cast<int>();
    const int& NU = gauntParams["N_u"].cast<int>();
    const double& step = gauntParams["step"].cast<double>();

    const double nu = calcFreq(wave);
    const double u = h * nu / (kB * TFF);
    const double gamma2 = h * c * Ryd / (kB * TFF);

    const double logU = log10(u);
    const double logGamma2 = log10(gamma2);

    // Setup gamma2 points for interpolation
    // TODO: Gamma2 part should go outside this function scope for efficiency
    int indGamma2 = static_cast<int>((logGamma2 - logGamma2Min) / step);
    indGamma2 = max(indGamma2, 1) - 1;
    indGamma2 = min(indGamma2, NGamma2 - NInterp);

    vector<double> interpGamma2(NInterp);
    double addedLogGamma2;
    for (int i = 0; i < NInterp; i++)
    {
        addedLogGamma2 = static_cast<double>(indGamma2 + i) * step;
        interpGamma2[i] = logGamma2Min + addedLogGamma2;
    }

    // Setup u points for interpolation
    int indU = static_cast<int>((logU - logUMin) / step);
    indU = max(indU, 1) - 1;
    indU = min(indU, NU - NInterp);

    vector<double> interpU(NInterp);
    double addedLogU;
    for (int i = 0; i < NInterp; i++)
    {
        addedLogU = static_cast<double>(indU + i) * step;
        interpU[i] = logUMin + addedLogU;
    }

    // Interpolate across gamma2 dimension
    const py::buffer_info gauntBuffer = gauntTable.request();
    auto gauntTableValues = static_cast<double*>(gauntBuffer.ptr);
    vector<double> interpTable(NInterp);
    for (int i = 0; i < NInterp; i++)
    {
        // gauntTableValues is flattened 2D -> 1D so this indexing is necessary
        interpTable[i] = gauntTableValues[NGamma2 * (indU + i) + indGamma2];
    }

    vector<double> interpGaunt(NInterp);
    for (int i = 0; i < NInterp; i++)
    {
        interpGaunt[i] = interpLagrange(
            logGamma2, interpGamma2, interpTable
        );
    }

    // Interpolate gamma2 interpolations across u
    const double gaunt = interpLagrange(
        logU, interpU, interpGaunt
    );

    return gaunt;
}


double kappaFF(
    const double& wave,
    const double& TFF,
    const py::dict& gauntParams,
    const py::array_t<double>& gauntTable)
{
    const double gaunt = interpolateGaunt(wave, TFF, gauntParams, gauntTable);
    const double Z = 1.0;   // Hydrogen
    const double nu = calcFreq(wave);
    const double u = h * nu / (kB * TFF);

    const double kappa = 3.692e8 * (1.0 - exp(-u)) * pow(Z, 2.0) * gaunt / (sqrt(TFF) * pow(nu, 3.0));

    return kappa;
}


py::array_t<double> jFF(
    const py::array_t<double>& wave,
    const double& TFF,
    const double& aFF,
    const py::dict& gauntParams,
    const py::array_t<double>& gauntTable)
{
    py::buffer_info waveBuffer = wave.request();

    py::array_t<double> out = py::array_t<double>(waveBuffer.size);
    py::buffer_info outBuffer = out.request();

    double* wavePtr = static_cast<double*>(waveBuffer.ptr);
    double* outPtr = static_cast<double*>(outBuffer.ptr);

    double kappa;
    double w;
    const double arbitraryScale = 1e31;
    for (int i = 0; i < waveBuffer.shape[0]; i++)
    {
        // Because wave.request() requested the entire (N, 3) spectrum
        w = wavePtr[i * 3];
        kappa = kappaFF(w, TFF, gauntParams, gauntTable);
        outPtr[i] = arbitraryScale * aFF * kappa * planckFunc(w, TFF, 1.0);
    }

    return out;
}

