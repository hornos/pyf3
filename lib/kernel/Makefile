# SWIG
INTERFACES = vsueig_omp.i vsueig_mpi.i
SOURCES    = vsueig_omp.c vsueig_mpi.c
HEADERS    = vsueig_omp.h vsueig_mpi.h
KERNEL     = kernel.c kernel.h
WRAPPERS   = $(INTERFACES:.i=_wrap.c)
PROXIES    = $(INTERFACES:.i=.py    )

SWIG_INC   = -I$(MPI4PY_HOME)/mpi4py/include


# Default target: build the tests
.PHONY : all
all: $(WRAPPERS) $(SOURCES) $(HEADERS) $(KERNEL)
	./setup.py build_ext -i

# Rule: %.i -> %_wrap.cxx
%_wrap.c: %.i %.h numpy.i
	swig $(SWIG_INC) -python $<

# Deps
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
	$(RM) $(WRAPPERS)
	$(RM) $(PROXIES)
