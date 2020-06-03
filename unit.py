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
  failed = int( testsuite.attrib["errors"] ) + int( testsuite.attrib["failures"] )
  skipped = int( testsuite.attrib["disabled"] ) if "disabled" in testsuite.attrib else 0
  success = int( testsuite.attrib["tests"] ) - failed - skipped
  return subpage, success, failed, skipped
  
def createTestData( dictionary ):
  data  = [ [ "flag", "status", "test", "time" ] ]
  data += [ [ gr(len(x)), len(x), x.attrib["name"], x.attrib["time"] ] \
      for x in dictionary \
      if "classname" in x.attrib ]
  return data
  
##########################################################################################
# plotting and creating texts
def createTestDonut( title, success, failed, skipped ):
  plotHeaders = [ "success", "failed", "skipped" ]
  return plot.donut( title, plotHeaders, [ success, failed, skipped] )
  
def createTestText( title, plot, data, additionalText = "" ):
  text  = h2( title )
  text += "\n" 
  text += additionalText
  text += plot 
  text += table( data )
  return text

##########################################################################################
# handling subpages and creating main page
def createTestSuiteSubpage( testsuite ):
  subpageTitle, success, failed, skipped = parseTestSuite(testsuite)
  subpageData = createTestData( testsuite )
  subpageDonut = createTestDonut( subpageTitle, failed, skipped, success )
  subpageText = createTestText( "Tests", subpageDonut, subpageData )
  createPage( subpageTitle, subpageTitle, subpageText )
  return subpageTitle, success, failed, skipped

def createPlatformSubpage( platformTitle, platformDict  ):
  platformDonut = createTestDonut( platformTitle, platformDict["success"], platformDict["failed"], platformDict["skipped"] )
  platformData =  platformDict["table"]
  platformText = createTestText( platformTitle, platformDonut, platformData )
  createPage( platformTitle, platformTitle, platformText)
  return [slink( platformTitle )]

def appendPlatformDict( platformDict, subpageTitle, success, failed, skipped ):
  platformName = subpageTitle.split(".")[0]
  if platformName not in platformDict:
      platformDict[platformName] = { "skipped" : 0, "success":0, "failed":0, "subpages":[] }
      platformDict[platformName]["table"] = [[ "flag", "test", "success", "failed", "skipped" ]]

  platformDict[platformName]["success"] += success
  platformDict[platformName]["failed"] += failed
  platformDict[platformName]["skipped"] += skipped
  platformDict[platformName]["subpages"] += [subpageTitle]
  platformDict[platformName]["table"] += [[ gr( failed ), 
                                                ilink(subpageTitle,subpageTitle),
                                                success,
                                                failed,
                                                skipped
                                                ]]

def textSummary( success, failed, skipped ):
    text = "\n\n"
    if failed == 0:
        text += "> All {} active tests have been run successfully.\n".format( success )
    else:
        text += "> The current build suffers regression!\n"
        text += "> {} of {} active tests failed and shall be fixed as soon as possible.\n".format( failed, success+failed+skipped )

    if skipped == 0:
        text += "> No tests have been skipped.\n"
    else:
        text += "> Unfortunately, {} test cases had to be de-activated by the developers after careful consideration\n".format( skipped )


    text += "> Please refer to the individual platform subpages (see table) for the results of individual tests.\n"
    text += "\n\n"
    return text

def main( unit = [] ):
  """
  main method of unit test import / export module

  unit - is a list of (xml) filenames of junit test results
  """
  title = "Test Results - Unit Test"

  subpages = []
  platformDict = {} # "x64" : { "success":0, "fail":1, "skipped":1, "table": [[ red, link, 0, 1, 0 ], ...]}

  ## loop over all files and testsuites and extract platform info (tests are named UnitTestx64.testxyz)
  ## this creates layer 3 test pages ( with individual test "suite" test results )
  for f in unit:
    for testsuite in getTestSuitesFromXML(f):
      subpageTitle, success, failed, skipped = createTestSuiteSubpage( testsuite )
      appendPlatformDict( platformDict, subpageTitle, success, failed, skipped )
      subpages += [ slink( subpageTitle ) ]
      
  ## this creates layer 2 test pages ( with a summary for the respective platform, e.g. x64 )
  subpages += [createPlatformSubpage( x, platformDict[x] ) for x in platformDict ]


  ## this creates the layer 1 (main report) overview with results of each platform
  overallTableData = [[ "flag", "platform", "success", "failed", "skipped"  ]]
  overallTableData += [[ gr(platformDict[x]["failed"]), ilink(x,x), platformDict[x]["success"], platformDict[x]["failed"], platformDict[x]["skipped"] ] for x in platformDict]
  overallSuccess, overallFailed, overallSkipped = [ sum( [ platformDict[x][y] for x in platformDict ] ) for y in ["success", "failed", "skipped" ] ]
  overallDonut = createTestDonut( title, overallSuccess, overallFailed, overallSkipped )
  additionalText = textSummary( overallSuccess, overallFailed, overallSkipped )
  overallText = createTestText( title, overallDonut, overallTableData, additionalText )
  return overallText, subpages
