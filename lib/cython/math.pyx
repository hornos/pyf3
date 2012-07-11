from libc.math cimport exp

def gauss( double x, double A = 1.0, double mu = 0.0, double sigma = 1.0 ):
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
  y = x - mu
  return A * exp( - y * y / ( 2.0 * sigma * sigma ) )
# end def

def dgauss( double x, double A = 1.0, double mu = 0.0, double sigma = 1.0 ):
  """
  Evaluate the 1st Derivative of a Gaussian.

  Parameters
  ----------
  A : float
      Amplitude.
  mu : float
      Mean.
  std : float
      Standard deviation.

  """
  return  - (x - mu) / ( sigma * sigma ) * gauss( x, A, mu, sigma ) 
# end def
