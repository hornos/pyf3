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
from pypak.Math   import *
from pypak.Util   import *
from pypak.Plot   import *

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
              help = "Sigma", default = 1.0 )

    self.option( "-s", "--spin",
              action = "store", type = "int",
              dest = "sp",
              help = "Spin", default = 1 )

    self.option( "-x", "--rate",
              action = "store", type = "int",
              dest = "rate",
              help = "Sampling rate", default = 0.5 )

    self.option( "-k", "--kpoint",
              action = "store", type = "int",
              dest = "kp",
              help = "K-point", default = 1 )

    self.option( "-o", "--output", action = "store", type = "string",
              dest = "out", default = "vsueig",
              help = "Output" )

    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    width = 3
    sig  = opts.sigma
    wsig = width * sig

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
    inp_grid = inp_ueig.grid(opts.kp,opts.sp)
    # print inp_grid

    # create input fine grid
    low  = inp_ueig.grid_min(opts.kp,opts.sp) - wsig
    high = inp_ueig.grid_max(opts.kp,opts.sp) + wsig

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
    i_range=len(inp_grid)
    j_range=len(inp_comp_grid[0])

    # TODO: mpi4py
    for i in range(0,i_range):
      mu = inp_grid[i,0]
      A  = inp_grid[i,1]
      # print mu,A
      for j in range(0,j_range):
        x = inp_comp_grid[0,j]
        # print x
        # fx
        inp_comp_grid[1,j] += GAUSS( x, A , mu, sig )
        # d/dx fx
        inp_comp_grid[2,j] += DGAUSS( x, A, mu, sig )
      # end for
    # end for

    # output
    out_name = opts.out + "_kp_" + str(opts.kp) + "_sp_" + str(opts.sp)
    out = open( out_name , 'w')
    out.write( "" )

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
