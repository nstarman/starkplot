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
### IMPORTS

## General
# matplotlib
from matplotlib import pyplot  # for usage here

## Project-Specific
from ._current_axes import gca, sca
from .decorators import GetAxArg, SetAxArg


#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__credits__ = ["matplotlib"]


# __all__ = [
#   'axes',
# ]


###############################################################################
# Axes

# axes = pyplot.Axes


###############################################################################
# title

get_title = GetAxArg(pyplot.Axes.get_title)


set_title = SetAxArg(pyplot.Axes.set_title)


###############################################################################
# labels

get_xlabel = GetAxArg(pyplot.Axes.get_xlabel)


set_xlabel = SetAxArg(pyplot.Axes.set_xlabel)


get_ylabel = GetAxArg(pyplot.Axes.get_ylabel)


set_ylabel = SetAxArg(pyplot.Axes.set_ylabel)


# get_zlabel = GetAxArg(pyplot.Axes.get_zlabel)


# set_zlabel = SetAxArg(pyplot.Axes.set_zlabel)


# def get_labels(ax=None):

#     oldax = pyplot.gca()  # saving old figure
#     ax = gca(ax=ax)     # get figure from fig argument

#     xlabel = get_xlabel(ax=ax)
#     ylabel = get_ylabel(ax=ax)

#     try:
#         zlabel = get_zlabel(ax=ax)
#     except Exception as e:
#         print(e)
#         has_zlabel = False
#     else:
#         has_zlabel = True

#     sca(ax=oldax)        # make old fig current

#     if has_zlabel:
#         return xlabel, ylabel, zlabel
#     else:
#         return xlabel, ylabel
# # /def


# def set_labels(*args, ax=None, **kwargs):
#     set_xlabel(*args, ax=ax, **kwargs)
#     set_ylabel(*args, ax=ax, **kwargs)

#     try:
#         set_zlabel(*args, ax=ax, **kwargs)
#     except Exception as e:
#         print(e)
#         pass

#     return
# # /def


###############################################################################
# limits

get_xlim = GetAxArg(pyplot.Axes.get_xlim)


set_xlim = SetAxArg(pyplot.Axes.set_xlim)


get_ylim = GetAxArg(pyplot.Axes.get_ylim)


set_ylim = SetAxArg(pyplot.Axes.set_ylim)


# get_zlim = GetAxArg(pyplot.Axes.get_zlim)


# set_zlim = SetAxArg(pyplot.Axes.set_zlim)


# def get_lims(ax=None):

#     oldax = pyplot.gca()  # saving old figure
#     ax = gca(ax=ax)     # get figure from fig argument

#     xlim = get_xlim(ax=ax)
#     ylim = get_ylim(ax=ax)

#     try:
#         zlim = get_zlim(ax=ax)
#     except Exception as e:
#         print(e)
#         has_zlim = False
#     else:
#         has_zlim = True

#     sca(ax=oldax)        # make old fig current

#     if has_zlim:
#         return xlim, ylim, zlim
#     else:
#         return xlim, ylim
# # /def


# def set_lims(*args, ax=None, **kwargs):
#     set_xlim(*args, ax=ax, **kwargs)
#     set_ylim(*args, ax=ax, **kwargs)

#     try:
#         set_zlim(*args, ax=ax, **kwargs)
#     except Exception as e:
#         print(e)
#         pass

#     return
# # /def


###############################################################################
# invert_axis

invert_xaxis = SetAxArg(pyplot.Axes.invert_xaxis)


invert_yaxis = SetAxArg(pyplot.Axes.invert_yaxis)


# invert_zaxis = SetAxArg(pyplot.Axes.invert_zaxis)


# def invert_axis():
#     pass
# # /def


###############################################################################
# scale

get_xscale = GetAxArg(pyplot.Axes.get_xscale)


set_xscale = SetAxArg(pyplot.Axes.set_xscale)


get_yscale = GetAxArg(pyplot.Axes.get_yscale)


set_yscale = SetAxArg(pyplot.Axes.set_yscale)


# get_zscale = GetAxArg(pyplot.Axes.get_zscale)


# set_zscale = SetAxArg(pyplot.Axes.set_zscale)


# def get_scale():
#     pass
# # /def


# def set_scale():
#     pass
# # /def
