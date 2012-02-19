#
# Types package
#

import sys
import string
import math
import copy
import numpy
from pypak.Math import *
from pypak.Types import *

# TODO: verbose
class Geometry:
  def __init__( self, name = "" ):
    self.name    = name
    self.species = {}
    self.atoms   = []
    self.ac      = 0
    self.pt      = PT.Direct
    self.lat_vec = numpy.zeros((3, 3))
    self.rec_vec = numpy.zeros((3, 3))
    self.lat_c   = 1.0000 # Ang
  # end def

  def clone( self, atoms = False ):
    geom = Geometry( self.name )
    geom.name = 'Clone of ' + geom.name
    geom.lat_vec = copy.deepcopy( self.lat_vec )
    geom.rec_vec = copy.deepcopy( self.rec_vec )
    geom.lat_c   = copy.deepcopy( self.lat_c )
    geom.pt      = copy.deepcopy( self.pt )
    if atoms:
      geom.species = copy.deepcopy( self.species )
      geom.atoms   = copy.deepcopy( self.atoms )
      geom.ac      = copy.deepcopy( self.ac )
    # end if
    return geom
  # end if

  def natoms( self ):
    return len( self.atoms )
  # end def

  def nspecies( self ):
    return len( self.species )
  # end def

  def info( self, header = False ):
    lv = self.lat_vec
    print "%20s%s" % ( "Name:", ' '+self.name )
    for i in range( 0, 3 ):
      print "%20s %9.6f %9.6f %9.6f" %( "a"+str(i+1)+":",lv[i][0], lv[i][1], lv[i][2] )
    # end for
    print "%20s%5d"  % ( "Species:", self.nspecies() )
    print "%20s%5d"  % ( "Atoms:", self.natoms() )
    print "%20s%5d"  % ( "PT:", self.pt )

    if header:
      return
    print "\n%5s%5s%12s%12s%12s" % ( "no", "sym", "x", "y", "z" )
    for atom in self.atoms:
      sym = atom.symbol
      no  = atom.no
      vec = atom.position
      print "%5s%5s%12.6f%12.6f%12.6f" % ( no, sym, vec[0], vec[1], vec[2] )
    # end for
  # end def

  def header( self ):
    self.info( True )
  # end def

  def gen_species( self ):
    # reset
    self.species = {}
    # regenerate
    for atom in self.atoms:
      sym = atom.symbol
      try:
        self.species[sym] += 1
      except:
        self.species[sym] = 1
      # end try
    # end for
    print " Species:",self.species
  # end def


  def add( self, atom = None, reno = True ):
    _atom = copy.deepcopy( atom )
    if reno:
      _atom.no = self.ac
    self.atoms.append( _atom )
    self.ac += 1
  # end def

  def rem( self, atom = None ):
    self.atoms.remove( atom )
    self.ac -= 1
  # end def

  def get( self, i = 0, vmd = True ):
    if vmd:
      return self.atoms[i]
    return self.atoms[i-1]
  # end def

  def order( self ):
    ordered = []
    for sym in self.species:
      for atom in self.atoms:
        if atom.symbol == sym:
          ordered.append( atom )
      # end for
    # end for
    self.atoms = ordered
  # end def

  def reciprocal( self ):
    self.rec_vec = numpy.linalg.inv( self.lat_vec )
  # end def


  def nearest( self, pos = None ):
    nearest_atom = None
    nearest_dpos = 100000.000
    for atom in self.atoms:
      dpos_vec = abs( numpy.subtract( atom.position, pos ) )
      dpos_max = dpos_vec[ numpy.argmax( dpos_vec ) ]
      if dpos_max < nearest_dpos :
        nearest_atom = atom
        nearest_dpos = dpos_max
    # end for
    return nearest_atom
  # end def


  def position_direct( self, r = numpy.zeros( 3 ) ):
    self.reciprocal()
    return numpy.dot( 1.0 / self.lat_c, numpy.dot( r, self.rec_vec ) )
  # end def

  def position_cart( self, rho = numpy.zeros( 3 ) ):
    return numpy.dot( self.lat_c, numpy.dot( rho, self.lat_vec ) )
  # end def

  def position( self, atom = None, pt = PT.Direct ):
    pos = r = atom.position
    if self.pt != pt:
      if pt == PT.Cart:
        # D -> C
        pos = self.position_cart( r )
      else:
        # C -> D
        pos = self.position_direct( r )
      # end if
    # end if
    return pos
  # end def

  def cart( self ):
    # convert to cart
    if self.pt == PT.Direct:
      for atom in self.atoms:
        atom.position = self.position_cart( atom.position )
      # end for
      self.pt = PT.Cart
      print " Cart coordinates: " + self.name
    # end if
  # end def

  def direct( self ):
    # convert to cart
    if self.pt == PT.Cart:
      for atom in self.atoms:
        atom.position = self.position_direct( atom.position )
      # end for 
      self.pt = PT.Direct
      print " Direct coordinates: " + self.name
    # end if
  # end def

  def move( self, S = numpy.zeros( 3 ) ):
    for atom in self.atoms:
      atom.move( S )
    # end for
  # end def

  # TODO
  def supercell( self, msc = numpy.zeros( [3, 3] ) ):
    vol = numpy.dot( msc[0,:], numpy.cross( msc[1,:], msc[2,:] ) )
    if not vol > 0.0:
      raise Warning( 'Not a right-hand system' )
    # end if
    # clone
    geom = self.clone()

    # scale lat_c
    if geom.lat_c != 1.0:
      geom.lat_vec = numpy.dot( geom.lat_c, geom.lat_vec )
    # end if
    # scale base
    geom.cart()

    sup_lat_vec = numpy.dot( msc, self.lat_vec )
    cmb = [[],[],[]]
    for i in range(0,3):
      mij = [0,0,0]
      lmn = [[],[],[]]
      for j in range(0,3):
        ij = msc[i][j]
        if ij < 0:
          mij[j] = ij
          lmn[j] = range(mij[j],0)
        else:
          mij[j] = ij + 1
          lmn[j] = range(1,mij[j])
        # end if
        if lmn[j] == []:
          lmn[j] = [0]
      # end for

      print lmn
      for l in lmn[0]:
        for m in lmn[1]:
          for n in lmn[2]:
            print i,l,m,n
            cmb[i] += [[l,m,n]]
          # end for
        # end for
      # end for
    # end for

    for o in cmb[0]:
      for p in cmb[1]:
        for q in cmb[2]:
          cmm = numpy.array([o,p,q])
          cmm_lat_vec = numpy.dot( cmm, self.lat_vec )
          print cmm_lat_vec
          # base transport
        # end for
      # end for
    # end for
    print len(cmb[0])*len(cmb[1])*len(cmb[2])
  # end def

  # very simple diff
  def diff( self, geom = None, ll = 0.001, ul = 1.5, na = False ):
    # check lattice
    if abs( self.lat_c - geom.lat_c) > 0.001:
      raise Warning( 'Lattice constant' )
    for i in range(0,3):
      if l2norm( self.lat_vec[i] - geom.lat_vec[i] ) > 0.001:
        raise Warning( 'Lattice vector' )
    # end for

    # check atoms
    if abs( self.ac - geom.ac ):
      raise Warning( 'Atoms' )

    # check coordinates
    geom.cart()
    self.cart()

    # build diff geom
    dgeom = self.bravais()
    dgeom.name = 'Diff:' + dgeom.name
    dgeom.cart()

    for atom in self.atoms:
      pos   = atom.position
      natom = geom.nearest( pos )
      npos  = natom.position
      # delta should be substracted
      dpos  = pos - npos
      d = l2norm( dpos )
      if d > ll and d < ul:
        print "R  " + str( atom.no ) + " " + atom.symbol + " " + str( atom.position )
        print "N  " + str( natom.no ) + " " + natom.symbol + " " + str( natom.position ) + " " + str( dpos )
        if na:
          natom.position = dpos
          dgeom.add( natom, False )
        else:
          atom.position = dpos
          dgeom.add( atom, False )
    # end for
    dgeom.gen_species()
    return dgeom
  # end def

  def patch( self, geom = None ):
    self.cart()
    geom.cart()
    for atom in geom.atoms:
      no  = atom.no
      if atom.symbol != self.get(no).symbol:
        raise Warning( "Symbol mismatch" )
      pos = self.get( no ).position
      pos -= atom.position
      self.get( no ).position = pos
    # end for
    return self
  # end def

  def normalize(self):
    self.gen_species()
    self.order()
    self.direct()
  # end def

  ### Transformations

  def TF_crop( self, c = [] ):
    # switch to cart coords
    self.cart()

    # around an atom
    if c[0] == 'Atom':
      s = c[1]
      n = string.atoi( c[2] )
      r = string.atof( c[3] )
      # get coords
      atom = self.get( n )
      origo = atom.position
    # end if

    # around an origo
    if c[0] == 'Origo':
      origo = numpy.array( [ 0.0, 0.0, 0.0 ] )
      origo[0] = string.atof( c[1] )
      origo[1] = string.atof( c[2] )
      origo[2] = string.atof( c[3] )
      r = string.atof( c[4] )
    # end if

    crop = self.clone()

    # copy atoms
    for atom in self.atoms:
      dr = l2norm( atom.position - origo )
      if dr < r:
        crop.add( atom, True )
        # atom.info()
      # end if
    # end for
    print " TF/crop", c
    crop.normalize()
    return crop
  # end def

  def TF_insert( self, c = [] ):
    pos  = numpy.array( [ 0.0, 0.0, 0.0 ] )
    s = c[0]
    for i in range(0,3):
      pos[i] = string.atof( c[i+1] )
    # insert atom
    self.add( AtomPos( symbol = s, vec = pos ) )
    self.gen_species()
    print " TF/insert",c
    return self
  # end def

  def TF_delete( self, c = [] ):
    s = c[0]
    n = string.atoi( c[1] )
    atom = self.get( n )
    if atom.symbol != s:
      atom.info()
      raise Warning( "Symbol mismatch" )
    # end if
    self.rem( atom )
    self.gen_species()
    print " TF/delete",c
    return self
  # end def

  def TF_rotate( self, c = [] ):
    s = c[0]
    n = string.atoi( c[1] )

    # direction
    u = numpy.array( [ 0.0, 0.0, 0.0 ] )
    u[0] = string.atof( c[2] )
    u[1] = string.atof( c[3] )
    u[2] = string.atof( c[4] )
    # angle
    t = string.atof( c[5] )

    self.cart()
    atom = self.get( n )
    if atom.symbol != s:
      raise Warning( "Symbol mismatch" )
    # end if
    origo = atom.position
    print "TF/rotate origo"
    atom.info()
    R = ROT(u,t)

    # copy atoms
    for atom in self.atoms:
      dv = atom.position - origo
      dv = numpy.dot(R,dv)
      atom.position = dv + origo
    # end for
    self.direct()

    return self
  # end def
# end class Geometry
