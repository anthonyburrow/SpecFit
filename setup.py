from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, find_packages
import glob


__version__ = '0.0.1'

src_files = glob.glob('SpecFit/models/*.cpp')

ext_modules = [
    Pybind11Extension(
        'SpecFitModels',
        src_files,
        define_macros=[('VERSION_INFO', __version__)]
    ),
]

setup(
    name='SpecFit',
    version=__version__,
    description='Spectrum fitter using lmfit.',
    url='https://github.com/anthonyburrow/SpecFit',
    author='Anthony Burrow',
    author_email='anthony.r.burrow@gmail.com',
    license='MIT',
    include_package_data=True,
    install_requires=['numpy', 'scipy', 'lmfit'],
    optional=['matplotlib'],
    packages=find_packages(),
    ext_modules=ext_modules,
    extras_require={'test': ['pytest', 'requests']},
    cmdclass={'build_ext': build_ext},
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Science/Research',
    ]
)
