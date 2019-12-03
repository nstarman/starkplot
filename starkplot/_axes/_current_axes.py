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
__all__ = ["gca", "sca"]


##############################################################################
### IMPORTS

## General
# import numpy as np

# matplotlib
from matplotlib import pyplot
from matplotlib.axes._base import _AxesBase


##############################################################################

gca = pyplot.gca  # TODO allow with-enabled axes


def sca(ax=None):
    """set current axes
    None:: current axes
    Axes: set's that
    # int: figure with that number

    TODO support actual options for pyplot.sca
    """

    # make figure current
    if ax is None:
        ax = pyplot.gca()
        return ax

    # elif issubclass(ax.__class__, _AxesBase):
    #     ax = pyplot.sca(ax)
    #     return ax

    # elif isinstance(ax, (int, np.integer)):
    #     fig = pyplot.figure(fig)
    #     return fig

    # else:
    #     raise ValueError

    else:
        return pyplot.sca(ax)


# /def
