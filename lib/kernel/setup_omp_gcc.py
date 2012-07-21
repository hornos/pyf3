#! /usr/bin/env python

# System imports
from distutils.core import *
from distutils      import sysconfig

# Third-party modules - we depend on numpy for everything
import numpy

# Obtain the numpy include directory.
numpy_include = numpy.get_include()


_vsueig_omp = Extension("_vsueig_omp",
                   ["vsueig_omp_wrap.c",
                    "vsueig_omp.c", "kernel.c"],
                   include_dirs = [numpy_include],
                   libraries=['m'],
                   extra_compile_args=['-O3','-fopenmp'],
                   extra_link_args=['-O3','-fopenmp'],
                   )

setup(name        = "kernel",
      description = "OMP C kernel functions",
      author      = "tom.hornos",
      py_modules  = ["vsueig_omp"],
      ext_modules = [_vsueig_omp]
      )
