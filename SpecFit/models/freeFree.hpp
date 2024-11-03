#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;


double kappaFF(
    const double& wave,
    const double& TFF
);
py::array_t<double> jFF(
    const py::array_t<double>& wave,
    const double& TFF,
    const double& aFF,
    const py::dict& gauntParams,
    const py::array_t<double>& gauntTable
);
