import re
from md import *

def parseErrors_pureMD( f, subpage ):
  text = "\n\n~~~~~\n"
  nlines = 1
  errors = []
  counter = 0
  for l in f:
    upper = l.upper()
    if "ERROR" in upper or "FAIL" in upper:
      errors.append( nlines )
      text += "[FAIL] "
    else:
      text += "[    ] "
    text += "{:05}: ".format( nlines )
    text += "{}".format( l.replace( "~", "&tilde;" ).replace( "\n", "" ))
    text += "\n"
    nlines += 1
    if nlines % 10 == 0:
      # too long texts are not formatted as pre-formatted text
      text += "~~~~~\n\n\n~~~~~\n"
  text += "~~~~~\n\n"
  return text, nlines, errors
    
def createLogDonut( title, errors, success ):
  plotHeaders = [ "success", "failed" ]
  return plot.donut( title, plotHeaders, [ success, errors] )

def createSubpage_pureMD( f, subpage):
  log, nlines, errors = parseErrors_pureMD( f, subpage)
  #text  = h2( "Errors" )
  #for e in errors:
  #  text += "* line " + str(e) + "\n"

  text = h2( "Complete Log" )
  text += log

  createPage( subpage, subpage, text )
  return nlines, len( errors )


def main( filenames ):
  data = [["flag", "log", "lines", "errors" ]]
  result = h2( "Log Files" )
  subpages = []
  total = 0
  errors = 0

  for f in filenames:
    with open( f, "r" ) as logfile:
      f = f.replace( ".", "_" ).split( "/" )[-1]
      subpage = "Log File - {}".format( f )
      nlines, nerrors = createSubpage_pureMD( logfile, subpage )
      errors += min( nerrors, 1 )
      total += 1
      
      data.append( [ 
          gr( nerrors ),
          ilink( subpage, subpage ),
          nlines,
          nerrors
        ] )
      subpages.append( slink( subpage ))
  result += createLogDonut( "Log File Overview", errors, total-errors )
  result += table( data )
  return result, subpages
