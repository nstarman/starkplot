#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : subplots initialization file
# AUTHOR  : Nathaniel Starkman
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""initialization file for subplots
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### IMPORTS

## Project-Specific
from .square import (
    closest_square_axis_grid_shape,  # shape of the closest-to-square grid
    closest_square_axis_grid,  # closest-to-square grid of axes
    closest_square_axis_grid_iter,  # flattened closest-to-square grid of axes
)

from .corner import corner_plot, staircase_plot

##############################################################################
# End
