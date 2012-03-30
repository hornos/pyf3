#!/usr/bin/env python2.6
#TAB: 8
import os
import sys
import string

### BEGIN PROGRAM CLASS
from pypak.Script        import Script
from pypak.LX.LX         import LX
from pypak.IO.IO         import IO
from pypak.Types         import *


class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.option( "-i", "--input", action = "store", type = "string",
              dest = "input", default = "POSCAR",
              help = "Input" )

    self.option( "-t", "--trans", action = "store", type = "string",
              dest = "trans", default = "vstrans.tf",
              help = "Transform" )

    self.option( "-o", "--output", action = "store", type = "string",
              dest = "output", default = "vstrans.POSCAR",
              help = "Output" )

    self.option( "-k", "--cart", action = "store_true",
              dest = "cart", default = False, help = "Cart" )

    # script init
    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    opts_sys = { "verbose" : self.verbose, "debug" : self.debug }

    # read input
    # IO  filename  type  mode  options
    try:
      inp = IO( opts.input, 'POSCAR', 'r', opts_sys )
      inp.read()
    except:
      if self.debug:
        raise
      else:
        print "Input not found:", opts.input
        sys.exit(1)
    # end try

    # do transformation
    # LX  transfile type options
    try:
      trs = LX( opts.trans, 'TF', opts_sys )
      trs.geom( inp.geom() )
      # build & process
      geom = trs.read()
    except:
      if self.debug:
        raise
      else:
        print "Transformation error:", opts.trans
        sys.exit(1)
    # end try

    # write output
    # IO  filename  type  mode  options
    try:
      out = IO( opts.output, 'POSCAR', "w+", opts_sys )
      out.geom( geom )
      if opts.cart:
        out.write( { 'pt' : PT.Cart } )
      else:
        out.write( { 'pt' : PT.Direct } )
    except:
      if self.debug:
        raise
      else:
        print "Output failed:", opts.output
        sys.exit(1)
    # end try
  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN
