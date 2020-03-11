import argparse
import environment
import unit
import logs

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

args = parser.parse_args()

md.output_path = args.out

text  = ""
if args.env:
  text += environment.main( args.env )
if args.unit:
  text += unit.main( args.unit )
if args.log:
  text += logs.main( args.log )

md.createPage( "Test Report", "testreport", text )
