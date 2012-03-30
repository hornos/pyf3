#!/usr/bin/env python2.6
#TAB: 8
import os
import sys
import string
import numpy
import pickle

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

    self.option( "-a", "--average",
              action = "store", type = "string",
              dest = "average",
              help = "Average" )

    self.option( "-x", "--compare",
              action = "store", type = "string",
              dest = "compare",
              help = "Compare" )

    self.option( "-f", "--furthest",
              action = "store", type = "string",
              dest = "max",
              help = "Rmax" )

    self.option( "-m", "--match",
              action = "store", type = "float",
              dest = "match",
              help = "Match" )

    self.option( "-k", "--cache",
              action = "store", type = "string",
              dest = "cache", default = "vsupot.cache",
              help = "Match cache" )

    self.init()
  # end def __init__

  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    ### begin reference
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

    # set geoms
    gref = ref.geom()

    # check furthest in reference
    if not opts.max == None:
      (origo,max) = opts.max.split(":")
      origo = int(origo)
      max = float(max)
      gref.furthest( origo, max )
      return
    # end if
    ### end reference

    ### begin input
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
    gref.geom = inp.geom()
    ### end input

    if not opts.compare == None:
      complist = {}
      pairs = opts.compare.split(",")
      for p in pairs:
        (k,v) = p.split(":")
        complist[k] = v
      # end for
      print
      ref.compare( complist )
      return
    # end if

    # warning: geoms should have the same lattice
    # generate match table
    if not opts.match == None:
      if not opts.cache == None:
        match = open( opts.cache, 'wb' )
      # end if
      gref.match( opts.match )
      # write out match cache
      if not opts.cache == None:
        pickle.dump(gref.geom_match,match,-1)
        return
      # end if
    # end if

    if not opts.average == None:
      if not opts.cache == None:
        match = open( opts.cache, 'rb' )
        gref.geom_match = pickle.load( match )
        match.close()
      else:
        raise Exception( "Cache error" )
      # end if

      print
      ref.average( opts.average.split(":") )
  # end def main
# end class

### main
if __name__ == '__main__':
  p = Program()
  p.main()
# end if
