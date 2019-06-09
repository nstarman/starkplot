#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _axes initialization
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**

TODO
"""

__author__ = "Nathaniel Starkman"
__credits__ = ["matplotlib"]
# __all__ = ['figure', ]


##############################################################################
### IMPORTS

## General
from ._current_axes import gca, sca

# from ._axes import *  # TODO replace

from ._axes_properties import (
    get_title, set_title,
    get_xlabel, set_xlabel,
    get_ylabel, set_ylabel,
    # get_zlabel, set_zlabel,
    # get_label, set_label,
    get_xlim, set_xlim,
    get_ylim, set_ylim,
    # get_zlim, set_zlim,
    invert_xaxis,
    invert_yaxis,
    # invert_zaxis,
    # invert_axis,
    get_xscale, set_xscale,
    get_yscale, set_yscale,
    # get_zscale, set_zscale,
    # get_scale, set_scale
)
