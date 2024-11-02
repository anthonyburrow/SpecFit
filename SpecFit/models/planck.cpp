// #include <pybind11/pybind11.h>
// #include <pybind11/numpy.h>
#include <cmath>

#include "constants.hpp"

// namespace py = pybind11;

double planck(const double& wave, const double& TPlanck, const double& aPlanck)
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

// py::array_t<double> planck(py::array_t<double> wave, double& TPlanck, double& aPlanck)
// {
//     const double waveCm = wave * 1e-8;

//     const double expTerm = exp(-h * c / (waveCm * kB * TPlanck));
//     double planck = (2.0 * h * pow(c, 2.0) / pow(waveCm, 5.0)) * expTerm / (1.0 - expTerm);
//     planck *= aPlanck * 1e-8;

//     if (planck < 0.0)
//     {
//         return 0.0;
//     }

//     return planck;
// }
