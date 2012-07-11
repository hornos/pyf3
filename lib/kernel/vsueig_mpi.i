%module vsueig_mpi

%{
#define SWIG_FILE_WITH_INIT
#include "vsueig_mpi.h"
%}

%include "numpy.i"
%init %{
import_array();
%}

%include "mpi4py/mpi4py.i"
%mpi4py_typemap(Comm, MPI_Comm);

%define %apply_numpy_typemaps(TYPE)
%apply (int DIM1, TYPE* INPLACE_ARRAY1)
      {(int dim1, TYPE* array1)};

%apply (int DIM1, TYPE* INPLACE_ARRAY1)
      {(int dim1, TYPE* array1)};

%apply (int DIM1, int DIM2, TYPE* INPLACE_ARRAY2)
      {(int dim1, int dim2, TYPE* array2)};

%apply (int DIM1, int DIM2, TYPE* INPLACE_ARRAY2)
      {(int dim1_1, int dim2_1, TYPE* array2_1),
       (int dim1_2, int dim2_2, TYPE* array2_2)};


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

%include "vsueig_mpi.h"
