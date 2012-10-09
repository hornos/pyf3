# Common kernel functions
KERNEL     = kernel.c kernel.h

# SWIG Interface
# OpenMP
IFC_OMP = vsueig_omp.i
SRC_OMP = vsueig_omp.c
HDR_OMP = vsueig_omp.h
WRP_OMP = $(IFC_OMP:.i=_wrap.c)
PRX_OMP = $(IFC_OMP:.i=.py    )

# MPI
IFC_MPI = vsueig_mpi.i
SRC_MPI = vsueig_mpi.c
HDR_MPI = vsueig_mpi.h
WRP_MPI = $(IFC_MPI:.i=_wrap.c)
PRX_MPI = $(IFC_MPI:.i=.py    )

SWG_INC = -I$(MPI4PY_HOME)/mpi4py/include

# Targets
.PHONY : all

all: omp

omp: $(WRP_OMP) $(SRC_OMP) $(HDR_OMP) $(KERNEL)
	./setup_omp_gcc.py build_ext --inplace

# numpy edit: /opt/local/Library/Frameworks/Python.framework/Versions/Current/lib/python2.7/distutils
omp-intel: $(WRP_OMP) $(SRC_OMP) $(HDR_OMP) $(KERNEL)
	./setup_omp_intel.py build_ext --inplace -c intel

mpi: $(WRP_MPI) $(SRC_MPI) $(HDR_MPI) $(KERNEL)
	./setup_mpi.py build_ext --inplace

# Rule: %.i -> %_wrap.cxx
%_wrap.c: %.i %.h numpy.i
	swig $(SWG_INC) -python $<

vsueig_omp.c: vsueig_omp.h $(KERNEL)
vsueig_omp.h:
kernel.h:

vsueig_mpi.c: vsueig_mpi.h $(KERNEL)
vsueig_mpi.h:

# Clean target
.PHONY : clean
clean:
	$(RM) -r build
	$(RM) *.so
	$(RM) $(WRP_OMP) $(WRP_MPI)
	$(RM) $(PRX_OMP) $(PRX_MPI)
