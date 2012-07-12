#! /usr/bin/env python

# System imports
from distutils.core import *
from distutils      import sysconfig

# Third-party modules - we depend on numpy for everything
import numpy

# Obtain the numpy include directory.
numpy_include = numpy.get_include()

# MPI
import os
mpi_root = os.getenv("MPI_ROOT")
mpi_inc = "-I" + mpi_root + "/include"
mpi_lib = "-L" + mpi_root + "/lib"

mpi4py_root = os.getenv("MPI4PY_HOME")
mpi4py_inc  = "-I" + mpi4py_root + "/mpi4py/include"


_vsueig_mpi = Extension("_vsueig_mpi",
                   ["vsueig_mpi_wrap.c",
                    "vsueig_mpi.c", "kernel.c"],
                   include_dirs = [numpy_include],
                   libraries=['m'],
                   extra_compile_args=['-DMPI', mpi_inc, mpi4py_inc],
                   extra_link_args=[mpi_lib,'-lmpi'],
                   )

setup(name        = "kernel",
      description = "MPI C kernel functions",
      author      = "tom.hornos",
      py_modules  = ['vsueig_mpi'],
      ext_modules = [_vsueig_mpi]
      )
