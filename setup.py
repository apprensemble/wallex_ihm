from setuptools import find_packages, setup

setup(
    name='wallex_ihm',
    packages=find_packages(include=['wallex']),
    version='0.0.1.0',
    description='A simple IHM for wallex',
    author='CryptoGrillon',
    install_requires=['selenium','requests','typing','pandas','dash','dash_bootstrap_components','dash_ag_grid','dash_daq','wallex','plotly_express'],
    extras_require={
        'tests': ['pytest'],
    },
)
# pip install setuptools
# pip install pytest
# pip install wheel
# lancement build : python setup.py bdist_wheel
# lancement tests : pytest