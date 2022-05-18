import string
import pandas as pd
import numpy as np
import datetime as dt
from IPython.display import display, HTML

# import tilesetting modules from directorys
# from .defaults import defaults
from .dataLoader import load_segments,update_pres
#from .htmile import *
#from .nameBuilder import *



__version__ = '0.1.0'
__author__ = 'Cady (penguinluver222)'



ws = load_segments()    # load name segment data
ws = update_pres(ws)    # ask to update prefixes
