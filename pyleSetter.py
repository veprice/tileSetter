######### Functions to make Pages ########

import string
import pandas as pd
import numpy as np


from dataLoader import *
import nameBuilder as nb
import petDB as pdb
import htmile

# Initialize Pages

# Name Search (for new pets)
ns = htmile.tileSetPage('name_search')

# Check pets I've already found
pc = htmile.tileSetPage('pet_check')

# Check names I've already found
ncheck = htmile.tileSetPage('name_check')

# Generate new code for names petpage
#petpage = tst.tileSetPage(petpage_setup)


#pets = pdb.loadDB
