######### Functions to make Pages ########
import string
import pandas as pd
import numpy as np
import datetime as dt


#from dataLoader import *
import nameBuilder as nb
#import petDB as pdb
import htmile as ts

def refresh(name_generator):
    ts.tileSet(name_generator.get_names())

# Import word segments and update prefixes
nb.w_s = nb.update_pres(nb.w_s)
#w_s = nb.update_pres(w_s)
# Start Default Generator
bb = nb.nameGen('bit:35:,bit:23:')
print(  '\nLoaded name generator \'bb\'.' +
        'Open /HTML/tileSetter.html in your favorite browser to see the tiles!'+
        '\nTo generate more names, type \'refresh(bb)\')')#+
        # '\nor create new name generator using nb.nameGen().')
# Initialize Pages
# Name Search (for new pets)
# ns = htmile.tileSetPage('name_search')

# Check pets I've already found
# pc = htmile.tileSetPage('pet_check')

# Check names I've already found
# ncheck = htmile.tileSetPage('name_check')

# Generate new code for names petpage
#petpage = tst.tileSetPage(petpage_setup)


#pets = pdb.loadDB
