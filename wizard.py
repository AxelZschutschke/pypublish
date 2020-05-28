import re
import plot
import md
import json

def parseFeatures( f ):
    results = [] # [ { name, success, fail, tests : { testname: testtext, ... } }, ... ]
    featureName = ""
    featureDict = None
    in_test = False
    test_out = ""
    total = 0
    failed = 0
    for l in f:
        l = l.lstrip()
        begin = re.match( ".* \| \[    \] +begin.*", l )
        if begin:
            in_test = True
            test_out = ""
        if in_test:
            test_out += l

        end = re.match( ".* \| \[(.*)\] +test [0-9]*: (.*) (?:successfull|failed)", l )
        feature = re.match( ".* \| \[    \] +feature(.*)", l )
        if end:
            in_test = False
            state = end.group(1)
            test_name = end.group(2)

            failed = failed + 1 if state == "FAIL" else failed
            total += 1
            featureDict["tests"][test_name] = test_out
        elif feature:
            if featureDict:
                # we have been in feature section, close it!
                featureDict["success"] = total - failed
                featureDict["fail"] = failed
                results.append( featureDict )
            failed = 0
            total = 0
            featureName = feature.group(1).lstrip().replace(" ", "_")
            featureDict = { "name" : featureName, "tests": {} }
    return results
            
def createWizardDonut( title, success, fail ):
    header = ["success", "failed"]
    return plot.donut( title, header, [success, fail] ) + "\n\n"

def createSubpage( f ):
    text = md.h2( "Overview" )
    text += createWizardDonut( f["name"]+ " - Overview", f["success"], f["fail"])
    for testName in f["tests"]:
        text += md.h2( "Test Result - " + testName)
        text += "\n"
        text += "~~~~~{.txt}\n"
        text += f["tests"][testName]
        text += "~~~~~\n\n"
    md.createPage( f["title"], f["title"], text )

def main( wizardFiles ):
    title = "Test Report - Wizard"
    overviewData = [["flag", "feature", "success", "failures"]]
    subpages = []
    success = 0
    fail = 0
    for filename in wizardFiles:
        with open( filename, "r" ) as f:
            featureStates = parseFeatures( f ) # [ { name, success, fail, tests : { testname: testtext, ... } }, ... ]
            for f in featureStates:
                f["title"] = "{} - {}".format( title, f["name"] )
                createSubpage( f )
                success += f["success"]
                fail += f["fail"]
                overviewData += [[md.gr(f["fail"]), md.ilink(f["name"],f["title"]), f["success"], f["fail"]]]
                subpages += [ md.slink( f["title"] ) ]

    text = md.h2( title )
    text += createWizardDonut( title + " - Overview", success, fail )
    text += md.table( overviewData )
    return text, subpages
