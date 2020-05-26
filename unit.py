import xml.etree.ElementTree as ET
from md import *
import plot

##########################################################################################
# XML file handling
def getTestSuitesFromXML( filename ):
  testresult = ET.parse( filename )
  return testresult.getroot()
    
def parseTestSuite( testsuite ):
  subpage = "Test Result - Unit Test - {}".format( testsuite.attrib["name"] ) 
  errors = int( testsuite.attrib["errors"] ) + int( testsuite.attrib["failures"] )
  skipped = int( testsuite.attrib["disabled"] ) if "disabled" in testsuite.attrib else 0
  success = int( testsuite.attrib["tests"] ) - errors - skipped
  return subpage, errors, skipped, success
  
def createTestData( dictionary ):
  data  = [ [ "flag", "status", "test", "time" ] ]
  data += [ [ gr(len(x)), len(x), x.attrib["classname"], x.attrib["time"] ] \
      for x in dictionary \
      if "classname" in x.attrib ]
  return data
  
##########################################################################################
# plotting and creating texts
def createTestDonut( title, errors, skipped, success ):
  plotHeaders = [ "success", "failed", "skipped" ]
  return plot.donut( title, plotHeaders, [ success, errors, skipped] )
  
def createTestText( title, plot, data ):
  text  = h2( title )
  text += "\n" 
  text += plot 
  text += "\n\n"
  text += table( data )
  return text

##########################################################################################
# handling subpages and creating main page
def createTestSuiteSubpage( testsuite ):
  subpageTitle, errors, skipped, success = parseTestSuite(testsuite)
  subpageData = createTestData( testsuite )
  subpageDonut = createTestDonut( subpageTitle, errors, skipped, success )
  subpageText = createTestText( "Tests", subpageDonut, subpageData )
  createPage( subpageTitle, subpageTitle, subpageText )
  return success, errors, skipped, subpageTitle

def main( unit = [] ):
  title = "Test Results - Unit Test"
  tableData = [[ "flag", "test", "success", "failed", "skipped"  ]]

  overallSuccess = 0
  overallErrors = 0
  overallSkipped = 0

  subpages = []

  for f in unit:
    for testsuite in getTestSuitesFromXML(f):
      success, errors, skipped, subpage = createTestSuiteSubpage( testsuite )
      tableData.append( [ gr(errors), ilink(subpage,subpage), success, errors, skipped ])
  
      overallSuccess += success
      overallErrors += errors
      overallSkipped += skipped

      subpages += [ slink( subpage ) ]
      
  overallDonut = createTestDonut( title, overallErrors, overallSkipped, overallSuccess )
  overallText = createTestText( title, overallDonut, tableData )
  return overallText, subpages
