import setuptools
from setuptools import setup


setup(
    name='SpecFit',
    version='0.1',
    description='Spectrum fitter using lmfit.',
    url='https://github.com/anthonyburrow/SpecFit',
    author='Anthony Burrow',
    author_email='anthony.r.burrow@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=['numpy', 'scipy>=1.3.0,<=1.12.0', 'lmfit'],
    optional=['matplotlib'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
        'Intended Audience :: Science/Research',
    ]
)
