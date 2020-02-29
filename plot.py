"""
simple wrapper around matplotlib for test result visualization
"""

import matplotlib.pyplot as plt



def donut( 
  title, 
  data, 
  filename=None, 
  colors = [ "limegreen", "tomato", "khaki", "steelblue", "silver" ] 
  ):
    """
    create an donut shape plot based on data and store to file

    parameters:
    -----------
    * title  - str, representing the title of the plot (+ the default filename)
    * data - dict, representing the values to be plotted
    * filename - str, defaults to "{title}.png"
    * colors - an list of color names, defaults to green, red, yellow, blue, grey
    """
    if not filename:
      filename=title+".png"
    fig, axs = plt.subplots( figsize=(4,4), subplot_kw=dict(aspect="equal") )
    keys = []
    values = []
    for k in data:
      keys.append( k )
      values.append( data[k] )
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
    plt.savefig( filename, dpi=300 )
