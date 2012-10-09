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
              dest = "input", default = "POSCAR",
              help = "Input" )

    self.option( "-o", "--output",
              action = "store", type = "string",
              dest = "output", default = "vsposcar",
              help = "Output" )

    self.option( "-k", "--cart",
              action = "store_true",
              dest = "cart", default = False,
              help = "Cart" )

    self.option( "-b", "--band",
              action = "store", type="string",
              dest = "band",
              help = "Band" )

    self.option( "-x", "--xyz",
              action = "store_true",
              dest = "xyz", default = False,
              help = "XYZ" )

    self.init()
  # end def __init__


  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()
    opts_sys = { "verbose" : self.verbose, "debug" : self.debug }

    try:
      inp  = IO( opts.input,'POSCAR', "r", opts_sys )
      inp.read()
    except:
      if self.debug:
        raise
      else:
        print "Input not found:", opts.input
        sys.exit(1)

    geom = inp.geom()

    try:
      band=[]
      with open(opts.band) as f:
        for line in f:
          line = line.split()
          if len(line) == 0:
            continue
          if line[0] == 'tot' or line[0] == 'band':
            continue
          # print len(line)
          band.append(string.atoi(line[0]))
    except:
      raise
    else:
      print band

    fileio = 'POSCAR'
    if opts.cart:
      opts_pt = { 'pt' : PT.Cart }
    else:
      opts_pt = { 'pt' : PT.Direct }

    if opts.xyz:
      opts.output += '.xyz'
      fileio = 'xyz'
      opts_pt = { 'pt' : PT.Cart }
    else:
      opts.output += '.POSCAR'
    # end if
    try:
      out = IO( opts.output, fileio, "w+", opts_sys )
      out.geom( geom )
      if len(band) != 0:
        out_geom = out.geom()
        out_geom.band(band)
      out.write( opts )
    except:
      if self.debug:
        raise
      else:
        print "Output failed:", opts.output
        sys.exit(1)
  # end def
# end class

### BEGIN MAIN
if __name__ == '__main__':
  p = Program()
  p.main()
### END MAIN
