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
  fail = int( testsuite.attrib["errors"] ) + int( testsuite.attrib["failures"] )
  skipped = int( testsuite.attrib["disabled"] ) if "disabled" in testsuite.attrib else 0
  success = int( testsuite.attrib["tests"] ) - fail - skipped
  return subpage, fail, skipped, success
  
def createTestData( dictionary ):
  data  = [ [ "flag", "status", "test", "time" ] ]
  data += [ [ gr(len(x)), len(x), x.attrib["name"], x.attrib["time"] ] \
      for x in dictionary \
      if "classname" in x.attrib ]
  return data
  
##########################################################################################
# plotting and creating texts
def createTestDonut( title, fail, skipped, success ):
  plotHeaders = [ "success", "failed", "skipped" ]
  return plot.donut( title, plotHeaders, [ success, fail, skipped] )
  
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
  subpageTitle, fail, skipped, success = parseTestSuite(testsuite)
  subpageData = createTestData( testsuite )
  subpageDonut = createTestDonut( subpageTitle, fail, skipped, success )
  subpageText = createTestText( "Tests", subpageDonut, subpageData )
  createPage( subpageTitle, subpageTitle, subpageText )
  return success, fail, skipped, subpageTitle

def main( unit = [] ):
  title = "Test Results - Unit Test"
  overallTableData = [[ "flag", "platform", "success", "failed", "skipped"  ]]

  overallSuccess = 0
  overallErrors = 0
  overallSkipped = 0

  subpages = []

  platformDict = {}

  for f in unit:
    for testsuite in getTestSuitesFromXML(f):
      success, fail, skipped, subpage = createTestSuiteSubpage( testsuite )
      platformName = subpage.split(".")[0]
      if platformName not in platformDict:
          platformDict[platformName] = { "skipped" : 0, "success":0, "fail":0, "subpages":[] }
          platformTableData = [[ "flag", "test", "success", "failed", "skipped" ]]
          platformDict[platformName]["table"] = platformTableData
      platformDict[platformName]["success"] += success
      platformDict[platformName]["fail"] += fail
      platformDict[platformName]["skipped"] += skipped
      platformDict[platformName]["subpages"] += [subpage]
      platformDict[platformName]["table"] += [[ gr( fail ), 
                                                ilink(subpage,subpage),
                                                success,
                                                fail,
                                                skipped
                                                ]]
      overallSuccess += success
      overallErrors += fail
      overallSkipped += skipped

      subpages += [ slink( subpage ) ]
      
  for x in platformDict:
    subpages += [slink( x ) ]
    platformText = h2( "Overview" )
    platformText += createTestDonut( x, platformDict[x]["fail"], platformDict[x]["skipped"], platformDict[x]["success"] )
    platformText += table( platformDict[x]["table"] )
    createPage( x, x, platformText)

    overallTableData.append( [ 
        gr(platformDict[x]["fail"]), 
        ilink(x,x), 
        platformDict[x]["success"],
        platformDict[x]["fail"], 
        platformDict[x]["skipped"] ])
  overallDonut = createTestDonut( title, overallErrors, overallSkipped, overallSuccess )
  overallText = createTestText( title, overallDonut, overallTableData)
  return overallText, subpages
