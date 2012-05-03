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
              dest = "input", default = "input.ASEPOT",
              help = "Input" )

    self.option( "-r", "--reference",
              action = "store", type = "string",
              dest = "reference", default = "reference.ASEPOT",
              help = "Reference" )

    self.option( "-a", "--average",
              action = "store", type = "string",
              dest = "average",
              help = "Average" )

    self.option( "-x", "--compare",
              action = "store", type = "string",
              dest = "compare",
              help = "Compare" )

    self.option( "-d", "--vacancy",
              action = "store", type = "string",
              dest = "vacancy",
              help = "Vacancy Defects" )

    self.option( "-f", "--furthest",
              action = "store", type = "string",
              dest = "rho",
              help = "Rho" )

    self.option( "-m", "--match",
              action = "store", type = "float",
              dest = "match",
              help = "Match" )

    self.option( "-o", "--origo",
              action = "store", type = "string",
              dest = "origo",
              help = "Origo" )

    self.option( "-k", "--cache",
              action = "store", type = "string",
              dest = "cache", default = "vsasepot.cache",
              help = "Match cache" )

    self.option( "-p", "--poscar",
              action = "store_true",
              dest = "poscar", default = False,
              help = "Write input and reference poscar" )

    self.init()
  # end def __init__

  ### MAIN BEGIN ###
  def main( self ):
    (opts, args) = self.parse()

    sysopts = { "verbose" : self.verbose, "debug" : self.debug }

    ### begin reference
    try:
      print opts.reference,":"
      ref = IO( opts.reference, 'ASEPOT', "r", sysopts )
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
    if opts.poscar:
      out = IO( 'vsasepot.ref.POSCAR', 'POSCAR', "w+", sysopts )
      out.geom( gref )
      out.write()
    # end if

    # G2012-04-27
    if not opts.origo == None:
      gref.shift_origo(opts.origo)
    # end if

    # check furthest in reference
    if not opts.rho == None:
      rho = float( opts.rho )
      crop = gref.cart_select( rho )
      if crop.ac == 0:
        print "EMPTY SELECTION, SET SMALLER RHO"
        sys.exit(1)

      out = IO( 'vsasepot.crop.POSCAR', 'POSCAR', "w+", sysopts )
      out.geom( crop )
      out.write()

      # for atom in crop.atoms:
      #   atom.info()
      # # end for
    # end if
    ### end reference


    ### begin input
    try:
      inp = IO( opts.input, 'ASEPOT', "r", sysopts )
      print opts.input,":"
      inp.read()
    except:
      if self.debug:
        raise
      else:
        print "Input failed:", opts.input
        sys.exit(1)
    # end try
    igeom = inp.geom()
    igeom.geom = crop
    ### end input

    if not opts.vacancy == None:
      vaclist = opts.vacancy.split(",")
      for i in range(0,len(vaclist)):
        vaclist[i] = int(vaclist[i])
      # end for
      inp.average( vaclist )
      return
    # end if

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
