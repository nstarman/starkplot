#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _info
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""

__author__ = "Nathaniel Starkman"
__credits__ = ["matplotlib"]


###############################################################################
### Key-Word Arguments for Functions

# figure arguments
_newfigk = (
    "num",
    # 'figsize'  # already a kwarg
    "dpi",  # dots-per-inch resolution
    "facecolor",  # facecolor
    "edgecolor",  # edgecolor
    "frameon",  # TODO
    "FigureClass",  # TODO
    "clear",  # TODO
    # from kwargs: (extra .Figure options)
    "sublotpars",  # TODO
    # 'tight_layout'  # already a kwarg, used later
    "constrained_layout",  # TODO
    "linewidth",  # TODO
)

# tight_layout arguments
_tightlayoutk = (
    "pad",  # padding
    "h_pad",  # height padding
    "w_pad",  # width padding
    "rect",  # figure size in canvas
)

# savefig arguments
_savefigk = (
    "dpi",  # dots-per-inch resolution
    "quality",  # quality 1-95
    "optimize",  # JPEG optimize
    "progressive",  # JPEG encode
    "facecolor",  # facecolor
    "edgecolor",  # edgecolor
    "orientation",  # orientation
    "papertype",  # postscript paper size
    "format",  # file format
    "transparent",  # axes transparency
    "bbox_inches",  # bbox in inches
    "pad_inches",  # padding for tight bbox
    "bbox_extra_artists",  # other artists considered
    "frameon",  # TODO
    "metadata",  # metadata
)

# suptitle arguments
_suptitlek = (
    "x",  # x location
    "y",  # y location
    "horizontalalignment",  # horizontal alignment
    "ha",  # horizontal alignment
    "verticalalignment",  # vertical alignment
    "va",  # vertical alignment
    "fontsize",  # font size
    "size",  # font size
    "fontweight",  # font weight
    "weight"  # font weight
    # 'fontproperties'  # include?
    # kwargs
)
