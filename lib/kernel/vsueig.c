#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "kernel.h"

/* Gauss Function
def GAUSS(x, A=1.0, mu=0.0, sigma=1.0):
  return np.real(A * np.exp(-(x - mu)**2 / (2 * sigma**2)))
*/
double GAUSS(double x, double A, double mu, double sigma ) {
  double xmu = x-mu;
  return A * exp(- xmu * xmu / ( 2.000 * sigma * sigma ) );
}


/* d/dx Gauss Function
def DGAUSS(x, A=1.0, mu=0.0, sigma=1.0):
  return  - (x - mu) / (sigma * sigma) * GAUSS( x, A, mu, sigma ) 
*/
double DGAUSS(double x, double A, double mu, double sigma ) {
  double xmu = x-mu;
  return - xmu / ( sigma * sigma ) * GAUSS( x, A, mu, sigma );
}


/*
    # inp_grid 2d float
    # inp_comp_grid 2 float
    for i in range(0,i_range):
      mu = inp_grid[i,0]
      A  = inp_grid[i,1]
      # print mu,A
      for j in range(0,j_range):
        x = inp_comp_grid[0,j]
        if abs(x-mu) > 3*sig:
          continue
        # print x
        # fx
        inp_comp_grid[1,j] += GAUSS( x, A , mu, sig )
        # d/dx fx
        inp_comp_grid[2,j] += DGAUSS( x, A, mu, sig )
      # end for
    # end for
*/

// Gauss cutoff
#define CUTOFF 3

void gendos(double sig, int dim1_1, int dim2_1, double *array2_1, int dim1_2, int dim2_2, double *array2_2 ) {
  // Array interface
  int i_range = dim1_1;
  int j_range = dim2_2;
  int i,j;

  double *inp_grid = array2_1;
  double *inp_comp_grid = array2_2;

  // Gauss parameters
  double mu, A, x, gw;

  // Timing
  clock_t t[2];

  printf( "C kernel: %s (%s)\n", __FUNCTION__, __FILE__ );
  printf( "array 1: %6d %6d\n", dim1_1, dim2_1 );
  printf( "array 2: %6d %6d\n", dim1_2, dim2_2 );

  t[0] = clock();

  i_range = dim1_1;
  j_range = dim2_2;

  gw = CUTOFF * sig;
  for( i = 0; i < i_range; i++ ) {
    mu = cij(dim1_1,dim2_1,inp_grid,i,0);
    A  = cij(dim1_1,dim2_1,inp_grid,i,1);
    for( j = 0; j < j_range; j++ ) {
      x = cij(dim1_2,dim2_2,inp_comp_grid,0,j);
      if( abs( x - mu ) > gw )
        continue;
      sij(dim1_2,dim2_2,inp_comp_grid,1,j,GAUSS(x,A,mu,sig));
      sij(dim1_2,dim2_2,inp_comp_grid,2,j,DGAUSS(x,A,mu,sig));
    }
  }

  t[1] = clock();
  printf("Elapsed time: %9.6lf s\n",(t[1]-t[0])/(double)CLOCKS_PER_SEC);
}
