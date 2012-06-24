/* module kernel.test */

#include <stdio.h>
#include "test.h"

int i64v_kernel(int dim1, long *array1) {
  int i=0;
  printf("%s: ",__FUNCTION__);
  for(i=0;i<dim1;++i)
    printf("%3ld",array1[i]);
  printf("\n");
  array1[0] = 10000;
  return 0;
}

int i64m_kernel(int dim1, int dim2, long *array2) {
  int i=0;
  int j=0;
  printf("%s: %d %d\n",__FUNCTION__,dim1,dim2);
  for(i=0;i<dim1;++i) {
    for(j=0;j<dim2;++j)
      printf("%3ld",array2[i*dim2+j]);
    printf("\n");
  }
  array2[0] = 10000;
  return 0;
}

int f64_kernel(int dim1, double *array1) {
  int i=0;
  printf("%s: ",__FUNCTION__);
  for(i=0;i<dim1;++i)
    printf("%9.6lf",array1[i]);
  printf("\n");
  array1[0] = 30000.0;
  return 0;
}
