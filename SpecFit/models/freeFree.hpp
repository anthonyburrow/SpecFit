#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

double calcFreq(const double& wave);
double interpLagrange(
    const double& x,
    const std::vector<double>& xTable,
    const std::vector<double>& yTable
);
double interpolateGaunt(
    const double& wave,
    const double& TFF,
    const py::dict& gauntParams,
    const py::array_t<double>& gauntTable
);
double kappaFF(
    const double& wave,
    const double& TFF,
    const py::dict& gauntParams,
    const py::array_t<double>& gauntTable
);
py::array_t<double> jFF(
    const py::array_t<double>& wave,
    const double& TFF,
    const double& aFF,
    const py::dict& gauntParams,
    const py::array_t<double>& gauntTable
);
