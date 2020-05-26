import json
import re
from md import *

#def parseErrors( f, subpage ):
#  text = ""
#  nlines = 1
#  errors = []
#  for l in f:
#    upper = l.upper()
#    if "ERROR" in upper or "FAIL" in upper:
#      errorName = subpage + "_" + str(nlines)
#      text += "`````\n"
#      text += red()
#      text += "\\anchor " + errorName + "\n"
#      text += "`````\n"
#      errors.append( errorName )
#    text += "{:05}: {}".format( nlines, re.sub(r"[`]+", "`", l ) )
#    #text += "{:05}: {}".format( nlines, l.replace( "`", "`" ))
#    nlines += 1
#  return text, nlines, errors

def parseErrors( f, subpage ):
  text = ""
  nlines = 1
  errors = []
  for l in f:
    upper = l.upper()
    if "ERROR" in upper or "FAIL" in upper:
      text += " <pre class=\"pre_fail\">"
      errorName = subpage + "_" + str(nlines)
      errors.append( errorName )
      text += " \\anchor " + errorName + " "
    else:
      text += " <pre class=\"pre_ok\">"
    text += "{:05}: ".format( nlines )
    text += "{}".format( re.sub(r"[`]+", "`", l ).replace( "\n", "" ))
    text += "</pre>\n"
    nlines += 1
  return text, nlines, errors


def createSubpage( f, subpage):
  log, nlines, errors = parseErrors( f, subpage)
  text  = h2( "Errors" )
  for e in errors:
    text += "* \\ref " + e + "\n"

  text += h2( "Complete Log" )
  text += "\n"
  text += log

  createPage( subpage, subpage, text )
  return nlines, len( errors )
    

def main( filenames ):
  data = [["flag", "log", "lines", "errors" ]]
  result = h2( "Log Files" )
  subpages = []

  for f in filenames:
    with open( f, "r" ) as logfile:
      f = f.replace( ".", "_" )
      subpage = "Log File - {}".format( f )
      nlines, nerrors = createSubpage( logfile, subpage )
      
      data.append( [ 
          gr( nerrors ),
          ilink( subpage, subpage ),
          nlines,
          nerrors
        ] )
      subpages.append( slink( subpage ))
  result += table( data )
  return result, subpages
