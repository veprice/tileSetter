######### Load tileSetter module ########
# To use, type 'from pyleSetter import *' in a Python session
# Python session/notebook must be in the same directory as the .py scripts.
#######################################

# Import general python modules
import string
import pandas as pd
import numpy as np
import datetime as dt

# import tilesetting modules from directory
import htmile as ts
import nameBuilder as nb

# create easy-to-call function
def refresh(name_generator):
    ts.tileSet(name_generator.get_names())

# Import word segments and update prefixes
nb.w_s = nb.update_pres(nb.w_s)

# Start Default Generator
bb = nb.nameGen('bit:34:,bit:34:')
print(  '\nLoaded name generator \'bb\'.' +
        'Open /HTML/tileSetter.html in your favorite browser to see the tiles!' +
        '\nTo generate more names, type \'refresh(bb)\')' +
        '\nor create new name generator using nb.nameGen().')

# Export prefix CSV's
