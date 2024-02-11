from setuptools import setup
from setuptools.command.install import install
import subprocess
import platform

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='DiSH',
    version='Latest',

    author='Khaled Sayed',
    #author_email='',
    description='A Hybrid Element-based Model Simulator: Dynamic Cell Signalling Networks',
    lience='MIT',
    keywords='Dynamic',

    packages=['src'],
    include_package_data=True,

    install_requires=[
        'networkx>=2.5',
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'scipy',
        'statsmodels',
        'scikit-learn',
        'openpyxl',
        ],
    python_requires='>=3.6, <=3.9.13',
    zip_safe=False
)