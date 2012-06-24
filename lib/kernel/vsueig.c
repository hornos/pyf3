#include <math.h>

/*
def GAUSS(x, A=1.0, mu=0.0, sigma=1.0):
  """
  Evaluate Gaussian.

  Parameters
  ----------
  A : float
      Amplitude.
  mu : float
      Mean.
  std : float
      Standard deviation.

  """
  return np.real(A * np.exp(-(x - mu)**2 / (2 * sigma**2)))
# end def
*/
double GAUSS(double x, double A, double mu, double sigma ) {
  double xmu = x-mu;
  return A * exp(- xmu * xmu / ( 2.000 * sigma * sigma ) );
}

/*
def DGAUSS(x, A=1.0, mu=0.0, sigma=1.0):
  return  - (x - mu) / (sigma * sigma) * GAUSS( x, A, mu, sigma ) 
*/
double DGAUSS(double x, double A, double mu, double sigma ) {
  double xmu = x-mu;
  return - xmu / ( sigma * sigma ) * GAUSS( x, A, mu, sigma );
}
