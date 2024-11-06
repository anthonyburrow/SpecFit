#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "planck.hpp"
#include "freeFree.hpp"

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

    // This de-vectorizes `T` and `a` arguments, but it doesn't really improve
    // performance...
    // module_handle.def(
    //     "planck",
    //     [](const py::array_t<double> &wave,
    //        const double& TPlanck,
    //        const double& aPlanck)
    //     {
    //         return py::vectorize(
    //             [&TPlanck, &aPlanck](const double& wave)
    //             {
    //                 return planck(wave, TPlanck, aPlanck);
    //             }
    //         )(std::move(wave));
    //     },
    //     py::arg("wave"), py::arg("T_planck"), py::arg("a_planck") = 1.0
    // );
    module_handle.def(
        "ff",
        &jFF,
        py::arg("wave"), py::arg("T_ff"), py::arg("a_ff") = 1.0,
        py::arg("gaunt_params"), py::arg("gaunt_table")
    );
}
