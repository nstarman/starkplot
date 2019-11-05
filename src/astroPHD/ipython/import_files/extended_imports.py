#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : Extending the Standard Import File
# AUTHOR  : Nathaniel Starkman
# PROJECT :
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""extending the standard import file.

Returns
-------
numpy:
    linalg.norm
scipy:
    stats.binned_statistic->binned_stats

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
### IMPORTS

## General
# numpy
from numpy.linalg import norm
# scipy
from scipy.stats import binned_statistic as binned_stats


##############################################################################
# Printing Information

@_set_docstring_import_file_helper('extend', __doc__)  # doc from __doc__
def extend_imports_help():
    """Help for extended base imports."""
    _import_file_docstring_helper(extend_imports_help.__doc__)  # formatting
# /def


if __config__.getboolean('verbosity', 'verbose-imports'):
    extend_imports_help()

##############################################################################
# END
