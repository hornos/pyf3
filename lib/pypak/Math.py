#
# Types package
#

import sys
import copy
import string
import math as m
import numpy as np
import numpy.linalg as npla

ZERO =  0.0000000000000000000
ONE  =  1.0000000000000000000
MONE = -1.0000000000000000000
HALF =  0.5000000000000000000

def array2float( arr ):
  for i in range( 0, len( arr ) ):
    arr[i] = string.atof( arr[i] )
  # end for
  return np.array( arr )
# end def

def string2float( s ):
  s = s.split()
  return array2float( s )
# end def

# L2 norm of a 3D vector
def l2norm( v ):
  return npla.norm( v )
# end def

# norm check of direct vectors
def rvnorm( v, m ):
  for i in range(0,3):
    if abs(v[i]) > m:
      return False
  # end for
  return True
# end def

# normalize relative coords
def rcnorm( v, eps = ZERO ):
  for i in range(0,3):
    if v[i] < ZERO - eps:
      v[i] = v[i] + ONE
    elif v[i] > ONE - eps:
      v[i] = v[i] - ONE
    else:
      v[i] = v[i]
    # end for
  return v
# end def

def sgn( v ):
  if v < ZERO:
    return MONE
  return ONE
# end def


# https://en.wikipedia.org/wiki/Rotation_matrix
def ROT( u, theta ):
  R  = np.zeros((3,3))
  ct = np.zeros(2)
  th = theta*2.0*m.pi/180.0
  ct[0] = m.cos(th)
  ct[1] = 1.000 - ct[0]
  st = m.sin(th)
  # normal vec
  un = l2norm(u)
  for i in range(0,3):
    u[i] = u[i] / un
  # diagonal
  for i in range(0,3):
    R[i][i] = ct[0] + u[i]*u[i]*ct[1]
  # offdiag
  R[0][1] = u[0]*u[1]*ct[1]-u[2]*st
  R[0][2] = u[0]*u[2]*ct[1]+u[1]*st
  R[1][0] = u[1]*u[0]*ct[1]+u[2]*st
  R[1][2] = u[1]*u[2]*ct[1]-u[0]*st
  R[2][0] = u[2]*u[0]*ct[1]-u[1]*st
  R[2][1] = u[2]*u[1]*ct[1]+u[0]*st
  return R
# end def

# https://en.wikipedia.org/wiki/Hypercube
def CUB():
  one = 1.00000000000000000
  C = np.zeros((8,3))
  C[3][0] = C[5][0] = C[6][0] = C[7][0] = one
  C[2][1] = C[4][1] = C[6][1] = C[7][1] = one
  C[1][2] = C[4][2] = C[5][2] = C[7][2] = one
  return C
# end def

def GAUSS(x, A=1, mu=1, sigma=1):
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
