%module vsueig

%{
#define SWIG_FILE_WITH_INIT
#include "vsueig.h"
%}

%include "numpy.i"
%init %{
import_array();
%}

%define %apply_numpy_typemaps(TYPE)
%apply (int DIM1, TYPE* INPLACE_ARRAY1)
      {(int dim1, TYPE* array1)};

%apply (int DIM1, TYPE* INPLACE_ARRAY1)
      {(int dim1, TYPE* array1)};

%apply (int DIM1, int DIM2, TYPE* INPLACE_ARRAY2)
      {(int dim1, int dim2, TYPE* array2)};
%enddef
%apply_numpy_typemaps(signed char       )
%apply_numpy_typemaps(unsigned char     )
%apply_numpy_typemaps(short             )
%apply_numpy_typemaps(unsigned short    )
%apply_numpy_typemaps(int               )
%apply_numpy_typemaps(unsigned int      )
%apply_numpy_typemaps(long              )
%apply_numpy_typemaps(unsigned long     )
%apply_numpy_typemaps(long long         )
%apply_numpy_typemaps(unsigned long long)
%apply_numpy_typemaps(float             )
%apply_numpy_typemaps(double            )

%include "vsueig.h"
