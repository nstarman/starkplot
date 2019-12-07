#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : functions for shaped subplots grids
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""functions for shaped subplots grids
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### IMPORTS

## General
import numpy as np

from matplotlib import pyplot

## Project-Specific
from ...decorators import mpl_decorator


##############################################################################


def closest_square_axis_grid_shape(numax, prefer_cols=True):
    """shape of the closest-to-square grid given the number of desired axes

    Parameters
    ----------
    numax : int
        number of axes
    prefer_cols : bool, optional
        if an (n-1) x n grid better fits the number of axes, whether to return
        an (n-1, n) grid (prefer_cols = True)
        or an (n, n-1) (prefer_cols = False)

    Returns
    -------
    shape : list
        (nrows, ncols)
    """
    # finding the side of the closest square grid which can hold all the axes
    side = int(np.ceil(np.sqrt(numax)))

    # the difference between this nearest square grid and the number of axes
    # this is needed for finding 'nearby' rectangles that are closer to the
    # desired number of axes
    diff = side ** 2 - numax

    # determining if the square grid is the best fit
    # comparing s^2 to (s-1) x s = s^2 - ss
    # if s^2 - n < s than s^2 - s will not hold all the axes
    # if s^2 - n >= s than s^2 - s will hold the axes better than s^2
    if diff < side:  # s^2 - n < s
        shape = [side, side]

    else:  # s^2 - n >= s
        if prefer_cols:
            shape = [side - 1, side]
        else:
            shape = [side, side - 1]

    return shape


# /def


# --------------------------------------------------------------------------


def closest_square_axis_grid(numax, prefer_cols=True, flatten=False, **kw):
    """the closest-to-square grid given the number of desired axes

    Parameters
    ----------
    numax : int
        number of axes
    prefer_cols : bool, optional
        if an (n-1) x n grid better fits the number of axes, whether to return
        an (n-1, n) grid (prefer_cols = True)
        or an (n, n-1) (prefer_cols = False)
    flatten : bool, optional
        whether to flatten the axes array for easier iteration

    Returns
    -------
    fig : Figure
    axs : array of Axes
        if flatten: flattened array
        else: (nrows, ncols) array of Axes

    TODO
    ----
    support mpl_decorator on the subplots
    """
    nrows, ncols = closest_square_axis_grid_shape(
        numax, prefer_cols=prefer_cols
    )

    fig, axs = pyplot.subplots(nrows=nrows, ncols=ncols, **kw)

    if flatten:
        axs = axs.reshape(-1)

    return fig, axs


# /def


# --------------------------------------------------------------------------


def closest_square_axis_grid_iter(numax, prefer_cols=True):
    """the closest-to-square grid given the number of desired axes
    axes list is flattened for easy looping

    Parameters
    ----------
    numax : int
        number of axes
    prefer_cols : bool, optional
        if an (n-1) x n grid better fits the number of axes, whether to return
        an (n-1, n) grid (prefer_cols = True)
        or an (n, n-1) (prefer_cols = False)

    Returns
    -------
    fig : Figure
    axs : flat array of Axes
    """
    return closest_square_axis_grid(
        numax, prefer_cols=prefer_cols, flatten=True
    )


# /def

##############################################################################
# End
