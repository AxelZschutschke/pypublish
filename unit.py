import xml.etree.ElementTree as ET
from md import *

def create_subpage( filename, dictionary ):
  text  = h2( "Overview" )
  data  = [ [ "Type", "Value" ] ]
  data += [ [ x, dictionary[x] ] for x in dictionary if x != "packages" ]
  text += table( data )

  text += h2( "Installed Packages" )
  data  = [ [ "Package", "Version" ] ]
  data += [ [ x, dictionary["packages"][x] ] for x in dictionary["packages"] ]
  text += table( data )

  createPage( filename, filename, text )
    

def main( filenames ):
  data = [["type", "success", "failed", "skipped", "total" ]]
  result = h2( "Test Results" )

  for f in filenames:
    testresult = ET.parse( f )
    subpage = "testresult_{}".format(
      env["type"], env["platform"], env["os"], env["host"] 
        )
    create_subpage( subpage, env )
    
    data.append( [ 
        slink( subpage ),
        env["platform"], 
        env["host"], 
        len( env["packages"] )
      ] )
  result += table( data )
  return result
