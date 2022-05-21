"""
A Python library for tilesetting Neopets.

"""


from .nameBuilder import nameGen
from .htmile import tileSet

__version__ = '0.1.0'
__author__ = 'Cady (penguinluver222)'

def refresh(name_generator):
    """Refreshes pet tiles with new names.

        Args:
            name_generator: a nameGen() object created with a specific string

        Returns:
            Writes updated HTML file using defined generator, and prints statistics about the names to the terminal.

        Examples:
            >>> refresh(bb)
            ------------------- HTML Updated! ---
            Saved to: ./HTML/tileSet.html
            ...
                         # of names
            6 Letters           100
            7 Letters           100
            8 Letters           100
            Total Names         300
            -----------------------
            Last Update @ 03:01:39 PM'
    """
    tileSet(name_generator.get_names())
    return name_generator.show_stats()

bb = nameGen('bit:34:,bit:34:')

print(' -------------- pylesetter loaded! ----------------- ')
