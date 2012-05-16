#!/usr/bin/env python2.6
#TAB: 8
import os
import sys
import string

### BEGIN PROGRAM CLASS
from pypak.Script        import Script
from pypak.IO.IO         import IO
from pypak.Types         import *


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
              dest = "sigma2",
              help = "Sigma square", default = 1.0 )

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

    inp_ueig = inp.handler
    inp_grid = ueig.grid(opts.kp)

    if opts.reference != None:
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
      ref_grid = ueig.grid(opts.kp)

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
