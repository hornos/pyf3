#!/usr/bin/env python2.6
#TAB: 8
import os
import sys
import string
import math
import numpy as np

### BEGIN PROGRAM CLASS
from pypak.Script        import Script
from pypak.IO.IO         import IO
from pypak.Types         import *
from pypak.Math          import *

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

    self.option( "-s", "--sigma",
              action = "store", type = "float",
              dest = "sigma",
              help = "Sigma", default = 1.0 )

    self.option( "-x", "--rate",
              action = "store", type = "int",
              dest = "rate",
              help = "Sampling rate", default = 0.5 )

    self.option( "-k", "--kpoint",
              action = "store", type = "int",
              dest = "kp",
              help = "K-point", default = 1 )

    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    width = 6
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
    inp_grid = inp_ueig.grid(opts.kp)

    # create input fine grid
    low  = inp_ueig.grid_min(opts.kp) - wsig
    high = inp_ueig.grid_max(opts.kp) + wsig
    rate = opts.rate
    grid_range = high - low
    maxrate = int(math.ceil( (high - low) * rate ))
    fine_range = np.arange(maxrate) / maxrate

    # shifted fine grid
    inp_fine_grid = fine_range * grid_range - abs( low )

    # compound grid
    inp_comp_grid = np.concatenate((inp_grid[:,0], inp_fine_grid))
    inp_comp_grid = np.sort(inp_comp_grid)
    # fx  d/dx fx
    inp_comp_grid = np.vstack( ( inp_comp_grid, 
                                 np.zeros( len( inp_comp_grid ) ), 
                                 np.zeros( len( inp_comp_grid ) ) ) )

    print inp_grid
    # inp_comp_grid -> mu
    for i in range(0,maxrate):
      mu = inp_comp_grid[i,0]
      for j in range(0,len(inp_grid)):
        x = inp_grid[j,0]
        A = inp_grid[j,1]
        # fx
        inp_comp_grid[i,1] += GAUSS( x, A , mu, sig )
        # d/dx fx
        inp_comp_grid[i,2] -= x*A / (sig * sig) * GAUSS( x, A, mu, sig )
      # end for
    # end for

    if opts.ref != None:
      try:
        ref = IO( opts.ref, 'UEIG', "r", sysopts )
        ref.read()
      except:
        if self.debug:
          raise
        else:
          print "Reference failed:", opts.ref
          sys.exit(1)
      # end try

      ref_ueig = ref.handler
      ref_grid = ref_ueig.grid(opts.kp)


    # end if


    # boundaries 3 sigma

    # write out dos for gnuplot
    # ueig.dos( opts.kp, opts.sigma2, opts.rate )
  # end def
# end class

### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN
