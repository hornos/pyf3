#!/usr/bin/env python2.7
#TAB: 8
import os
import sys
import string
import math
import numpy as np

### BEGIN PROGRAM CLASS
from pypak.Script import Script
from pypak.IO.IO  import IO
from pypak.Types  import *
from pypak.Util   import *
from pypak.Plot   import *


### Kernel wrapper
def gendos( amp, sig, inp_grid, inp_comp_grid, python = False ):
  if not python:
    import kernel.vsueig_omp as kernel
    inp_grid_cont = c_cont( inp_grid )
    inp_comp_grid_cont = c_cont( inp_comp_grid )
    kernel.gendos( amp, sig, inp_grid_cont, inp_comp_grid_cont )
    return
  # end if

  print "Python Kernel"

  from pypak.Math import gauss,dgauss
  # from cython.math import gauss,dgauss
  from time import clock

  i_range=len(inp_grid)
  j_range=len(inp_comp_grid[0])

  print i_range, j_range

  start = clock()
  # inp_grid 2d float
  # inp_comp_grid 2 float
  for i in range(0,i_range):
    mu = inp_grid[i,0]
    A  = inp_grid[i,1] * amp
    # print mu,A
    for j in range(0,j_range):
      x = inp_comp_grid[0,j]
      if abs(x-mu) > 3*sig:
        continue
      # print x
      # fx
      inp_comp_grid[1,j] += gauss( x, A , mu, sig )
      # d/dx fx
      inp_comp_grid[2,j] += dgauss( x, A, mu, sig )
    # end for
  # end for
  elapsed = (clock() - start)
  print "Elapsed time: %9.6lf s" % elapsed
# end def


class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.option( "-i", "--input",
              action = "store", type = "string",
              dest = "inp", default = "UEIG",
              help = "Input" )

    self.option( "-r", "--reference",
              action = "store", type = "string",
              dest = "ref", default = "reference.UEIG",
              help = "Reference" )

    self.option( "-z", "--sigma",
              action = "store", type = "float",
              dest = "sigma",
              help = "Sigma", default = 0.1 )

    self.option( "-a", "--amp",
              action = "store", type = "float",
              dest = "amp",
              help = "Amplitudo", default = 1.0 )

    self.option( "-s", "--spin",
              action = "store", type = "int",
              dest = "sp",
              help = "Spin", default = 1 )

    self.option( "-x", "--rate",
              action = "store", type = "int",
              dest = "rate",
              help = "Sampling rate", default = 100 )

    self.option( "-k", "--kpoint",
              action = "store", type = "int",
              dest = "kp",
              help = "K-point", default = 1 )

    self.option( "-o", "--output", action = "store", type = "string",
              dest = "out", default = "vsueig",
              help = "Output" )

    self.option( "-t", "--test", action = "store_true",
              dest = "test", default = False,
              help = "Kernel Test" )

    self.option( "-p", "--python", action = "store_true",
              dest = "python", default = False,
              help = "Do not use C kernel" )

    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    width = 3
    sig   = opts.sigma
    amp   = opts.amp
    wsig  = width * sig

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    try:
      inp = IO( opts.inp, 'UEIG', "r", sysopts )
      inp.read()
    except:
      if self.debug:
        raise
      else:
        print "Input failed:", opts.inp
        sys.exit(1)
    # end try

    mu = 0.0

    inp_ueig = inp.handler

    # grid for k-point: eig occ
    kp = opts.kp - 1
    sp = opts.sp - 1 
    inp_grid = inp_ueig.grid(kp,sp)
    # print inp_grid

    # create input fine grid
    low  = inp_ueig.grid_min(kp,sp) - wsig
    high = inp_ueig.grid_max(kp,sp) + wsig

    #print low, high
    rate = opts.rate
    grid_range = high - low
    maxrate = int(math.ceil( grid_range * rate ) )
    # print maxrate
    fine_range = np.arange( maxrate ) / float(maxrate)
    # print fine_range

    # shifted fine grid
    inp_fine_grid = fine_range * grid_range - abs( low )
    # print inp_fine_grid

    # compound grid
    inp_comp_grid = np.concatenate((inp_grid[:,0], inp_fine_grid))
    inp_comp_grid = np.sort(inp_comp_grid)
    # print inp_comp_grid

    # init grid: eig, fx,  d/dx fx
    inp_comp_grid = np.vstack( ( inp_comp_grid, 
                                 np.zeros( len( inp_comp_grid ) ), 
                                 np.zeros( len( inp_comp_grid ) ) ) )
    # print inp_comp_grid[0]
    # sys.exit(0)

    # generating DOS
    gendos( amp, sig, inp_grid, inp_comp_grid, opts.python )

    if opts.test:
      sys.exit(1)

    # output
    out_name = opts.out + "_kp_" + str(opts.kp) + "_sp_" + str(opts.sp)
    out = open( out_name , 'w')
    out.write( "" )

    i_range=len(inp_grid)
    j_range=len(inp_comp_grid[0])

    # create & write out dos
    dos = np.zeros( (j_range,3) )
    for j in range(0,j_range):
      dos[j,0] = inp_comp_grid[0,j]
      dos[j,1] = inp_comp_grid[1,j]
      dos[j,2] = inp_comp_grid[2,j]
      out.write( "%12.6f %12.6f %12.6f\n" % (dos[j,0],dos[j,1],dos[j,2]) )
    out.close()

    # dump dos
    save(dos,out_name)
    # plot
    plot(dos)
  # end def
# end class

### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN
