#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>

#include "constants.hpp"

namespace py = pybind11;

double lorentzianFunc(
    const double& wave,
    const double& meanLorentzian,
    const double& fwhmLorentzian)
{

    const double hwhm = fwhmLorentzian * 0.5;
    const double dist = wave - meanLorentzian;
    const double ratio = hwhm / (pow(dist, 2.0) + pow(hwhm, 2.0));

    const double lorentzian = ratio / pi;

    return lorentzian;
}

py::array_t<double> lorentzian(
    py::array_t<double>& wave,
    const double& meanLorentzian,
    const double& fwhmLorentzian,
    const double& aLorentzian)
{
    py::buffer_info waveBuffer = wave.request();

    py::array_t<double> out = py::array_t<double>(waveBuffer.size);
    py::buffer_info outBuffer = out.request();

    double* wavePtr = static_cast<double*>(waveBuffer.ptr);
    double* outPtr = static_cast<double*>(outBuffer.ptr);

    double w;
    const double arbitraryScale = 1.66e2;
    const int dim = wave.strides(0) / 8;
    for (int i = 0; i < waveBuffer.shape[0]; i++)
    {
        w = wavePtr[i * dim];
        outPtr[i] = lorentzianFunc(w, meanLorentzian, fwhmLorentzian);
        outPtr[i] *= arbitraryScale * aLorentzian;
    }

    return out;
}
