#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <iostream>

#include "constants.hpp"
#include "planck.hpp"

namespace py = pybind11;

double kappaFF(const double& wave, const double& TFF)
{
    return 1.0;
}


py::array_t<double> jFF(
    const py::array_t<double>& wave, const double& TFF, const double& aFF,
    const py::dict& gauntParams, const py::array_t<double>& gauntTable)
{
    py::buffer_info waveBuffer = wave.request();
    py::buffer_info gauntBuffer = gauntTable.request();
    // gauntParams["N_u"].cast<int>()

    py::array_t<double> out = py::array_t<double>(waveBuffer.size);
    py::buffer_info outBuffer = out.request();

    double* wavePtr = static_cast<double*>(waveBuffer.ptr);
    double* outPtr = static_cast<double*>(outBuffer.ptr);

    // Read table

    double kappa;
    double w;
    for (size_t i = 0; i < waveBuffer.shape[0]; i++)
    {
        // Because wave.request() requested the entire (N, 3) spectrum
        w = wavePtr[i * 3];
        kappa = kappaFF(w, TFF);
        outPtr[i] = aFF * kappa * planck(w, TFF, 1.0);
    }

    return out;
}

