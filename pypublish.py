import argparse

import md
import traceback

import environment
import unit
import logs 
import cppcheck
import security
import cccc
import valgrind
import wizard
import lcov

parser = argparse.ArgumentParser( 
	description="script for importing different test reports into doxygen" 
	)

parser.add_argument( "--out", type=str, nargs="?", default=".",
	           help="output directory to export reports to" )
parser.add_argument( "--env", type=str, nargs="+", default=[],
	           help="environment report file[s] (json)" )
parser.add_argument( "--unit", type=str, nargs="+", default=[],
		   help="junit xml report file[s] (xml)" )
parser.add_argument( "--log", type=str, nargs="+", default=[],
		   help="log file[s] (txt)" )
parser.add_argument( "--cppcheck", type=str, nargs="+", default=[],
		   help="cppcheck report file[s] (xml)" )
parser.add_argument( "--cccc", type=str, nargs="+", default=[],
		   help="cccc report file[s] (xml)" )
parser.add_argument( "--valgrind", type=str, nargs="+", default=[],
		   help="valgrind report file[s] (txt)" )
parser.add_argument( "--wizard", type=str, nargs="+", default=[],
		   help="wizard report file[s] (txt)" )
parser.add_argument( "--lcov", type=str, nargs="+", default=[],
		   help="lcov report file[s] (txt)" )
parser.add_argument( "--sec", type=str, nargs="+", default=[],
		   help="security report file[s] (txt)" )


args = parser.parse_args()

md.output_path = args.out

text  = ""
subpages = []

def runModule( module, moduleArgs, text, subpages ):
    if moduleArgs:
        try:
          moduleText, moduleSubPages = module.main( moduleArgs )
          text += moduleText
          subpages += moduleSubPages
        except Exception as e:
          text += md.h2( "{} - Exception Occoured".format( module.__name__ ))
          text += traceback.format_exc()
          traceback.print_exc()
    return text, subpages
      
text, subpages = runModule( environment, args.env, text, subpages )
text, subpages = runModule( unit, args.unit, text, subpages )
text, subpages = runModule( logs, args.log, text, subpages )
text, subpages = runModule( cppcheck, args.cppcheck, text, subpages )
text, subpages = runModule( cccc, args.cccc, text, subpages )
text, subpages = runModule( valgrind, args.valgrind, text, subpages )
text, subpages = runModule( wizard, args.wizard, text, subpages )
text, subpages = runModule( lcov, args.lcov, text, subpages )
text, subpages = runModule( security, args.sec, text, subpages )

#### create subpages section (cleaning up TOC)
text += "\n\n"
text += "**See also:**\n\n"
text += md.slink( "testreportsub" )
subpagetext = ""
for subpage in subpages:
  subpagetext += " * {}\n".format( subpage )
md.createPage( "Test Report - Subpages", "testreportsub", subpagetext )

md.createPage( "Test Report", "testreport", text )


