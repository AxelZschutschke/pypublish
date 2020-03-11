"""
simple wrapper around matplotlib for test result visualization
"""

import matplotlib.pyplot as plt
import md



def donut( 
  title, 
  keys,
  values, 
  filename=None, 
  colors = [ "limegreen", "tomato", "khaki", "steelblue", "silver" ] 
  ):
    """
    create an donut shape plot based on data and store to file

    parameters:
    -----------
    * title  - str, representing the title of the plot (+ the default filename)
    * keys - list, representing the keys / categories to be plotted
    * values - list, representing the values to be plotted
    * filename - str, defaults to "{title}.png"
    * colors - an list of color names, defaults to green, red, yellow, blue, grey
    """
    if not filename:
      filename = md.formatFilename( title ) + ".png"
    fig, axs = plt.subplots( figsize=(4,4), subplot_kw=dict(aspect="equal") )
    wedges,texts = axs.pie( 
      values, 
      wedgeprops=dict(width=0.5), 
      startangle=90, 
      colors=colors[:len(values)] 
      )
    axs.legend( wedges, keys, title=None, loc="lower right" )

    text=str( sum( values ) )
    axs.annotate( text, xy=( -0.04 * len( text ), -0.05 ) )
    axs.set_title( title )
    plt.savefig( md.output_path + "/" + filename, dpi=80 )
    return "![{}]({})".format( title, filename )
