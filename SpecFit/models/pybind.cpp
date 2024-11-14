#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "planck.hpp"
#include "freeFree.hpp"
#include "gaussian.hpp"

using namespace std;
namespace py = pybind11;

PYBIND11_MODULE(SpecFitModels, module_handle) {
    module_handle.doc() = "Spectrum models.";

    // Planck function
    module_handle.def(
        "planck",
        &planck,
        py::arg("wave"), py::arg("T_planck"), py::arg("a_planck") = 1.0
    );
    // Free-free
    module_handle.def(
        "ff",
        &jFF,
        py::arg("wave"), py::arg("T_ff"), py::arg("a_ff") = 1.0,
        py::arg("gaunt_params"), py::arg("gaunt_table")
    );
    // Gaussian
    module_handle.def(
        "gaussian",
        &gaussian,
        py::arg("wave"), py::arg("mean_gaussian"), py::arg("std_gaussian"),
        py::arg("a_gaussian") = 1.0
    );
}
