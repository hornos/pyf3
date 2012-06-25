#! /usr/bin/env python

# System imports
from distutils.core import *
from distutils      import sysconfig

# Third-party modules - we depend on numpy for everything
import numpy

# Obtain the numpy include directory.
numpy_include = numpy.get_include()

_test = Extension("_test",
                   ["test_wrap.c",
                    "test.c"],
                   include_dirs = [numpy_include],
                   )

_vsueig = Extension("_vsueig",
                   ["vsueig_wrap.c",
                    "vsueig.c"],
                   include_dirs = [numpy_include],
                   libraries=['m'],
                   extra_compile_args=['-fopenmp'],
                   extra_link_args=['-fopenmp'],
                   )

setup(name        = "kernel",
      description = "C kernel functions",
      author      = "HT",
      py_modules  = ["test", "vsueig"],
      ext_modules = [_test, _vsueig]
      )
