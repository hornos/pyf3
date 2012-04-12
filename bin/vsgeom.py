#!/usr/bin/env python2.6
#TAB: 8
import os
import sys
import string

### BEGIN PROGRAM CLASS
from pypak.Script        import Script
from pypak.IO.IO         import IO
from pypak.Types         import *
from pypak.Geometry      import Geometry


class Program( Script ):
  def __init__( self ):
    Script.__init__( self )

    self.option( "-i", "--input",
              action = "store", type = "string",
              dest = "input", default = "input.POSCAR",
              help = "Input" )

    self.option( "-s", "--select",
              action = "store", type = "string",
              dest = "select",
              help = "Output" )

    self.option( "-o", "--output",
              action = "store", type = "string",
              dest = "output", default = "output.POSCAR",
              help = "Output" )

    self.option( "-d", "--delete",
              action = "store", type = "string",
              dest = "delete",
              help = "Delete" )

    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    inp = IO( opts.input,'POSCAR', "r", sysopts )
    inp.read()
    geom = inp.geom()

    if opts.select != None:
      aid = int(opts.select)
      cmd = "select"
    if opts.delete != None:
      aid = int(opts.delete)
      cmd = "delete"
    # end if

    atom = geom.get(aid)
    atom.info()

    if geom.pt == PT.Cart:
      dp = geom.position( atom, PT.Direct )
      cp = atom.position
    else:
      dp = atom.position
      cp = geom.position( atom, PT.Cart )
    # end if

    print " Frac : %21.16f%21.16f%21.16f" % (dp[0],dp[1],dp[2])
    print " Cart : %21.16f%21.16f%21.16f" % (cp[0],cp[1],cp[2])
  # end def
# end class


### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN
