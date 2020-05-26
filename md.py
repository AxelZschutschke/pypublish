import plot

output_path = "."


def formatFilename( name ):
  """
  replace special characters in filename and make lowercase
  """
  return name.\
          replace( " ", "" ).\
          replace( ".", "_" ).\
          replace( "-", "_" ).\
          replace( "/", "_" ).\
          lower()

def h1( title, link ):
  """
  begin section
  """
  return "# {0} {{#{1}}}\n\n".format( str( title ), formatFilename( link ) )
def h2( title ):
  """
  begin subsection
  """
  return "# {}\n\n".format( str( title ) )
def link( text, ref ):
  """
  create internal link to an given site
  """
  return "[{}]({})".format( str(text), str(ref))
def ilink( text, ref ):
  """
  create internal link to an given site, replacing special characters in ref[erence]
  """
  return "[{}](\\ref {})".format( str(text), formatFilename(ref))
def slink( ref ):
  """
  subpage link to [ref]erence
  """
  return "\subpage {}".format( formatFilename(ref))
def img( filename, alt ):
  """
  place an image
  """
  return "![{}]({})".format( str(alt), str(filename))
def table( data ):
  """
  create a markdown table
  """
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
  """
  create a new file, based on global output path and ref[erence] string and add header
  section with TOC and title of page
  """
  ref = formatFilename( ref )
  with open( output_path + "/" + ref + ".md", "w" ) as f:
    f.write( h1( title, ref ) )
    f.write( "[TOC]\n\n" )
    f.write( text )
 
def red():
  """
  place the image of a green flag
  """
  return "\image html red.png \"\" "
def green():
  """
  place the image of a green flag
  """
  return "\image html green.png \"\" "

def rg( x ):
  """
  place image of red flag if value is zero, green flag otherwise
  (e.g. for expected results - shall be > 0)
  """
  return red() if x == 0 else green()
def gr( x ):
  """
  place image of green flag if value is zero, red flag otherwise
  (e.g. for error counters - shall be == 0)
  """
  return red() if x > 0 else green()
