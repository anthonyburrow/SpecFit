#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>

#include "constants.hpp"

namespace py = pybind11;

double planckFunc(
    const double& wave,
    const double& TPlanck,
    const double& aPlanck)
{
    const double waveCm = wave * 1e-8;

    const double expTerm = exp(-h * c / (waveCm * kB * TPlanck));
    double planck = (2.0 * h * pow(c, 2.0) / pow(waveCm, 5.0)) * expTerm / (1.0 - expTerm);
    planck *= aPlanck * 1e-8;

    if (planck < 0.0)
    {
        return 0.0;
    }

    return planck;
}

py::array_t<double> planck(
    py::array_t<double>& wave,
    double& TPlanck,
    double& aPlanck)
{
    py::buffer_info waveBuffer = wave.request();

    py::array_t<double> out = py::array_t<double>(waveBuffer.size);
    py::buffer_info outBuffer = out.request();

    double* wavePtr = static_cast<double*>(waveBuffer.ptr);
    double* outPtr = static_cast<double*>(outBuffer.ptr);

    double w;
    const double arbitraryScale = 1e-7;
    for (int i = 0; i < waveBuffer.shape[0]; i++)
    {
        // Because wave.request() requested the entire (N, 3) spectrum (flattened)
        w = wavePtr[i * 3];
        outPtr[i] = arbitraryScale * aPlanck * planckFunc(w, TPlanck, 1.0);
    }

    return out;
}
