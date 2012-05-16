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
    self.reference = None
  # end def

  def read( self, opts = None ):
    self.rewind()
    self.clean()
    self.state( 1, self.comment )
    self.state( 2, self.comment )
    self.state( 3, self.comment )
    self.state( 4, self.read_efermi )
    self.state( 5, self.comment )
    self.state( 6, self.read_nelect )
    self.state( 7, self.read_eigs )
    File.run( self )
  # end def

  def read_efermi( self ):
    (efermi) = self.line()
    self.efermi = string.atof( efermi[0] )
    self.process()
    # print self.efermi
  # end def

  def read_nelect( self ):
    (nelect,nkpts,nbands) = self.line()
    self.nelect = string.atoi( nelect )
    self.nkpts  = string.atoi( nkpts )
    self.nbands = string.atoi( nbands )
    self.process()
    # print self.nelect
  # end def

  def read_eigs( self ):
    # 5: band,energy1,occupation1,energy2,occupation2
    self.eigs = numpy.zeros((self.nkpts,self.nbands,5))

    for i in range( 0, self.nkpts ):
      if i > 0:
        self.getline()
      self.getline()
      self.getline()
      print "nk", self.line()
      (nk,vkpt1,vkpt2,vkpt3,wtkpt) = self.line()
      self.getline()
      self.getline()
      print "sp", self.line()
      (spl,spin) = self.line()
      self.spl = string.atoi(spl)
      self.getline()

      for j in range(0,self.nbands):
        self.getline()
        print self.line()
        if(self.spl>0):
          (band,eig1,occ1,eig2,occ2) = self.line()
          self.eigs[i][j][0] = string.atof(band)
          self.eigs[i][j][1] = string.atof(eig1)
          self.eigs[i][j][2] = string.atof(occ1)
          self.eigs[i][j][3] = string.atof(eig2)
          self.eigs[i][j][4] = string.atof(occ2)
        else:
          (band,eig1,occ1) = self.line()
          self.eigs[i][j][0] = string.atof(band)
          self.eigs[i][j][1] = string.atof(eig1)
          self.eigs[i][j][2] = string.atof(occ1)
        # end if
      # end for nbands
      # print self.eigs
    # end for nkpts
  # end def

  def grid(self, kp = 0):
    return self.eigs[kp,:,1]
  # end def
# end class
