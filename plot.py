"""
simple wrapper around matplotlib for test result visualization
"""

import matplotlib as mpl
mpl.use( "Agg" )
import matplotlib.pyplot as plt
import md

def donut( 
  title, 
  keys,
  values, 
  filename=None, 
  colors = [ "limegreen", "tomato", "khaki", "steelblue", "silver", "mediumpurple",
  "peru", "pink" ] 
  ):
    """
    create an donut shape plot based on data and store to file

    parameters:
    -----------
    * title  - str, representing the title of the plot (+ the default filename)
    * keys - list, representing the keys / categories to be plotted
    * values - list, representing the values to be plotted (same order as keys)
    * filename - str, defaults to "{title}.png"
    * colors - an list of color names, defaults to green, red, yellow, blue, grey, ...
    """
    if not filename:
      filename = md.formatFilename( title ) + ".png"

    # make the file a little wider (6x4) to create some space for the key/legend
    fig, axs = plt.subplots( figsize=(6,4), subplot_kw=dict(aspect="equal") )

    # plot as punched-out pie plot (donut shape)
    wedges,texts = axs.pie( 
      values, 
      wedgeprops=dict(width=0.5), 
      startangle=90, 
      colors=colors[:len(values)] 
      )

    # create key (outside right), bbox for placement outside of pie plot (otherwise it would hide the plot)
    axs.legend( wedges, keys, title=None, loc="upper right", bbox_to_anchor=(1.3,1) )

    # numer (total) in center of plot
    text=str( sum( values ) )
    axs.annotate( text, xy=( -0.04 * len( text ), -0.05 ) )

    # avoid title, doxygen adds a caption automatically
    ##axs.set_title( title )

    # save figure and close it (avoid memory leak)
    plt.savefig( md.output_path + "/" + filename, dpi=80 )
    plt.close()

    # return markdown-formatted link
    return "![{}]({})".format( title, filename ) + "\n\n"
