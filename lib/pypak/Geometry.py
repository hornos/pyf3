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
    self.geom_match = {}
    self.geom    = None
    self.atoms   = []
    self.ac      = 0
    self.pt      = PT.Direct
    self.lat_vec = numpy.zeros((3, 3))
    self.rec_vec = numpy.zeros((3, 3))
    self.lat_c   = 1.0000 # Ang
  # end def

  def clone( self, atoms = False ):
    geom = Geometry( self.name )
    geom.name = "Clone of " + geom.name
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

  # direct simple supercell
  # 3x3x3
  def scc_333_direct( self ):
    scc_geom = self.clone( True )
    scc = numpy.zeros(3])

    self.lat_vec[0] *= 3
    self.lat_vec[1] *= 3
    self.lat_vec[2] *= 3

    # slow loop
    for atom in self.atom:
      _atom = copy.deepcopy( atom )
      # z index
      for i in range(-1,2):
        scc[0] = i
        for j in range(-1,2):
          scc[1] = j
          for k in range(-1,2):
            scc[2] = k
            # skip original
            if scc[0] + scc[1] + scc[2] == 0:
              continue
            # vector add
            _atom.position += scc
            self.add(_atom)
          # end for
        # end for
      # end for
    # end for
    return scc_geom
  # end def

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

  def nearest( self, pos = None ):
    na = None
    r  = 100000.000
    dr = r
    for a in self.atoms:
      apos = a.position
      dr = l2norm ( a.position - pos )
      if dr < r :
        na = a
        r  = dr
    # end for
    return na
  # end def

  #                where           what
  # self = host
  def embed( self, host_origo = 0, embed_geom = None, embed_origo = 0 ):
    # absolute coords
    self.cart()
    embed_geom.cart()

    # check
    ho = self.atoms[host_origo]
    eo = embed_geom.atoms[embed_origo]

    print ' Host origo:'
    ho.info()
    print ' Embed origo:'
    eo.info()  
    if eo.symbol != ho.symbol:
      print ' Warning: origo mismatch', ho.symbol, eo.symbol
    # end if

    # TODO
    reo = eo.position
    rho = ho.position
    drh = rho - reo

    print ' Origo shift:', drh
    print ' Origo distance:',l2norm(drh)

    # embed -> host
    frm1="%5d %2s   -> %5d %2s %9.6f %s"
    nearest = {}
    # loop on embed geometry
    print "   Embed   ->     Host  dr"
    for ea in embed_geom.atoms:
      warn = ""
      # shift relative to host origo
      eapos = ea.position
      rh = eapos + drh
      # find the nearest atom to rh vector in host
      ha = self.nearest(rh)
      hapos = ha.position
      dr = l2norm(hapos - rh)
      if dr > 1.000:
        warn = "high dr"
      # end if
      print frm1 %(ea.no,ea.symbol,ha.no,ha.symbol,dr,warn)
      if ea.symbol != ha.symbol:
        print ' Warning: nearest mismatch', ea.symbol, ha.symbol
      # end if
      try:
        nearest[ea.no]
        print ' Warning: found', ea.no
        ea.info()
      except:
        nearest[ea.no] = ha.no
      # end try
    # end for

    # do the embedding
    for eai,hai in nearest.iteritems():
      ea = embed_geom.atoms[eai]
      rea = ea.position + drh
      self.atoms[hai].position = rea
      self.atoms[hai].symbol = ea.symbol
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

  def furthest(self, origo = 0, rmax = 0.400):
    half  = 0.50000000000000000
    one   = 1.00000000000000000
    origo = self.get(origo)
    opos  = origo.position
    ono   = origo.no
    osym  = origo.symbol
    norma = numpy.zeros( 3 )
    for i in range(0,3):
      if opos[i] < half:
        norma[i] = -one
      else:
        norma[i] = one
    # end for

    print "ORIGO %4d %2s %12.9f %12.9f %12.9f" % (ono,osym,opos[0],opos[1],opos[2])
    for atom in self.atoms:
      apos = atom.position
      asym = atom.symbol
      ano  = atom.no
      # normalize
      for i in range(0,3):
        if abs(apos[i] - opos[i]) > half:
          apos[i] += norma[i]
      # end for
      # print apos
      dr = l2norm(apos - opos)
      if dr > rmax:
        print "RMAX  %4d %2s %12.9f %12.9f %12.9f %12.9f" % (ano,asym,apos[0],apos[1],apos[2],dr)
    # end for
  # end def

  def scc_match(self, eps = 0.0100000 ):
    self.geom_match = {}

    self
  # end def

  def match(self, eps = 0.010000000 ):
    self.geom_match = {}
    one = 1.0000000000000000
    if self.geom == None:
      raise Exception("Match geometry not found")

    spos = numpy.zeros([8,3])
    for atom in self.atoms:
      ano  = atom.no
      asym = atom.symbol
      apos = atom.position
      spos = numpy.zeros([8,3])
      lfound = False

      rno  = 0
      rsym = ""
      rpos = numpy.zeros(3)

      # loop over reference
      for aref in self.geom.atoms:
        rno  = aref.no
        rsym = aref.symbol
        rpos = aref.position

        # shift match
        # spos [8,3]
        # i 0 1 2 3 4 5 6 7
        # x 0 *     * *   *
        # y 0   *   *   * *
        # z 0     *   * * *

        spos[0][0] = apos[0]
        spos[0][1] = apos[1]
        spos[0][2] = apos[2]

        spos[1][0] = apos[0]
        spos[1][1] = apos[1]
        spos[1][2] = apos[2]

        spos[2][0] = apos[0]
        spos[2][1] = apos[1]
        spos[2][2] = apos[2]

        spos[3][0] = apos[0]
        spos[3][1] = apos[1]
        spos[3][2] = apos[2]

        spos[4][0] = apos[0]
        spos[4][1] = apos[1]
        spos[4][2] = apos[2]

        spos[5][0] = apos[0]
        spos[5][1] = apos[1]
        spos[5][2] = apos[2]

        spos[6][0] = apos[0]
        spos[6][1] = apos[1]
        spos[6][2] = apos[2]

        spos[7][0] = apos[0]
        spos[7][1] = apos[1]
        spos[7][2] = apos[2]

        spos[1][0] -= one
        spos[2][1] -= one
        spos[3][2] -= one

        spos[4][0] -= one
        spos[4][1] -= one

        spos[5][0] -= one
        spos[5][2] -= one

        spos[6][1] -= one
        spos[6][2] -= one

        spos[7][0] -= one
        spos[7][1] -= one
        spos[7][2] -= one

        # check with shifted
        for i in range(0,8):
          if l2norm(rpos-spos[i]) < eps:
            # found direct match
            try:
              #print "Before try ano:",ano
              # print self.geom_match
              self.geom_match[ano]
            except:
              self.geom_match[ano] = rno
              # print "Shifted from :",ano,asym,apos
              #print "Shifted to   :",rno,rsym,rpos
              if asym != rsym:
                print "Warning: Symbol mismatch:",ano,asym,rno,rsym
              lfound = True
              break
            else:
              print "Error: Match already found:", ano
            # end if
          # end if
        # end for shifted

      # end for aref

      if not lfound:
        print "No match: %4d %2s %12.9f %12.9f %12.9f" % (ano,asym,apos[0],apos[1],apos[2])

    # end for atom
    # print self.geom_match
  # end def

  ### Parallel

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
    print " TF/rotate origo"
    atom.info()
    print " TF/rotate",u,t

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
