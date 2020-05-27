import re
from md import *

def parseErrors( f ):
  text = ""
  nlines = 1
  errors = 0
  errorsSuppressed = 0
  leaks = 0
  leaksSuppressed = 0
  for l in f:
    if l.startswith( "==" ):
      match = re.match( "==[0-9]+== .* ([^ ]+): [0-9]+ bytes? in ([0-9]+) block", l )
      if match:
        if match.group(1) == "suppressed":
          leaksSuppressed += int( match.group(2) )
        elif match.group(1) in ["lost", "reachable"]:
          leaks += int( match.group(2) )
      match = re.match("==[0-9]+== ERROR SUMMARY: ([0-9]+) errors.*\(suppressed ([0-9]*)", l)
      if match:
        errors += int( match.group(1))
        errorsSuppressed += int( match.group(2))
    text += "{:05}: ".format( nlines )
    text += "{}".format( re.sub(r"[`]+", "`", l ))
    nlines += 1
  return text, nlines, errors, errorsSuppressed, leaks, leaksSuppressed

def createLogDonut( title, success, errors, leaks ):
  plotHeaders = [ "success", "errors", "leaks" ]
  return plot.donut( title, plotHeaders, [ success, errors, leaks ] )

def createSubpage( f, subpage):
  log, nlines, errors, errorsSuppressed, leaks, leaksSuppressed = parseErrors( f )
  text  = h2( subpage )
  text += createLogDonut( subpage, 1 if errors+leaks == 0 else 0, errors, leaks )
  tableData = [["type", "count" ]]
  tableData.append( ["lines", nlines ] )
  tableData.append( ["errors", errors ] )
  tableData.append( ["errors suppressed", errorsSuppressed] )
  tableData.append( ["leaks", leaks ] )
  tableData.append( ["leaks suppressed", leaksSuppressed ] )
  text += table( tableData )
  text += "\n\n"

  text += h2( "Complete Log" )
  text += "\n"
  text += "~~~~~.txt\n"
  text += log
  text += "\n~~~~~\n"

  createPage( subpage, subpage, text )
  return errors, leaks
    

def main( filenames ):
  data = [["flag", "valgrind report", "errors", "leaks" ]]
  result = h2( "Test Report - Memcheck" )
  subpages = []
  success = 0
  errors = 0
  leaks = 0

  for filename in filenames:
    with open( filename, "r" ) as f:
      subpage = "Memcheck - {}".format( filename )
      nerrors, nleaks = createSubpage( f, subpage )
      errors += min( nerrors, 1 )
      leaks += min(nleaks, 1 )
      success += 1 if nerrors + nleaks == 0 else 0
      
      data.append( [ 
          gr( nerrors + nleaks ),
          ilink( subpage, subpage ),
          nerrors,
          nleaks
        ] )
      subpages.append( slink( subpage ))
  result += createLogDonut( "Memcheck Overview", success, errors, leaks )
  result += table( data )
  return result, subpages
