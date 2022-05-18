import string
import pandas as pd
import numpy as np
import datetime as dt
from IPython.display import display, HTML

# import tilesetting modules from directory
from .defaults import *
from .dataLoader import *
#from .htmile import *
#from .nameBuilder import *

__version__ = '0.1.0'
__author__ = 'Cady (penguinluver222)'

# create easy-to-call function
# def refresh(name_generator,notebook=False):
#     if notebook == False:
#         ts.tileSet(name_generator.get_names())
#         return name_generator.show_stats()
#     else:
#         tiles = ts.tileSet(name_generator.get_names(),local_page=False)
#
#         with open('./HTML/ipyn_style.css', 'r') as file:
#             css = file.read().replace('\n', '')
#
#         html =  '<style>' + css + '</style>'
#         html += '<div style="float:left;padding-left:50px;">'
#         html += name_generator.stats['name_data'].to_html()
#         html += 'Last Updated @'+ name_generator.stats['time']
#
#         html += '</div><div style="float:left;margin-top:0px;padding-left:75px;">'
#         html += '<br><b>Generator:</b>'
#         html += name_generator.ng.to_html()
#         html += '</div>'
#         #html += name_generator.stats['name_data'].to_html()
#         html += tiles
#
#     return display(HTML(html))

# Import word segments and update prefixes



w_s = load_segments()
#nb.w_s = nb.update_pres(nb.w_s)

# Load Data
