#pragma once

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

double lorentzianFunc(
    const double& wave,
    const double& meanLorentzian,
    const double& fwhmLorentzian,
    const double& aLorentzian
);
py::array_t<double> lorentzian(
    py::array_t<double>& wave,
    const double& meanLorentzian,
    const double& fwhmLorentzian,
    const double& aLorentzian
);
