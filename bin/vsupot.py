#!/usr/bin/env python
#TAB: 8
import os
import sys
import string
import numpy

from pypak.Script import Script
from pypak.IO.IO import IO

class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.option( "-i", "--input",
              action = "store", type = "string",
              dest = "input", default = "input.UPOT",
              help = "Input" )

    self.option( "-r", "--reference",
              action = "store", type = "string",
              dest = "reference", default = "reference.UPOT",
              help = "Reference" )

    self.init()
  # end def __init__

  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    try:
      inp = IO( opts.input, 'UPOT', "r", sysopts )
      print opts.input,":"
      inp.read()
    except:
      if self.debug:
        raise
      else:
        print "Input failed:", opts.input
        sys.exit(1)
    # end try

    try:
      print opts.reference,":"
      ref = IO( opts.reference, 'UPOT', "r", sysopts )
      ref.read()
    except:
      if self.debug:
        raise
      else:
        print "Reference failed:", opts.reference
        sys.exit(1)
    # end try

    # read atomlist

    # warning: geoms should have the same lattice
    # match
    gref = ref.geom()
    gref.geom = inp.geom()
    gref.match()

  # end def main
# end class

### main
if __name__ == '__main__':
  p = Program()
  p.main()
# end if
