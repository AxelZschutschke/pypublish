import argparse
import environment
import unit
import logs 
import cppcheck

import md

parser = argparse.ArgumentParser( 
	description="script for importing different test reports into doxygen" 
	)

parser.add_argument( "--out", type=str, nargs="?", default=".",
	           help="output directory to export reports to" )
parser.add_argument( "--env", type=str, nargs="+", default=[],
	           help="environment report file[s]" )
parser.add_argument( "--unit", type=str, nargs="+", default=[],
		   help="junit xml report file[s]" )
parser.add_argument( "--log", type=str, nargs="+", default=[],
		   help="log file[s]" )
parser.add_argument( "--cppcheck", type=str, nargs="+", default=[],
		   help="cppcheck report file[s]" )

args = parser.parse_args()

md.output_path = args.out

text  = ""
subpages = []

if args.env:
  envtext, envsubpages = environment.main( args.env )
  text += envtext
  subpages += envsubpages
if args.unit:
  unitText, unitSubpages = unit.main( args.unit )
  text += unitText
  subpages += unitSubpages
if args.log:
  logtext, logsubpages = logs.main( args.log )
  text += logtext
  subpages += logsubpages
if args.cppcheck:
  cppchecktext, cppchecksubpages = cppcheck.main( args.cppcheck )
  text += cppchecktext
  subpages += cppchecksubpages

#### create subpages section (cleaning up TOC)
text += "\n\n"
text += "**See also:**\n\n"
text += md.slink( "testreportsub" )
subpagetext = ""
for subpage in subpages:
  subpagetext += " * {}\n".format( subpage )
md.createPage( "Test Report - Subpages", "testreportsub", subpagetext )

md.createPage( "Test Report", "testreport", text )


