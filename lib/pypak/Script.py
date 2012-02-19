#
# Script
#

import os
import sys
import string
import numpy
from ConfigParser import ConfigParser
from optparse     import OptionParser
from pypak.Types  import *

class Script( Debug ):
  def __init__( self, gbn = os.path.basename( sys.argv[0] ), 
                      cfg = os.path.basename( sys.argv[0] ) + ".ini" ):
    Debug.__init__( self )
    self.gbn = gbn
    self.opt = OptionParser()
    self.cfg = ConfigParser()
    try:
      self.cfg.read( cfg )
    except:
      print "Configuration not found:", cfg
      sys.exit(1)
  # end def

  def option( self, *args, **kwargs ):
    self.opt.add_option( *args, **kwargs )
  # end def

  def init( self ):
    self.option( "-c", "--config", action = "store", type = "string", dest = "gcn", 
              default = "config.ini", help = "Configuration File" )

    self.option( "-v", "--verbose", action = "store_true", dest = "verbose", 
              default = False, help = "Verbose Mode" )

    self.option( "-w", "--debug", action = "store_true", dest = "debug", 
              default = False, help = "Debug Mode" )


    (opts,args) = self.opt.parse_args()
    self.verbose = opts.verbose
    self.debug   = opts.debug
  # end def

  def parse( self ):
    return self.opt.parse_args()
  # end def

  def cfgint( self, opt = None ):
    return self.cfg.getint( self.gbn, opt )
  # end def


  def cfgfloat( self, opt = None ):
    return self.cfg.getfloat( self.gbn, opt )
  # end def


  def cfgarray( self, opt = None ):
    line = self.cfg.get( self.gbn, opt )
    return line.split();
  # end def


  def cfgiarray( self, opt = None ):
    array = self.cfgarray( opt )
    for i in range( 0, len( array ) ):
      array[i] = string.atoi( array[i] )
    # end for
    return numpy.array( array )
  # end def


  def cfgfarray( self, opt = None ):
    array = self.cfgarray( opt )
    for i in range( 0, len( array ) ):
      array[i] = string.atof( array[i] )
    # end for
    return numpy.array( array )
  # end def
# end class
