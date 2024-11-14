#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>

#include "constants.hpp"

namespace py = pybind11;

double gaussianFunc(
    const double& wave,
    const double& meanGaussian,
    const double& stdGaussian)
{
    const double MDist = (wave - meanGaussian) / stdGaussian;
    const double expTerm = exp(-0.5 * pow(MDist, 2.0));
    const double norm = 1.0 / (stdGaussian * sqrt(2.0 * pi));

    const double gaussian = norm * expTerm;

    return gaussian;
}

py::array_t<double> gaussian(
    py::array_t<double>& wave,
    const double& meanGaussian,
    const double& stdGaussian,
    const double& aGaussian)
{
    py::buffer_info waveBuffer = wave.request();

    py::array_t<double> out = py::array_t<double>(waveBuffer.size);
    py::buffer_info outBuffer = out.request();

    double* wavePtr = static_cast<double*>(waveBuffer.ptr);
    double* outPtr = static_cast<double*>(outBuffer.ptr);

    double w;
    const double arbitraryScale = 1e2;
    const int dim = wave.strides(0) / 8;
    for (int i = 0; i < waveBuffer.shape[0]; i++)
    {
        w = wavePtr[i * dim];
        outPtr[i] = gaussianFunc(w, meanGaussian, stdGaussian);
        outPtr[i] *= arbitraryScale * aGaussian;
    }

    return out;
}
