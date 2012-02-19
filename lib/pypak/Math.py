#
# Types package
#

import sys
import copy
import string
import math as m
import numpy as np
import numpy.linalg as npla

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

def l2norm( v ):
  return npla.norm( v )
# end def


# http://en.wikipedia.org/wiki/Rotation_matrix
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
