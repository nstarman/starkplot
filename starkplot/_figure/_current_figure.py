#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _current_figure
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**

TODO
- contextmanager which accepts an argument for the documentation
"""

__author__ = "Nathaniel Starkman"
__credits__ = ["matplotlib"]

__all__ = [
    'gcf', 'scf'
]


##############################################################################
### Imports

## General
import numpy as np

# matplotlib
from matplotlib import pyplot
from matplotlib.pyplot import figure, Figure


##############################################################################
# gcf & scf

gcf = pyplot.gcf   # TODO allow with-enabled figures


def scf(fig=None):
    """set current figure
    None:: current figure
    Figure: set's that
    int: figure with that number

    supports with

    TODO support full mpl_decorator options
    """

    # make figure current
    if fig is None:
        fig = pyplot.gcf()
        return fig

    elif isinstance(fig, Figure):
        fig = pyplot.figure(fig.number)
        return fig

    elif isinstance(fig, (int, np.integer)):
        fig = pyplot.figure(fig)
        return fig

    else:
        raise ValueError
# /def
