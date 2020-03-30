# -*- coding: utf-8 -*-

"""initialization file for jupyter notebook functions

# TODO:
- provide functions to set the inline vs notebook,
  change figure_format to something other than retina, etc.

"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

## General
import matplotlib.pyplot as pyplot

try:
    from astropy.visualization import quantity_support, astropy_mpl_style
except ImportError:
    _APY = False
else:
    _APY = True

## Custom

## Project-Specific


##############################################################################
### Running

# configure matplotlib
try:
    get_ipython()

except NameError:
    pass

else:
    get_ipython().magic("matplotlib inline")
    get_ipython().magic("config InlineBackend.figure_format='retina'")


if _APY:
    quantity_support()
    pyplot.style.use(astropy_mpl_style)


##############################################################################
### Printing Output
print(
    """Imported:
Set matplotlib inline
configured figure format to retina
set up astropy quantity support
changed style to astropy style
"""
)
