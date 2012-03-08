#!/usr/bin/env python
#TAB: 8
import os
import sys
import string

### BEGIN PROGRAM CLASS
from pypak.Script        import Script
from pypak.LX.LX         import LX
from pypak.LX.Lexer      import Lexer
from pypak.Types         import *


class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.option( "-i", "--input",
              action = "store", type = "string",
              dest = "input", default = "UEIG",
              help = "Input" )

    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    try:
      inp = LX( opts.input, 'UEIG', sysopts )
      inp.build()
      inp.process()
    except:
      if self.debug:
        raise
      else:
        print "Input failed:", opts.input
        sys.exit(1)
    # end try

  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN
