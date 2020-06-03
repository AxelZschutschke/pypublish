import json
from md import *

def create_subpage( filename, dictionary ):
  text  = h2( "Overview" )
  data  = [ [ "Type", "Value" ] ]
  data += [ [ x, dictionary[x] ] for x in dictionary if not x in [ "packages", "custom" ] and dictionary[x] ]
  text += table( data )

  if "custom" in dictionary:
      text += h2( "Custom Installations" )
      data  = [ [ "Package", "Version" ] ]
      data += [ [ x, dictionary["custom"][x] ] for x in dictionary["custom"] ]
      text += table( data )

  text += h2( "Installed Packages" )
  data  = [ [ "Package", "Version" ] ]
  data += [ [ x, dictionary["packages"][x] ] for x in dictionary["packages"] ]
  text += table( data )

  createPage( filename, filename, text )
    

def main( filenames ):
  data = [["os", "platform", "hostname", "# packages" ]]
  result = h2( "Build Environments" )

  subpages = []

  for f in filenames:
    with open( f, "r" ) as jsonfile:
      env = json.load( jsonfile )
      subpage = "{} {} {} {}".format(
        env["type"], env["platform"], env["os"], env["host"] 
          )
      create_subpage( subpage, env )
      
      data.append( [ 
          ilink( env["os"], subpage ),
          env["platform"], 
          env["host"], 
          len( env["packages"] )
        ] )
      subpages.append( slink( subpage ) )
  result += table( data )
  return result, subpages
