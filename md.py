import plot

output_path = "."


def formatFilename( name ):
  return name.\
          replace( " ", "" ).\
          replace( ".", "_" ).\
          replace( "-", "_" ).\
          replace( "/", "_" ).\
          lower()

def h1( title, link ):
  return "# {0} {{#{1}}}\n\n".format( str( title ), formatFilename( link ) )
def h2( title ):
  return "# {}\n\n".format( str( title ) )
def link( text, ref ):
  return "[{}]({})".format( str(text), str(ref))
def ilink( text, ref ):
  return "[{}]({})".format( str(text), formatFilename(ref))
def slink( ref ):
  return "\subpage {}".format( formatFilename(ref))
def img( filename, alt ):
  return "![{}]({})".format( str(alt), str(filename))
def table( data ):
  seps = " | ".join( [ "---" for x in data[0] ] )
  data[0] = " | ".join( [ str(x) for x in data[0] ] )
  data[1:] = [ " | ".join( [ str(x) for x in y ] ) for y in data[1:] ]
  result  = "\n\n"
  result += data[0]
  result += "\n"
  result += seps
  result += "\n"
  result += "\n".join( data[1:] )
  result += "\n\n"
  return result
def createPage( title, ref, text ):
  ref = formatFilename( ref )
  with open( output_path + "/" + ref + ".md", "w" ) as f:
    f.write( h1( title, ref ) )
    f.write( "[TOC]\n\n" )
    f.write( text )
 
def red():
  return "\image html red.png \"\" "
def green():
  return "\image html green.png \"\" "
def rg( x ):
  return red() if x == 0 else green()
def gr( x ):
  return red() if x > 0 else green()
