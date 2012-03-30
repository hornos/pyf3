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

    self.option( "-e", "--embed", action = "store", type = "string",
              dest = "embed", default = "POSCAR",
              help = "Embed" )

    self.option( "-i", "--host", action = "store", type = "string",
              dest = "host", default = "host.POSCAR",
              help = "Host" )

    self.option( "-o", "--output", action = "store", type = "string",
              dest = "output", default = "vsembed.POSCAR",
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

    (embed,eno) = opts.embed.split( ":" )
    eno = string.atoi( eno )

    (host,hno)  = opts.host.split( ":" )
    hno = string.atoi( hno )

    # read input
    # IO  filename  type  mode  options
    try:
      embedio = IO( embed, 'POSCAR', 'r', opts_sys )
      embedio.read()
    except:
      if self.debug:
        raise
      else:
        print "Input not found:", embedio
        sys.exit(1)
    # end try

    try:
      hostio = IO( host, 'POSCAR', 'r', opts_sys )
      hostio.read()
    except:
      if self.debug:
        raise
      else:
        print "Input not found:", host
        sys.exit(1)
    # end try

    host_geom = hostio.geom()
    #               where what
    # self = host
    host_geom.embed( hno, embedio.geom(), eno )
    host_geom.normalize()

    # write output
    # IO  filename  type  mode  options
    try:
      out = IO( opts.output, 'POSCAR', "w+", opts_sys )
      out.geom( host_geom )
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
