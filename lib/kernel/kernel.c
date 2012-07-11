#include <math.h>

/* Gauss Function
def gauss(x, A=1.0, mu=0.0, sigma=1.0):
  return np.real(A * np.exp(-(x - mu)**2 / (2 * sigma**2)))
*/
double gauss(double x, double A, double mu, double sigma ) {
  double xmu = x-mu;
  return A * exp(- xmu * xmu / ( 2.000 * sigma * sigma ) );
}


/* d/dx Gauss Function
def dgauss(x, A=1.0, mu=0.0, sigma=1.0):
  return  - (x - mu) / (sigma * sigma) * gauss( x, A, mu, sigma ) 
*/
double dgauss(double x, double A, double mu, double sigma ) {
  double xmu = x-mu;
  return - xmu / ( sigma * sigma ) * gauss( x, A, mu, sigma );
}
