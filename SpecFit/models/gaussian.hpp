#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

double gaussianFunc(
    const double& wave,
    const double& meanGaussian,
    const double& stdGaussian,
    const double& aGaussian
);
py::array_t<double> gaussian(
    py::array_t<double>& wave,
    const double& meanGaussian,
    const double& stdGaussian,
    const double& aGaussian
);
