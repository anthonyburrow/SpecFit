#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

double planckFunc(
    const double& wave,
    const double& TPlanck,
    const double& aPlanck);
py::array_t<double> planck(
    py::array_t<double>& wave,
    double& TPlanck,
    double& aPlanck);
