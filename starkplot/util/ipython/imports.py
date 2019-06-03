#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Standard Import File
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""standard import file.
imports:

GENERAL
-------
os, sys  # operating system
time
pdb
warnings

ASTROPY
-------
.visualization.quantity_support, astropy_mpl_style
** does:
quantity_support()
plt.style -> astropy_mpl_style

PLOTTING
--------
starkplot -> plt
.mpl_decorator

matplotlib -> mpl
.colors
.cm

Logging
-------
logging
.util.logging.LogFile, LoggerFile

Misc
-------
.util.ObjDict

IPYTHON
-------
display, Latex, Markdown, set_trace,
printmd, printltx

**also does:
%matplotlib inline
%config InlineBackend.figure_format = 'retina'
InteractiveShell.ast_node_interactivity = "all"
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### Imports

## General
import os, sys                        # operating system
import time                           # timing
import pdb                            # debugging
import warnings                       # warning
# warnings.filterwarnings('ignore', RuntimeWarning)

# Allowing Astropy quantities in matplotlib
from astropy.visualization import quantity_support, astropy_mpl_style

## Plotting
# starkplot
import starkplot as plt
from starkplot import mpl_decorator

# matplotlib
import matplotlib as mpl
from matplotlib import colors
from matplotlib import cm

## Logging
from src.util.logging import (
    logging,                          # standard logging
    LogFile,                          # custom minimal logging
    LoggerFile                        # custom extended logger
)

## Custom Functions
from src.util import ObjDict

# +--------------------------------------------------------------------------+
# IPython Magic

# %run runs in the main namespace, so need to run as 'src.', not '.''
from src.util.ipython import (
    display, Latex, Markdown,
    set_trace,
    printmd, printltx
)
# this also does: %matplotlib inline,
#                 %config InlineBackend.figure_format = 'retina'
#                 InteractiveShell.ast_node_interactivity = "all"

##############################################################################
### Running Imported Functions

# astropy changes
quantity_support()
plt.style.use(astropy_mpl_style)

##############################################################################
### Priting Information

print("""Imported:
Base: os, sys, time, pdb, warnings,
Plot: starkplot->plt, .mpl_decorator
      matplotlib->mpl, .colors, .cm
Logging: logging, .LogFile, .LoggerFile
Misc: ObjDict
IPython: display, Latex, Markdown, set_trace, printmd, printltx
""")
