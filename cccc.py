import xml.etree.ElementTree as ET
import md 

projectSummaryFeatures = [
  "number_of_modules",
  "lines_of_code",
  "lines_of_comment",
  "McCabes_cyclomatic_complexity",
  "lines_of_code_per_lines_of_comment",
  "McCabes_cyclomatic_complexity_per_lines_of_comment",
  "rejected_lines_of_code"
  ]

proceduralFeatures = [
  "name",
  "lines_of_code",
  "lines_of_comment",
  "McCabes_cyclomatic_complexity",
  "lines_of_code_per_lines_of_comment",
  "McCabes_cyclomatic_complexity_per_lines_of_comment"
  ]

ooFeatures = [
  "name",
  "weighted_methods_per_class_unity",
  "depth_of_inheritance_tree",
  "number_of_children",
  "coupling_between_objects"
  ]

structuralFeatures = [
  "name",
  "fan_in",
  "fan_out"
  ]

##########################################################################################
# XML file handling
def getRootFromXML( filename ):
  testresult = ET.parse( filename )
  return testresult.getroot()
    
def getTimestamp( xmlRoot ):
  return xmlRoot.find( "timestamp" ).text

def extractFeaturesOfSection( section, features ):
  result = {}
  for feature in features:
    if feature == "name":
      result[feature] = project_summary.find( feature ).text
    else:
      result[feature] = projectSummary.find( feature ).get("value")
  return result

def parseProjectSummary( xmlRoot ):
  projectSummary = xmlRoot.find( "project_summary" )
  return extractFeaturesOfSection( projectSummaryFeatures )

def parseProceduralSummary( xmlRoot ):
  proceduralSummary = xmlRoot( "procedural_summary" )
  result = []
  for module in proceduralSummary.findall( "module" ):
    result.append( extractFeaturesOfSection( module ) )
  return result

def parseOOSummary( xmlRoot ):
  ooSummary = xmlRoot( "oo_design" )
  result = []
  for module in ooSummary.findall( "module" ):
    result.append( extractFeaturesOfSection( module ) )
  return result

def parseStructuralSummary( xmlRoot ):
  structuralSummary = xmlRoot( "structural_summary" )
  result = []
  for module in structuralSummary.findall( "module" ):
    result.append( extractFeaturesOfSection( module ) )
  return result

##########################################################################################
# plotting and creating texts
def projectSummary( data, explanation=True ):
  text = md.h2( "Project Summary" )
  text += "code counters / metrics calculated using CCCC\n"
  if explanation:
    text += "for explanations, please refer to the detailed report on the "
    text += ilink( "CCCC report", "cccc_report" )
    text += "subpage\n\n"
  tableData = [[ "metric", "value" ]]
  for feature in projectSummaryFeatures:
    tableData += [ feature.replace( "_", " " ), data[feature] ]
  text += md.table( tableData )
  return text

def structuralSummary( data ):
  text = md.h2( "Procedural Summary" )
  tableData = [[ "module", "LOC", "COM", "MVG", "L_C", "M_C" ]]
  for module in data:
    tableData += [ value for value in proceduralFeatures ]
  text += md.table( tableData )
  return text

def ooSummary( data ):
  text = md.h2( "Object Oriented Design Summary" )
  tableData = [[ "module", "WMC", "DIT", "NOC", "CBD" ]]
  for module in data:
    tableData += [ value for value in ooFeatures ]
  text += md.table( tableData )
  return text

def structuralSummary( data ):
  text = md.h2( "Structural Summary" )
  tableData = [[ "module", "FI", "FO" ]]
  for module in data:
    tableData += [ value for value in structuralFeatures ]
  text += md.table( tableData )
  return text

##########################################################################################
# handling subpages and creating main page
def createCCCCSubpage( xml ):
  projectSummaryData = parseProjectSummary( xml )
  proceduralSummaryData = parseProceduralSummary( xml )
  ooSummaryData = parseOOSummary( xml )
  structuralSummaryData = parseStructuralSummary( xml )

  text = md.h2( "Explanations" )
  text += """
The following code metrics are reported:"

 * NOM **number of modules** - the number of non-trivial modules identified by the analyzer
 * LOC **lines of code** - the number of non-blank, non-comment lines of code
 * COM **lines of comments** - the number of lines of comment
 * MVG **McCabe's cyclomatic complexibility number [wikipedia](https://de.wikipedia.org/wiki/McCabe-Metrik)
 * L_C **lines of code per lines of comment**
 * M_C **McCabe's cyclomatic complexibility per lines of comment**
 * REJ **rejected lines of code** which the analyzer refused to process
 * WMC **(weighted) methods per class** weight=1, represents the number of methods per class
 * DIT **depth of inheritance tree** length of longest path of inheritance ending in this module
 * NOC **number of children** number of children which inherit directly from this module
 * CBD **coupling between objects** number of modules which are coupled directly to this module (either client or supplier)
 * FI **fan-in** number of modules passing information into this module
 * FO **fan-out** number of modules into which this module passes information

For more details, please refer to the CCCC documentation (and output HTML files)
"""
  text += projectSummary( projectSummaryData, False )

  text += proceduralSummary( proceduralSummaryData )
  text += ooSummary( ooSummaryData )
  text += structuralSummary( structuralSummaryData )

  createPage( "Code Metrics", "cccc_report", text)
  return proceduralSummaryData

def main( cccc = [] ):
  title = "Code Metrics - CCCC"
  subpages = ["cccc_report"]
  ccccXml = getRootFromXML( cccc[0] )
  
  projectSummaryData = createCCCCSubpage( ccccXml )

  return projectSummary( projectSummaryData ), subpages
