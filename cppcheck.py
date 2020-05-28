import xml.etree.ElementTree as ET
from md import *
import plot

##########################################################################################
# XML file handling
def getRootFromXML( filename ):
  testresult = ET.parse( filename )
  return testresult.getroot()
    
def parseErrorEntries( xml ):
  errors = []
  errorList = xml.find( "errors" )
  for error in errorList.findall("error"):
    parsedError = {}
    parsedError["id"] = error.get("id" )
    parsedError["message"] = error.get("verbose")
    parsedError["severity"] = error.get("severity")
    parsedError["location"] = []
    for location in error.findall("location"):
      parsedLocation = {}
      parsedLocation["file"] = location.get("file")
      parsedLocation["line"] = location.get("line")
      parsedError["location"].append( parsedLocation )
    errors.append( parsedError ) 
  return errors
  
##########################################################################################
# plotting and creating texts
def getErrorsPerCategory( plotData ):
  plotHeaders = [ "none", "error", "warning", "style", "performance", "portability", "information", "debug" ]
  # count each category (map-reduce)
  plotData = [ sum( [ 1 for x in plotData if x["severity"] == y ] ) for y in plotHeaders ]
  return plotHeaders, plotData

def createCppCheckDonut( title, plotHeaders, plotData):
  return plot.donut( title, plotHeaders, plotData )
  
def createFileExcerpt( location ):
  lineCounter = 0
  firstLine = int( location["line"] ) - 10
  lastLine = firstLine + 20
  excerpt = ""
  try:
    with open( location["file"], "r" ) as f:
      for line in f:
        lineCounter += 1
        if lineCounter > lastLine:
          break
        if lineCounter >= firstLine and lineCounter <= lastLine:
          excerpt += "{:05}: {}".format( lineCounter, line )
  except Exception as e:
    excerpt = "exception occoured while parsing:\n" + str(e)
  return excerpt

##########################################################################################
# handling subpages and creating main page
def createCppCheckSubpage( title, subpage, plot, data ):
  text = h2( "Overview" ) 
  text += plot
  text += "\n\n"
  for error in data:
    text += h2( error["severity"] + " - " + error["id"] )
    text += "**error description:**\n"
    text += "  " + error["message"]
    if error["location"]:
      text += "\n\n"
      for location in error["location"]:
        text += "**location of finding:**\n"
        text += "  {}:{}\n\n".format( location["file"], location["line"] )
        text += "**surrounding code:**\n"
        text += "~~~~~{.cpp}\n"
        text += createFileExcerpt( location )
        text += "~~~~~\n\n"

  createPage( title, subpage, text )
  return subpage

def main( cppcheck = [] ):
  title = "Analysis Report - CppCheck"
  subpages = []

  overviewData = [[ "flag", "report", "findings" ] ]
  overviewPlotData = []
  overviewPlotHeaders = []
  for filename in cppcheck:
    xml = getRootFromXML( filename )
    errors = parseErrorEntries( xml )
    subpageName = "cppCheckReport" + filename.replace( ".xml", "" )
    subpageTitle = "{} - {}".format( title, filename )

    plotHeaders, plotData = getErrorsPerCategory( errors )
    overviewPlotHeaders = plotHeaders
    overviewPlotData.append( plotData )

    plot = createCppCheckDonut( subpageName, plotHeaders, plotData )
    createCppCheckSubpage( subpageTitle, subpageName, plot, errors )

    overviewData.append( [ gr( len( errors ) ), ilink( subpageTitle,subpageName ), sum( plotData ) ])
    subpages += [ slink( subpageName ) ]

  # map/reduce - sum of each category over all input files
  overviewPlotData = [sum([x[i] for x in overviewPlotData ]) for i in range(len(overviewPlotHeaders ))]
  text = ""
  text += h2( title )
  text += createCppCheckDonut( "Analysis Report - CppCheck - Summary", overviewPlotHeaders, overviewPlotData )
  text += table( overviewData )
  return text, subpages
