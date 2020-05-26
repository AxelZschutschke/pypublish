import re
import md 
import plot

def parseResults( f ):
  success = 0
  error = 0
  warning = 0
  text = ""

  for line in f:
    line = line.strip()
    success += 1 if line.startswith( "[   OK   ]" )
    error += 1 if line.startswith(   "[ FAILED ]" )
    warning += 1 if line.startswith( "[  WARN  ]" )
    text += line

  return text, error, warning, success

def createDetailDonut( title, errors, warning, success ):
  plotHeaders = [ "success", "failed", "skipped" ]
  return plot.donut( title, plotHeaders, [success, errors, warning ] )

def createOverviewDonut( title, errors, total ):
  plotHeaders = [ "success", "failed" ]
  return plot.donut( title, plotHeaders, [total-errors, errors ] )

def createSubpage( f, subpage):
  log, error, warning, success= parseResults( f )
  text  = h2( subpage )
  
  text += createDetailDonut( subpage, error, warning, success )

  text += h2( "Complete Log" )
  text += "\n"
  text += "~~~~~.txt"
  text += log
  text += "~~~~~"

  createPage( subpage, subpage, text )
  return errors, warning, success    

def main( filenames ):
  data = [["flag", "component", "success", "warning", "errors" ]]
  subpages = []

  errors = 0
  total = 0
  for f in filenames:
    with open( f, "r" ) as securityFile:
      f = f.replace( ".", "_" )
      subpage = "Security Result - {}".format( f )
      error, warning, success = createSubpage( securityFile, subpage )
      errors += 1 if error + warning > 0 else 0
      total += 1
      
      data.append( [ 
          gr( error ),
          ilink( subpage, subpage ),
          success,
          warning,
          error
        ] )
      subpages.append( slink( subpage ))

  result = h2( "Security Checks" )
  result += createOverviewDonut( "Modules", errors, total )
  result += table( data )
  return result, subpages
