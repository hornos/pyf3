# SWIG
INTERFACES = test.i vsueig.i
WRAPPERS   = $(INTERFACES:.i=_wrap.c)
PROXIES    = $(INTERFACES:.i=.py    )

# Default target: build the tests
.PHONY : all
all: $(WRAPPERS) test.c test.h vsueig.c vsueig.h kernel.h
	./setup.py build_ext -i

# Rule: %.i -> %_wrap.cxx
%_wrap.c: %.i %.h numpy.i
	swig -python $<

# Clean target
.PHONY : clean
clean:
	$(RM) -r build
	$(RM) *.so
	$(RM) $(WRAPPERS)
	$(RM) $(PROXIES)
