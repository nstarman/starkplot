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
"""functions for getting/setting the current figure

TODO
- contextmanager which accepts an argument for the documentation
  so can have "with" enabled gcf / scf
"""

__author__ = "Nathaniel Starkman"
__credits__ = ["matplotlib"]

__all__ = ["gcf", "scf"]


##############################################################################
### IMPORTS

## General
import numpy as np

# matplotlib
from matplotlib import pyplot as _pyplot
from matplotlib.pyplot import figure, Figure


##############################################################################
# gcf & scf

gcf = _pyplot.gcf  # TODO allow with-enabled figures


def scf(fig=None):
    """set current figure

    Parameters
    ----------
    fig : Figure, int, None  (defualt None)
        the figure which should be made current

    Returns
    -------
    fig : Figure
        Figure object, which is also set as the current figure

    Exceptions
    ----------
    ValueError : if <fig> is not None, Figure, or int (np.integer)
    ValueError : if int argument is not for an existing Figure
    """

    # make figure current
    if fig is None:
        fig = _pyplot.gcf()
        return fig

    elif isinstance(fig, Figure):
        fig = _pyplot.figure(fig.number)
        return fig

    elif isinstance(fig, (int, np.integer)):
        if not _pyplot.fignum_exists(fig):
            raise ValueError(f"fig #{fig} does not exist")
        fig = _pyplot.figure(fig)
        return fig

    else:
        raise ValueError


# /def
