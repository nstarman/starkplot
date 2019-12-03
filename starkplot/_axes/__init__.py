#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _axes initialization
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""DOCSTRING."""

__author__ = "Nathaniel Starkman"
__credits__ = ["matplotlib"]


##############################################################################
### IMPORTS

## General
from ._current_axes import gca, sca

from ._axes_properties import (
    get_title,
    set_title,
    get_xlabel,
    set_xlabel,
    get_ylabel,
    set_ylabel,
    get_xlim,
    set_xlim,
    get_ylim,
    set_ylim,
    invert_xaxis,
    invert_yaxis,
    get_xscale,
    set_xscale,
    get_yscale,
    set_yscale,
)
