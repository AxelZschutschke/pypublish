import xml.etree.ElementTree as ET
from md import *
import plot

def create_subpage( filename, dictionary, testdonut ):
  text  = h2( "Tests" )
  
  text += "\n" + testdonut + "\n\n"
  
  data  = [ [ "status", "test", "time" ] ]
  data += [ [ len(x), x.attrib["classname"], x.attrib["time"] ] for x in dictionary if "classname" in x.attrib ]
  formatter = [ gr, nn, nn ]
  text += table( data, formatter  )
  createPage( filename, filename, text )
    

def main( unit = [], integration = [], system = [] ):
  data = [["test", "success", "failed", "skipped" ]]
  result = h2( "Test Results" )

  overall_success = 0
  overall_errors = 0
  overall_skipped = 0
  for f in unit:
    testresult = ET.parse( f )
    suites = testresult.getroot()

    for testsuite in suites:
      subpage = "Test Result - Unit Test - {}".format( testsuite.attrib["name"] ) 
      errors = int( testsuite.attrib["errors"] ) + int( testsuite.attrib["failures"] )
      skipped = int( testsuite.attrib["disabled"] ) if "disabled" in testsuite.attrib else 0
      success = int( testsuite.attrib["tests"] ) - errors - skipped
      testdonut = plot.donut( subpage, data[0][1:], [ success, errors, skipped ] )
      testresult = create_subpage( subpage, testsuite, testdonut )
      data.append( [ slink( subpage ), success, errors, skipped ])
  
      overall_success += success
      overall_errors += errors
      overall_skipped += skipped
      
  result += plot.donut( "Test Result - Unit Test", data[0][1:], [ overall_success, overall_errors, overall_skipped ] )
  formatter = [ nn, ng, nr, ny ]
  result += table( data, formatter )
  return result
