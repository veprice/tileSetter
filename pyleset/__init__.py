# import tilesetting modules from directorys
# from .defaults import defaults


from .nameBuilder import nameGen
from .htmile import tileSet

__version__ = '0.1.0'
__author__ = 'Cady (penguinluver222)'

def refresh(name_generator):
    tileSet(name_generator.get_names())
    return name_generator.show_stats()

bb = nameGen('bit:34:,bit:34:')

print(' -------------- pylesetter loaded! ----------------- ')
