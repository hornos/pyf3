#
# IO Package
# TAB: 4
#
import os
import sys
import math
import string
import numpy

from pypak.Types         import *
from pypak.IO.IO         import IO
from pypak.IO.File       import File
from pypak.Geometry      import Geometry
from pypak.Math          import *

class IO( File ):
  def __init__( self, path = None, opts = "", sysopts = { "verbose" : False, "debug" : False } ):
    File.__init__( self, path, opts, sysopts )
    self.geom = Geometry( 'ASEPOT' )
    self.reference = None
  # end def

  def read( self, opts = None ):
    self.rewind()
    self.clean()
    self.state( 1, self.comment )
    self.state( 2, self.read_types_header )
    self.state( 3, self.comment )
    self.state( 4, self.read_types )
    File.run( self, 4 )
    self.state( 4 + self.types, self.comment )
    self.state( 4 + self.types + 2, self.comment )
    self.state( 4 + self.types + 3, self.read_lat_c )
    self.state( 4 + self.types + 4, self.read_lat_vec )
    self.state( 4 + self.types + 8, self.read_ions )
    File.run( self )
    self.geom.gen_species()
  # end def

  def read_types_header( self ):
    (types,ions) = self.line()
    self.types = string.atoi( types )
    self.ions  = string.atoi( ions )
    self.process()
  # end def

  def read_types( self ):
    for i in range( 1, self.types + 1 ):
      if i > 1:
        self.getline()
      # end if
      self.process()
    # end for
  # end def

  def read_ions( self ):
    for i in range( 1, self.ions + 1 ):
      if i > 1:
        self.getline()
      # end if
      (no,symbol,cl_shift,x,y,z) = self.line()
      no = string.atoi( no )
      # VMD indexes
      no = no - 1 
      cl_shift = string.atof( cl_shift )
      x = string.atof( x )
      y = string.atof( y )
      z = string.atof( z )
      try:
        self.geom.add( AtomPos( symbol, no, cl_shift, numpy.array( [x, y, z] ) ) )
      except Exception as ex:
        print str( ex )
      # end try
      self.process()
    # end for
  # end def

  def read_lat_c( self ):
    constant = self.line()[0]
    self.geom.lat_c = string.atof( constant )
    self.process()
  # end def

  # super: read_lat_vec

# PRB 78, 235104-5 (7)
# EPA(D,q) = q * (V_Dq - V_H)
#   shift  =     (inp  - ref)

  def average_upot( self, argv = None ):
    atomlist = argv['atomlist']
    ref      = argv['reference']
    vacancy  = argv['vacancy']
    spec = {}
    avg_cl_shift = 0.000

    # lattice vectors
    try:
      lat_vec = argv['lat_vec']
      self.geom.lat_vec = numpy.reshape( lat_vec, ( 3, 3 ) )
      if ref != None:
        ref.geom.lat_vec = numpy.reshape( lat_vec, ( 3, 3 ) )
      # end if
      msg = PTD[PT.Cart]
      # cart origo?
      try:
        origo_vec = argv['origo_vec']
      except:
        origo_vec = None
      # end try
    # end if
    except:
      lat_vec = None
      msg = PTD[PT.Direct]
    # end try
    if self.verbose:
      print " Coords:",msg
    # end if

    if lat_vec != None:
      avg_xyz = Geometry()
      avg_xyz.lat_vec = self.geom.lat_vec
      avg_xyz.pt = PT.Cart
    # end if

    if self.verbose:
      msg = "\n  %5s %4s %12s %12s %12s %12s" % ("No","Sym","cl_shift","x","y","z")
      if origo_vec != None:
        msg += " %12s" % ("dr")
        if ref != None:
          msg += " %12s" % ("ref dr")
      print msg
    # end if

    # cross check
    if ref != None:
      lookup = l_vacancy( range( 0, ref.geom.ac ), vacancy )
      ref_avg_cl_shift = 0.000
    # end if

    for ai in atomlist:
      atom = self.geom.get( ai )
      s    = atom.symbol
      no   = atom.no
      cls  = atom.cl_shift
      pos  = atom.position
      avg_cl_shift += cls

      # cross check
      if ref != None:
        ref_atom = ref.geom.get( lookup[ai] )
        ref_s    = ref_atom.symbol
        ref_pos  = ref_atom.position
        ref_cls  = ref_atom.cl_shift
        ref_avg_cl_shift += ref_cls
      # end if

      # cart position
      if lat_vec != None:
        # change to cart
        pos = self.geom.position( atom, PT.Cart )
        if ref != None:
          ref_pos = ref.geom.position( ref_atom, PT.Cart )
        avg_xyz.add( AtomPos( s, no, cls, pos ) )
      # end if

      if self.verbose:
        msg  = "  %5d %4s" % (atom.no, s)
        msg += " %12.6f" % cls
        msg += " %12.6f %12.6f %12.6f" % (pos[0], pos[1], pos[2])
        if origo_vec != None and lat_vec != None:
          msg += " %12.6f" % v_dr( origo_vec, pos )
        # end if
        print msg

        if ref != None:
          msg  = "R %5d %4s" % (ref_atom.no, ref_s)
          msg += " %12.6f" % ref_cls
          msg += " %12.6f %12.6f %12.6f" % (ref_pos[0], ref_pos[1], ref_pos[2])
          if origo_vec != None and lat_vec != None:
            msg += " %12.6f" % v_dr( origo_vec, ref_pos )
            msg += " %12.6f" % v_dr( ref_pos, pos )
          # end if
          print msg
        # end if
      # end if

      try:
        spec[s] += 1
      except:
        spec[s] = 1
      # end try
    # end for ai

    if self.verbose:
      print "\n Atoms: ", len( atomlist )
      print " Species: ", spec
      print "\n Orig. Average:", avg_cl_shift, "/", len( atomlist ), \
                        "=", avg_cl_shift / len( atomlist )
      if ref != None:
        print "  Ref. Average:", ref_avg_cl_shift, "/", len( atomlist ), \
                               "=", ref_avg_cl_shift / len( atomlist )
        print "\n Shift:", avg_cl_shift - ref_avg_cl_shift
      # end if

    # end if

    # end if
    if lat_vec != None:
      avg_output = IO( 'atomlist.xyz', 'xyz', 'w+' )
      avg_output.geom( avg_xyz )
      avg_output.write()
    # end if

    avg_cl_shift /= len( atomlist )
    return avg_cl_shift
  # end def

  def compare( self, complist = None, eps = 0.01 ):
    shift = 0.00000
    one  = 1.000000
    zero = 0.000000
    c = 0
    ref = self.geom
    inp = self.geom.geom
    for k,v in complist.iteritems():
      k = int(k)
      v = int(v)
      ratom = ref.get(k)
      rpos  = ratom.position
      rcls  = ratom.cl_shift

      iatom = inp.get(v)
      ipos  = iatom.position
      icls  = iatom.cl_shift

      if ratom.symbol != iatom.symbol:
        raise Warning( "Symbol mismatch!" )

      # G2012-04-12
      # normalize coordinates
      for i in range(0,3):
        if ipos[i] > one:
          ipos[i] -= one
        if abs(one - ipos[i]) < eps:
          ipos[i] = one - ipos[i]

        if rpos[i] > one:
          rpos[i] -= one
        if abs(one - rpos[i]) < eps:
          rpos[i] = one - rpos[i]
      # end for
      print "REF %4d %2s %12.9f %12.9f %12.9f %12.9f" % (ratom.no,ratom.symbol,rpos[0],rpos[1],rpos[2],rcls)
      print "INP %4d %2s %12.9f %12.9f %12.9f %12.9f" % (iatom.no,iatom.symbol,ipos[0],ipos[1],ipos[2],icls)
      print "L2 INP-REF: %12.9f" %(l2norm(ipos-rpos))
      print
      # print ratom.no,ratom.symbol,ratom.position
      # print iatom.no,iatom.symbol,iatom.position
      shift += icls - rcls
      c += 1
    # end for
    print "Shift:",shift/float(c)
    print
  # end def

  def ino( self, no, vl ):
    vl.sort()
    for i in vl:
      if no >= i:
        no = no - 1
    # end for
    return no
  # end def

  def average( self, vaclist = None ):
    shift = 0.00000
    one  = 1.000000
    zero = 0.000000
    c = 0
    inp = self.geom
    ref = self.geom.geom

    # for crop check
    crop = self.geom.clone()

    for aref in ref.atoms:
      # reference
      rno  = aref.rno
      rpos = aref.position
      rcls = aref.cl_shift

      # input
      ino  = self.ino( rno, vaclist )
      if(ino!=rno):
        print "INDEX SHIFT: %d -> %d" %(rno,ino)
      ainp = inp.get(ino)
      ipos = ainp.position
      icls = ainp.cl_shift
      crop.add(ainp)

      if aref.symbol != ainp.symbol:
        raise Warning( "Symbol mismatch!" )

      # G2012-04-12
      # normalize coordinates
      ipos = rcnorm( ipos, 0.01 )
      rpos = rcnorm( rpos, 0.01 )
      dist = l2norm(ipos-rpos)
      ps = icls-rcls
      print "REF %4d %2s %12.9f %12.9f %12.9f %12.9f" % (rno,aref.symbol,rpos[0],rpos[1],rpos[2],rcls)
      print "INP %4d %2s %12.9f %12.9f %12.9f %12.9f" % (ainp.no,ainp.symbol,ipos[0],ipos[1],ipos[2],icls)
      if(dist > 0.05):
        print "HIGH DISTANCE"
      print "L2(INP-REF) %12.9f  Shift  %12.9f" %(dist,ps)
      print "ASEDIFF %4d %2s %12.9f %12.9f" %(rno,aref.symbol,aref.dist,ps)
      print
      shift += ps
      c += 1
    # end for
    print "APS %4d %12.9f" % ( c, shift/float(c) )
    print

    crop.normalize()
    #crop.info()
    return crop
  # end def

# end class