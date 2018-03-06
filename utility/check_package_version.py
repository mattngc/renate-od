#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from scipy import __version__ as scipy__version__
from numpy import __version__ as numpy__version__
from matplotlib import __version__ as matplotlib__version__
from h5py import __version__ as h5py__version__
import warnings

"""
CHECK_PACKAGE_VERSION

AUTHOR: Miklos Vecsei
        Wigner Research Centre for Physics
        Department of Plasma Physics

PURPOSE: This program checks whether the system it is ran on is compatible with
renate_od.  It can be used as a library of functions to check the validity of
single packages. It can be also run as a stand-alone program to check all
packages. If there is a problem with the packages, running the code from the
command line as
$ python check_package_version.py 1
will print out more information about exactly which packages are problematic.

INPUT: print_warn_in - an optional input from the command line

VERSION INFO:
    Created using Python 3.6.4 |Anaconda custom (64-bit)
    Package versions:
        numpy: 1.14.0
        scipy: 1.0.0
        matplotlib: 2.1.12
        h5py: 2.7.1
    Checked on Ubuntu 16.04
    Last Revision: 06.03.2018
"""


def check_sys_version(print_info=0):
    """Checking whether the Python version is compatible with the renate_od code"""

    # The following list contains all verified versions of Python. If it is
    # found that another version of Python is also compatible with renate_od,
    # please expand the list accordingly.
    valid_sys_version = ['3.6.4']
    version_ok = True
    local_sys_version = str(sys.version_info[0]) + '.' + \
        str(sys.version_info[1]) + '.' + str(sys.version_info[2])
    if not (local_sys_version in valid_sys_version):
        if print_info:
            warnings.warn('The code has been verified for Python versions:'
                          + str(valid_sys_version) + '. Your version is '
                          + str(sys.version_info[0]) + '.' +
                          str(sys.version_info[1]) + '.' +
                          str(sys.version_info[2]))
        version_ok = False
    return version_ok


def check_scipy_version(print_info=0):
    """Checking whether the scipy package is compatible with the renate_od code"""

    # The following list contains all verified versions of scipy. If it is
    # found that another version of Python is also compatible with renate_od,
    # please expand the list accordingly.
    valid_scipy_version = ['1.0.0']
    version_ok = True
    if not (scipy__version__ in valid_scipy_version):
        if print_info:
            warnings.warn('The code has been verified for scipy version '
                          + str(valid_scipy_version) + '. Your version is '
                          + scipy__version__)
        version_ok = False
    return version_ok


def check_numpy_version(print_info=0):
    """Checking whether the numpy package is compatible with the renate_od code"""

    # The following list contains all verified versions of numpy. If it is
    # found that another version of Python is also compatible with renate_od,
    # please expand the list accordingly.
    valid_numpy_version = ['1.14.0']
    version_ok = True
    if not (numpy__version__ in valid_numpy_version):
        if print_info:
            warnings.warn('The code has been verified for numpy version '
                          + str(valid_numpy_version) + '. Your version is '
                          + numpy__version__)
        version_ok = False
    return version_ok


def check_matplotlib_version(print_info=0):
    """Checking whether the matplotlib package is compatible with the renate_od code"""

    # The following list contains all verified versions of matplotlib. If it is
    # found that another version of Python is also compatible with renate_od,
    # please expand the list accordingly.
    valid_matplotlib_version = ['2.1.2']
    version_ok = True
    if not (matplotlib__version__ in valid_matplotlib_version):
        if print_info:
            warnings.warn('The code has been verified for matplotlib version '
                          + str(valid_matplotlib_version)
                          + '. Your version is ' + matplotlib__version__)
        version_ok = False
    return version_ok


def check_h5py_version(print_info=0):
    """Checking whether the h5py package is compatible with the renate_od code"""

    # The following list contains all verified versions of h5py. If it is
    # found that another version of Python is also compatible with renate_od,
    # please expand the list accordingly.
    valid_h5py_version = ['2.7.1']
    version_ok = True
    if not (h5py__version__ in valid_h5py_version):
        if print_info:
            warnings.warn('The code has been verified for h5py version '
                          + str(valid_h5py_version) + '. Your version is '
                          + h5py__version__)
        version_ok = False
    return version_ok


def check_all_packages(print_warn=0):
    """Checking whether all packages are compatible with the renate_od code"""
    return check_sys_version(print_info=print_warn) \
        * check_scipy_version(print_info=print_warn) \
        * check_numpy_version(print_info=print_warn) \
        * check_matplotlib_version(print_info=print_warn) \
        * check_h5py_version(print_info=print_warn)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_warn_in = 0
    else:
        print_warn_in = sys.argv[1]

    package_check = check_all_packages(print_warn=print_warn_in)

    if package_check:
        print('Your version of Python packages has been verified and IS '
              'compatible with renate_od.')
    else:
        print('Your version of Python packages has not been verified and IS '
              'POSSIBLY NOT compatible with renate_od.')
