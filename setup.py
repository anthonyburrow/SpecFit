from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext
import glob

__version__ = "0.0.1"

ext_modules = [
    Pybind11Extension(
        "SpecFitModels",
        glob.glob("SpecFit/models/*.cpp"),
        define_macros=[("VERSION_INFO", __version__)],
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
