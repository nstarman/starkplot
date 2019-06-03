#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _axes
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
TODO oldax and return to current ax
"""

__author__ = "Nathaniel Starkman"
__credits__ = ["matplotlib"]
# __all__ = ['figure', ]


##############################################################################
### Imports

# matplotlib
from matplotlib.pyplot import figure
from matplotlib import pyplot  # for usage here

# import decorator

# from .decorators import mpl_decorator, docstring
# from .decorators.docstring import wrap_func_keep_orig_sign

# # custom imports

# from ._util import _parseoptsdict, _parsestrandopts, _parselatexstrandopts,\
#     _stripprefix, _latexstr,\
#     axisLabels, axisScales
# from ._info import _pltypes, _annotations, _customadded, _other

# try:
#     from astropy.utils.decorators import wraps  # TODO move to internal file
# except Exception as e:
#     print('cannot import preferred wrapper')
#     from functools import wraps


#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = ["Jo Bovy", "The Matplotlib Team"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"


# __all__ = [
#   'axes',
# ]


###############################################################################

def _gca(ax=None):
    return ax if ax is not None else pyplot.gca()
# /def


###############################################################################
# Axes

# @decorator.contextmanager
# def protem_axes(*args, **kw):
#     """`with` enabled figure
#     when used in `with` statement:
#         stores current figure & creates a pro-tem figure
#         executes with statment
#         restores old figure
#     """
#     # BEFORE
#     # store old axes
#     oldax = pyplot.gca()
#     # make new axes
#     pyplot.axes(*args, **kw)

#     yield  # DURING

#     # AFTER
#     # restore old figure
#     pyplot.sca(oldax)
# # /def

# NEW DEFAULT PYPLOT FIGURE
# imported into _plot to overwrite
# axes = wrap_func_keep_orig_sign(
#     protem_axes, pyplot.axes,
#     doc_post='\n\nThis function has been modified to be `with` enabled')

axes = pyplot.axes

# @mpl_decorator
# def axes(*args, **kw):  # TODO improve,
#     return axes(*args, **kw)


###############################################################################
# title

# TODO with decorator
def get_title(ax=None):
    ax = _gca(ax=ax)
    return ax.get_title()
# /def


# TODO with decorator
# TODO with _parsexkwandopts
def set_title(label, fontdict=None, loc='center', pad=None, ax=None, **kwargs):
    ax = _gca(ax=ax)
    ax.set_title(label, fontdict=fontdict, loc=loc, pad=pad, **kwargs)
# /def


###############################################################################
# xlabel

def get_xlabel(ax=None):
    ax = _gca(ax=ax)
    return ax.get_xlabel()
# /def


###############################################################################
# ylabel

def get_ylabel(ax=None):
    ax = _gca(ax=ax)
    return ax.get_ylabel()
# /def


###############################################################################
# zlabel

def get_zlabel(ax=None):
    ax = _gca(ax=ax)
    return ax.get_zlabel()
# /def


###############################################################################
# axes labels

def get_axes_labels(ax=None):
    return [get_xlabel(ax=ax), get_ylabel(ax=ax), get_zlabel(ax=ax)]
# /def


###############################################################################
# xlim

def get_xlim(ax=None):
    ax = _gca(ax=ax)
    return ax.get_xlim()
# /def


###############################################################################
# ylim

def get_ylim(ax=None):
    ax = _gca(ax=ax)
    return ax.get_ylim()
# /def


###############################################################################
# zlim

def get_zlim(ax=None):
    ax = _gca(ax=ax)
    return ax.get_zlim()
# /def


###############################################################################
# axes limits

def get_axes_lims(ax=None):
    ax = _gca(ax=ax)
    return ax.get_xlim()
# /def


###############################################################################
# invert_xaxis

###############################################################################
# invert_yaxis

###############################################################################
# invert_zaxis

###############################################################################
# invert_axis

###############################################################################
# invert axes

###############################################################################
# xscale

###############################################################################
# yscale

###############################################################################
# zscale

###############################################################################
# axes scales

###############################################################################
# xlabel

###############################################################################
# ylabel

###############################################################################
# zlabel