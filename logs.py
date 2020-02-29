import json
from md import *

def parseErrors( filehandle, subpage ):
  text = ""
  n_lines = 1
  errors = []
  for l in filehandle:
    if "ERROR" in l:
      errorName = subpage + "_" + str(n_lines)
      text += "\\anchor " + errorName + "\n"
      errors.append( errorName )
    text += "{:05}: {}\n".format( n_lines, l )
  return text, errors

def createSubpage( filename, dictionary ):
  log, errors = parseErrors( filename )
  text  = h2( "Errors" )
  for e in errors:
    text += "* \\ref " + e + "\n"

  text += h2( "Complete Log" )
  text += "~~~~.txt"
  text += 
  text += "~~~~"

  createPage( filename, filename, text )
    

def main( filenames ):
  data = [["log", "lines", "errors" ]]
  result = h2( "Log Files" )

  for f in filenames:
    with open( f, "r" ) as logfile:
      subpage = "{} {} {} {}".format(
        env["type"], env["platform"], env["os"], env["host"] 
          )
      createSubpage( subpage, env )
      
      data.append( [ 
          slink( subpage ),
          env["platform"], 
          env["host"], 
          len( env["packages"] )
        ] )
  result += table( data )
  return result
