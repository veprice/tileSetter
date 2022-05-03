######### Load tileSetter module ########
# To use, type 'from pyleSetter import *' in a Python session
# Python session/notebook must be in the same directory as the .py scripts.
#######################################

# Import general python modules
import string
import pandas as pd
import numpy as np
import datetime as dt
from IPython.display import display, HTML

# import tilesetting modules from directory
import htmile as ts
import nameBuilder as nb

# create easy-to-call function
def refresh(name_generator):
    ts.tileSet(name_generator.get_names())

def nb_refresh(name_generator):
    tiles = ts.tileSet(name_generator.get_names(show_stats=False),local_page=False)

    with open('./HTML/ipyn_style.css', 'r') as file:
        css = file.read().replace('\n', '')

    html =  '<style>' + css + '</style>'
    html += '<div style="float:left;padding-left:50px;">'
    html += name_generator.stats['name_data'].to_html()
    html += 'Last Updated @'+ name_generator.stats['time']

    html += '</div><div style="float:left;margin-top:0px;padding-left:75px;">'
    html += '<br><b>Generator:</b>'
    html += name_generator.ng.to_html()
    html += '</div>'
    #html += name_generator.stats['name_data'].to_html()
    html += tiles


    return display(HTML(html))

# Import word segments and update prefixes
#nb.w_s = nb.update_pres(nb.w_s)

# Start Default Generator
bb = nb.nameGen('bit:34:,bit:34:')
print(  '\nLoaded name generator \'bb\'.' +
        '\nTo generate more names, type \'refresh(bb)\')' +
        '\nor create new name generator using nb.nameGen().')
