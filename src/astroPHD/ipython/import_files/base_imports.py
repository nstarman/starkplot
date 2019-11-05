# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : base_imports
# AUTHOR  : Nathaniel Starkman
# PROJECT : astroPHD
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Base set of imports.

Returns
-------
 Base: os, sys, time, pdb, warnings,
      numpy -> np, scipy,
      tqdm -> TQDM, .tqdm, .tqdm_notebook ->. tqdmn
Logging: .LogFile
Misc: ObjDict
IPython: display, Latex, Markdown, set_trace,
         printmd, printMD, printltx, printLaTeX,
         set_autoreload, aimport,
         run_imports, import_from_file,
         add_raw_code_toggle

References
----------
SciPy references are [1]_ and [2]_
NumPy references are [3]_ and [4]_
IPython reference is [5]_
Matplotlib reference is [6]_

.. [1] Travis E. Oliphant. Python for Scientific Computing, Computing in
    Science & Engineering, 9, 10-20 (2007), DOI:10.1109/MCSE.2007.58
    http://scitation.aip.org/content/aip/journal/cise/9/3/10.1109/MCSE.2007.58
.. [2] K. Jarrod Millman and Michael Aivazis. Python for Scientists and
    Engineers, Computing in Science & Engineering, 13, 9-12 (2011),
    DOI:10.1109/MCSE.2011.36
    http://scitation.aip.org/content/aip/journal/cise/13/2/10.1109/MCSE.2011.36
.. [3] Travis E, Oliphant. A guide to NumPy, USA: Trelgol Publishing, (2006).
.. [4] Stéfan van der Walt, S. Chris Colbert and Gaël Varoquaux.
    The NumPy Array: A Structure for Efficient Numerical Computation,
    Computing in Science & Engineering, 13, 22-30 (2011),
    DOI:10.1109/MCSE.2011.37
    http://scitation.aip.org/content/aip/journal/cise/13/2/10.1109/MCSE.2011.37
.. [5] Fernando Pérez, Brian E. Granger, IPython: A System for Interactive
    Scientific Computing, Computing in Science and Engineering, vol. 9,
    no. 3, pp. 21-29, May/June 2007, doi:10.1109/MCSE.2007.53.
    URL: https://ipython.org
.. [6] John D. Hunter. Matplotlib: A 2D Graphics Environment, Computing in
    Science & Engineering, 9, 90-95 (2007), DOI:10.1109/MCSE.2007.55
    http://scitation.aip.org/content/aip/journal/cise/9/3/10.1109/MCSE.2007.55


"""

__author__ = "Nathaniel Starkman"


##############################################################################
# HELPER FUNCTIONS

from astroPHD.util.config import __config__
from astroPHD.util.decorators.docstring import (
    _set_docstring_import_file_helper,
    _import_file_docstring_helper
)



##############################################################################
# IMPORTS

# +---------------------------------------------------------------------------+
# Basic

import os
import sys  # operating system
import time  # timing
import pdb  # debugging
import warnings  # warning

# Numpy
import numpy as np  # numerical python
import scipy  # scientific python

# TODO implement when no TqdmExperimentalWarning
# from tqdm.autonotebook import tqdm
import tqdm as TQDM
from tqdm import tqdm as tqdm, tqdm_notebook as tqdmn

# Custom
from astroPHD.util import ObjDict          # custom dictionary-like object
from astroPHD.util.logging import LogFile  # LoggerFile  # custom logging


# +--------------------------------------------------------------------------+
# IPython Magic

from IPython.core.interactiveshell import InteractiveShell
from IPython.core.debugger import set_trace
from IPython.display import (
    display,               # display is a better print
    Latex, Markdown       # for printing LaTeX or Markdown strings
)

# %run runs in the main namespace, so need to run as 'src.', not '.''
from astroPHD.ipython import (
    printmd, printMD,               # markdown printing
    printltx, printLaTeX,           # LaTeX printing
    set_autoreload, aimport,        # imports
    run_imports, import_from_file,  # imports
    add_raw_code_toggle,            # notebook
)


##############################################################################
# Running Imported Functions

InteractiveShell.ast_node_interactivity = "all"


##############################################################################
# Printing Information

@_set_docstring_import_file_helper('base', __doc__)  # doc from __doc__
def base_imports_help():
    """Help for Matplotlib base imports."""
    _import_file_docstring_helper(base_imports_help.__doc__)  # formatting
# /def


if __config__.getboolean('verbosity', 'verbose-imports'):
    base_imports_help()

##############################################################################
# END
