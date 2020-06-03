import os

import plot
import md

################## new
#################### FROM THE MANUAL ###########################################
###
###    Following is a quick description of the tracefile  format  as  used  by
###    genhtml, geninfo and lcov.
###
###    A tracefile is made up of several human-readable lines of text, divided
###    into sections. If available, a tracefile begins with the testname which
###    is stored in the following format:
###
###      TN:<test name>
###
###    For  each  source  file  referenced in the .da file, there is a section
###    containing filename and coverage data:
###
###      SF:<absolute path to the source file>
###
###    Following is a list of line numbers for each function name found in the
###    source file:
###
###      FN:<line number of function start>,<function name>
###
###    Next,  there  is a list of execution counts for each instrumented func‐
###    tion:
###
###      FNDA:<execution count>,<function name>
###
###    This list is followed by two lines containing the number  of  functions
###    found and hit:
###
###      FNF:<number of functions found>
###      FNH:<number of function hit>
###
###    Branch coverage information is stored which one line per branch:
###
###      BRDA:<line number>,<block number>,<branch number>,<taken>
###
###    Block  number  and  branch  number are gcc internal IDs for the branch.
###    Taken is either '-' if the basic block containing the branch was  never
###    executed or a number indicating how often that branch was taken.
###
###    Branch coverage summaries are stored in two lines:
###
###      BRF:<number of branches found>
###      BRH:<number of branches hit>
###
###    Then  there  is  a  list of execution counts for each instrumented line
###    (i.e. a line which resulted in executable code):
###
###      DA:<line number>,<execution count>[,<checksum>]
###
###    Note that there may be an optional checksum present  for  each  instru‐
###    mented  line.  The  current  geninfo implementation uses an MD5 hash as
###    checksumming algorithm.
###
###    At the end of a section, there is a summary about how many  lines  were
###    found and how many were actually instrumented:
###
###      LH:<number of lines with a non-zero execution count>
###      LF:<number of instrumented lines>
###
###    Each sections ends with:
###      end_of_record
###

def formatLine_pureMD( line, branch, hits, code ):
    text = ""
    if hits == "0":
        text += "!! "
    else:
        text += "   "
    text += "{:4} : {:6} : {:4} : {}\n".format( line, branch, hits, md.removeSpecial( code ) )
    return text

def createCoverageSourceFile_pureMD( title, sub):
    text = ""
    text += "***full path:*** " + sub["fullpath"]
    text += "\n\n"
    text += "***source code:*** " 
    text += "\n\n"
    text += "~~~~~\n"
    try:
        with open( sub["fullpath"], "r" ) as f:
            lines = f.readlines()
            text += formatLine_pureMD( "line", "branch", "hits", "code" )
            for idx, line in enumerate( lines ):
                counter = sub["DA"][idx+1] if "DA" in sub and idx + 1 in sub["DA"] else " "
                branchData = sub["BRDA"][idx+1] if "BRDA" in sub and idx + 1 in sub["BRDA"] else ""
                while len( branchData ) > 6:
                    text += formatLine_pureMD( idx + 1, branchData[:6], "", "" )
                    branchData = branchData[6:]
                text += formatLine_pureMD( idx+1, branchData, counter, line )
    except Exception as e:
        text = "exception occoured creating page:"
        text += str(e)
    text += "~~~~~\n\n"
    md.createPage( title, title, text)

def importCoverage( filename ):
    total = {}
    current = None
    results = {} ## folder : { source : { FNF, FNH, ..., BRDA : [], DA: [] }}

    counters = [ 
                "FNF", # functions found
                "FNH", # ... hit
                "BRF", # branches found
                "BRH", # ... hit
                "LF",  # lines found
                "LH"   # ... hit
                ]
    for k in counters:
        total[k] = 0

    with open( filename, "r" ) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith( "end_of_record" ): ## end of one SF entry
                current = None
            if line.startswith( "SF" ): # source file
                fullpath = line.replace("\n","").split(":")[1]
                folder, filename = line.replace("\n","").split("/")[-2:]
                if folder not in results:
                    results[folder] = {}
                results[folder][filename] = {}
                current = results[folder][filename]
                current["fullpath"] = fullpath
            if line.startswith( "DA" ): # line data (linenumber + number of hits total)
                if not "DA" in current:
                    current["DA"] = {}
                ln,counter = line.replace("\n","").split(":")[1].split(",")
                current["DA"][int(ln)] = counter
            if line.startswith( "BRDA" ): # branch data (lines repeat for each branch per line of source code)
                if not "BRDA" in current:
                    current["BRDA"] = {}
                ln,ids,branch,counter = line.replace("\n","").split(":")[1].split(",")
                ln = int( ln )
                if ln not in current["BRDA"]:
                    current["BRDA"][ln] = ""
                if counter == "-":
                    current["BRDA"][ln] += "#"
                elif counter == "0":
                    current["BRDA"][ln] += "-"
                else:
                    current["BRDA"][ln] += "+"

            for k in counters:
                if line.startswith( k ):
                    value = int( line.split( ":" )[1] )
                    if not k in current:
                        current[k] = 0
                    current[k] += value
                    total[k] += value
    return results, total

def getCoverage( total ):
    lhit = total["LH"] if "LH" in total else 0
    ltot = total["LF"] if "LF" in total else 0
    fhit = total["FNH"] if "FNH" in total else 0
    ftot = total["FNF"] if "FNF" in total else 0
    bhit =  total["BRH"] if "BRH" in total else 0
    btot =  total["BRF"] if "BRF" in total else 0
    return lhit, ltot, fhit, ftot, bhit, btot

def formatPercent( hit, tot ):
    result = "--- % (   0/   0)"
    if tot > 0:
        result = "{:3} % ({:4}/{:4})".format( int( hit * 100 / tot ), hit, tot )    
    return result

def folderSum( resultFolder, name ):
    hit = 0
    tot = 0
    for f in resultFolder:
        if name+"H" in resultFolder[f]:
            hit += resultFolder[f][name + "H"]
        if name+"F" in resultFolder[f]:
            tot += resultFolder[f][name + "F"]
    return formatPercent( hit, tot )

def createCoverageDonut( title, hit, tot ):
  plotHeaders = [ "hit", "miss"]
  return plot.donut( title, plotHeaders, [ hit, tot-hit ] )

def createSubpage( project, title ):
    text = ""
    subpages = []

    results, total = importCoverage( project )
    lhit, ltot, fhit, ftot, bhit, btot = getCoverage( total )

    projectData = [[ "folder", "lines", "functions", "branches" ]]
    projectData += [[ 
        folder, 
        folderSum( results[folder], "L" ), 
        folderSum( results[folder], "FN" ), 
        folderSum( results[folder], "BR" ) 
        ] for folder in results ]

    text += md.h2( "Overview" )
    text += createCoverageDonut( "lines", lhit, ltot )
    text += createCoverageDonut( "functions", fhit, ftot )
    text += createCoverageDonut( "branches", bhit, btot )
    text += md.table( projectData )

    for folder in results:
        resultFolder = results[folder]
        sourceData = [[ "file", "lines", "functions", "branches" ]]
        for f in resultFolder:
            lhit, ltot, fhit, ftot, bhit, btot = getCoverage( resultFolder[f] )
            sourceData += [[ 
                md.ilink( f, "Coverage of " + f ), 
                            formatPercent( lhit, ltot ),
                            formatPercent( fhit, ftot ),
                            formatPercent( bhit, btot )
                ]]
        text += md.h2( folder )
        text += md.table( sourceData )

        for f in resultFolder:
            createCoverageSourceFile_pureMD( "Coverage of " + f, resultFolder[f] )
            subpages.append( md.slink("Coverage of " + f ))

    md.createPage( title, title, text )
    return subpages, total

def main( coverage ):
    text = ""
    subpages = []
    lhit_global, ltot_global = 0,0

    overallData = [[ "project", "lines", "functions", "branches" ]]
    for project in coverage:
        title = "Test Results - Coverage - " + project 
        subsubpages, subresult = createSubpage( project, title )
        lhit, ltot, fhit, ftot, bhit, btot = getCoverage( subresult )
        lhit_global += lhit
        ltot_global += ltot
        overallData += [[ md.ilink( project, title),
                            formatPercent( lhit, ltot ),
                            formatPercent( fhit, ftot ),
                            formatPercent( bhit, btot )
                            ]]
        subpages += [ md.slink( title ) ]
        subpages += subsubpages

    text += md.h2( "Test Report - Coverage Analysis" )
    text += createCoverageDonut( project + " - lines", lhit_global, ltot_global )
    text += md.table( overallData )
    return text, subpages

