#include "kernel.h"
#include "vsueig_mpi.h"

void gendos(MPI_Comm comm, double amp, double sig, int dim1_1, int dim2_1, double *array2_1, int dim1_2, int dim2_2, double *array2_2 ) {
  // Array interface
  int i_range = dim1_1;
  int j_range = dim2_2;
  int i,j,size,rank;

  double *inp_grid = array2_1;
  double *inp_comp_grid = array2_2;

  // Gauss parameters
  double mu, A, x, gw;

  // Timing
  clock_t t = -clock(), wt;

  // MPI
  MPI_Comm_size(comm, &size);
  MPI_Comm_rank(comm, &rank); 

  // ditch out high ranks
  if( rank > 1 )
    return;

  // io node
  if( rank == 0 ) {
    printf( "MPI C kernel: %s (%s)\n", __FUNCTION__, __FILE__ );
    printf("%5s %8s %8s\n", "Array", "dim1", "dim2");
    printf( "%5d %8d %8d\n", 1, dim1_1, dim2_1 );
    printf( "%5d %8d %8d\n", 2, dim1_2, dim2_2 );
    printf("MPI Procs: %d\n", size);
    t = -clock();
  }

  // array indexes
  i_range = dim1_1;
  j_range = dim2_2;

  gw = CUTOFF * sig;

  // serial fallback
  if( size == 1 ) {
    wt = -clock();
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
    wt += clock();
    printf("%2d/%2d wtime: %9.6lf s\n", 1, 1, wt/((double)CLOCKS_PER_SEC));
    goto end;
  }


  if( rank == 0 ) {
    wt = -clock();
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
    wt += clock();
    printf("%2d/%2d wtime: %9.6lf s\n", rank, size, wt/((double)CLOCKS_PER_SEC));
  }

  if( rank == 1 ) {
    wt = -clock();
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
    wt += clock();
    printf("%2d/%2d wtime: %9.6lf s\n", rank, size, wt/((double)CLOCKS_PER_SEC));
  }

end:
  MPI_Barrier(comm);
  if( rank == 0 ) {
    t += clock();
    printf("       time: %9.6lf s\n",t/((double)CLOCKS_PER_SEC));
  }
}
