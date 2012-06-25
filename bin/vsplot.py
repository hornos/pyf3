#!/usr/bin/env python2.7
#TAB: 8
import os
import sys

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
              dest = "ref", default = "ref_UEIG",
              help = "Reference" )

    self.option( "-x", "--column",
              action = "store", type = "int",
              dest = "col",
              help = "Column", default = 1 )

    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }
    data1=load(opts.inp)
    data2=load(opts.ref)

    plot2(data1,data2,opts.col)
# end class

### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN
