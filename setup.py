from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, find_namespace_packages
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
    # Package info
    name='SpecFit',
    version=__version__,
    description='Spectrum fitter using lmfit.',
    url='https://github.com/anthonyburrow/SpecFit',
    author='Anthony Burrow',
    author_email='anthony.r.burrow@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Science/Research',
    ],
    # Dependencies
    install_requires=['numpy', 'scipy', 'lmfit'],
    optional=['matplotlib'],
    extras_require={'test': ['pytest', 'requests']},
    # Package installation
    packages=find_namespace_packages(where='SpecFit'),
    package_dir={'': 'SpecFit'},
    include_package_data=True,
    package_data={
        'SpecFit.data': ['*.dat']
    },
    # External
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)
