#
# Script
#

import os
import string
import ConfigParser
from optparse import OptionParser
import numpy
from pypak.Types import *

class Script( Debug ):
  def __init__( self, gbn = os.path.basename( sys.argv[0] ), 
                      gcn = os.path.basename( sys.argv[0] ) + ".ini" ):
    Debug.__init__( self )
    self.gbn = gbn
    self.opt = OptionParser()
    self.gcn = gcn
    self.par = ConfigParser.ConfigParser()
  # end def

  def option( self, *args, **kwargs ):
    self.opt.add_option( *args, **kwargs )
  # end def

  def parse( self ):
    return self.par.parse_args()
  # end def

  def init( self ):
    self.option( "-c", "--config", action = "store", type = "string", dest = "gcn", 
              default = "config.ini", help = "Configuration File" )

    self.option( "-v", "--verbose", action = "store_true", dest = "verbose", 
              default = False, help = "Verbose Mode" )

    self.option( "-w", "--debug", action = "store_true", dest = "debug", 
              default = False, help = "Debug Mode" )


    (_opt, _arg) = self.parse()
    self.verbose = _opt.verbose
    self.debug   = _opt.debug
    self.gcn     = _opt.gcn

    ## Global Config
    try:
      self.gpcpar.readfp( open( self.gpc ) )
      if self.verbose :
        print ' Global: ' + self.gpc
    except:
      if self.verbose :
        print ' Missing: ' + self.gpc
    # end try

    ## Read User Config
    try:
      self.upcpar.readfp( open( self.upc ) )
      if self.verbose :
        print ' User: ' + self.upc
    except:
      if self.verbose :
        print ' Missing: ' + self.upc
    # end try
  # end def


  def cfg( self, item = None ):
    try:
      return self.upcpar.get( self.scn, item )
    except:
      try:
        return self.gpcpar.get( self.scn, item )
      except:
        raise
      # end try
    # end try
  # end def


  def cfgi( self, item = None ):
    return string.atoi( self.cfg( item ) )
  # end def


  def cfgf( self, item = None ):
    return string.atof( self.cfg( item ) )
  # end def


  def cfgarr( self, item = None ):
    line = self.cfg( item )
    return line.split();
  # end def


  def cfgarri( self, item = None ):
    arr = self.cfgarr( item )
    for i in range( 0, len( arr ) ):
      arr[i] = string.atoi( arr[i] )
    # end for
    return numpy.array( arr )
  # end def


  def cfgarrf( self, item = None ):
    arr = self.cfgarr( item )
    for i in range( 0, len( arr ) ):
      arr[i] = string.atof( arr[i] )
    # end for
    return numpy.array( arr )
  # end def
# end class
