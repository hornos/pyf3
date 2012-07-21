#include "kernel.h"
#include "vsueig_omp.h"

void gendos(double amp, double sig, int dim1_1, int dim2_1, double *array2_1, int dim1_2, int dim2_2, double *array2_2 ) {
  // Array interface
  int i_range = dim1_1;
  int j_range = dim2_2;
  int i,j,threads=1;

  double *inp_grid = array2_1;
  double *inp_comp_grid = array2_2;

  // Gauss parameters
  double mu, A, x, gw;

  // Timing
  clock_t t;
  double wt;

#ifdef INTEL
  printf( "Intel OMP C kernel: %s (%s)\n", __FUNCTION__, __FILE__ );
#else
  printf( "GCC OMP C kernel: %s (%s)\n", __FUNCTION__, __FILE__ );
#endif
  printf("%5s %8s %8s\n", "Array", "dim1", "dim2");
  printf( "%5d %8d %8d\n", 1, dim1_1, dim2_1 );
  printf( "%5d %8d %8d\n", 2, dim1_2, dim2_2 );

  t = -clock();

  i_range = dim1_1;
  j_range = dim2_2;

  gw = CUTOFF * sig;

#ifdef _OPENMP
  threads = omp_get_max_threads();
  printf("OpenMP Threads: %d\n", threads);

#pragma omp parallel private(i,j,mu,A,x,wt)
{

#pragma omp sections nowait
{

#pragma omp section
{
  wt = -omp_get_wtime();
  for( i = 0; i < i_range; i++ ) {
    mu = cij(dim1_1,dim2_1,inp_grid,i,0);
    A  = cij(dim1_1,dim2_1,inp_grid,i,1) * amp;
    for( j = 0; j < j_range; j++ ) {
      x = cij(dim1_2,dim2_2,inp_comp_grid,0,j);
      if( abs( x - mu ) > gw )
        continue;
      sij(dim1_2,dim2_2,inp_comp_grid,1,j,gauss(x,A,mu,sig));
    }
  }
  wt += omp_get_wtime();
  printf("%2d/%2d wtime: %9.6lf s\n", omp_get_thread_num(), threads, wt);
}

#pragma omp section
{
  wt = -omp_get_wtime();
  for( i = 0; i < i_range; i++ ) {
    mu = cij(dim1_1,dim2_1,inp_grid,i,0);
    A  = cij(dim1_1,dim2_1,inp_grid,i,1) * amp;
    for( j = 0; j < j_range; j++ ) {
      x = cij(dim1_2,dim2_2,inp_comp_grid,0,j);
      if( abs( x - mu ) > gw )
        continue;
      sij(dim1_2,dim2_2,inp_comp_grid,2,j,dgauss(x,A,mu,sig));
    }
  }
  wt += omp_get_wtime();
  printf("%2d/%2d wtime: %9.6lf s\n", omp_get_thread_num(), threads, wt);
}

} // sections
} // parallel
// omp parallel end

// serial
#else
  for( i = 0; i < i_range; i++ ) {
    mu = cij(dim1_1,dim2_1,inp_grid,i,0);
    A  = cij(dim1_1,dim2_1,inp_grid,i,1) * amp;
    for( j = 0; j < j_range; j++ ) {
      x = cij(dim1_2,dim2_2,inp_comp_grid,0,j);
      if( abs( x - mu ) > gw )
        continue;
      sij(dim1_2,dim2_2,inp_comp_grid,1,j,gauss(x,A,mu,sig));
      sij(dim1_2,dim2_2,inp_comp_grid,2,j,dgauss(x,A,mu,sig));
    }
  }
#endif

  t += clock();
  printf("       time: %9.6lf s\n",t/((double)CLOCKS_PER_SEC*threads));
}
