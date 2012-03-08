#
# Types package
#

import sys
import copy
import string
import math

from pypak.Math import *
from pypak.LX.Lexer import Lexer

class LX( Lexer ):
  def __init__( self, path = None, sysopts = { "verbose" : False, "debug" : False } ):
    Lexer.__init__( self, path, sysopts )
    self.tokens.extend( ['LABEL','SPLIT','EFERMI','NELECT','BAND','NK','VALUE'] )
    self.token = ""
    self.efermi = 0.000
    self.eps = 5
  # end def

  def t_NELECT( self, t ):
    r'nelect.*'
    self.token = "nelect"
    # print "nelect"
  # end def

  def t_SPLIT(self,t):
    r'split.*'
    self.token = "split"
  # end def

  def t_EFERMI( self, t ):
    r'efermi.*'
    self.token = "efermi"
  # end def

  def t_BAND( self, t ):
    r'band.*'
    self.token = "band"
    # print "band"
  # end def

  def t_NK( self, t ):
    r'.*vkpt.*'
    self.token = "nk"
    # print "nk"
  # end def

  def t_LABEL( self, t ):
    r'[A-Za-z_ ]+'
    if self.verbose:
      print "LABEL:" + t.value
    # pass
  # end def
  
  def t_VALUE( self, t ):
    r'[0-9-. ]+'
    val = t.value.split()
    if self.token == "nk":
      print "K-point: %s" % (t.value)
    elif self.token == "efermi":
      self.efermi = string.atof(t.value)
    elif self.token == "split":
      self.split = val[0]
      self.spin  = val[1]
    elif self.token == "nelect":
      self.nelect = string.atoi(val[0])
      self.nelect = math.floor( self.nelect / 2.000 )
    elif self.token == "band":
      val[0] = string.atoi(val[0])
      val[1] = string.atof(val[1])
      val[2] = string.atof(val[2])

      if abs(val[0]-self.nelect) < self.eps:
        print t.value
      # end if
    # end if
  # end def
# end class
