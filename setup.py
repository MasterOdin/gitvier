#!/usr/bin/env python

"""Setup script for the package."""

import os
import sys
import setuptools

from gitvier import __project__, __version__, __author__, DESCRIPTION

PACKAGE_NAME = "gitvier"
MINIMUM_PYTHON_VERSION = (3, 5)


def check_python_version():
    """Exit when the Python version is too low."""
    if sys.version_info < MINIMUM_PYTHON_VERSION:
        sys.exit("Python {0}.{1}+ is required.".format(*MINIMUM_PYTHON_VERSION))


def read_descriptions():
    """Build a description for the project from documentation files."""
    try:
        readme = open("README.rst").read()
    except IOError:
        return "<placeholder>"
    else:
        return readme


check_python_version()

setuptools.setup(
    name=__project__,
    version=__version__,
    author=__author__,
    author_email='matt.peveler@gmail.com',
    description=DESCRIPTION,
    long_description=read_descriptions(),
    url='https://github.com/MasterOdin/gitvier',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': [
        'gitvier = gitvier.cli:main'
    ]},
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Version Control',
        'Topic :: System :: Software Distribution'
    ],
    install_requires=[
        'GitPython',
        'PyYAML'
    ]
)
