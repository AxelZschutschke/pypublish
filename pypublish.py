import argparse
import environment

from md import *

parser = argparse.ArgumentParser( 
	description="script for importing different test reports into doxygen" 
	)

parser.add_argument( "--env", type=str, nargs="+", default=[],
	           help="environment report file[s]" )
parser.add_argument( "--unit", type=str, nargs="+", default=[],
		   help="junit xml report file[s]" )

args = parser.parse_args()

text  = ""
text += environment.main( args.env )

createPage( "Test Report", "testreport", text )
