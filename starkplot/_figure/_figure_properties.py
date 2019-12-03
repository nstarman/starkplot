#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _figure
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

# __all__ = ['figure', ]


##############################################################################
### IMPORTS

## General

# matplotlib
from matplotlib import pyplot
from matplotlib.pyplot import figure, Figure

## Project-Specific
from ._info import _newfigk, _tightlayoutk, _suptitlek
from ._current_figure import gcf, scf
from .decorators import GetFigArg, SetFigArg

from ..decorators import docstring
from ..decorators.docstring import wrap_func_keep_orig_sign

from .._util import _parsexkwandopts, _parsestrandopts


###############################################################################
# figure

figure = pyplot.figure  # TODO allow with-enabled figures


###############################################################################
# Figsize

get_figsize = GetFigArg(pyplot.Figure.get_size_inches)


set_figsize = SetFigArg(pyplot.Figure.set_size_inches)


###############################################################################
# Suptitle


def get_suptitle(fig=None, text=True):
    """Get a figure's title.

    Parameters
    ----------
    fig : Figure, None  (default None)
        figure to set supertitle
        None -> current figure
    text : bool, optional
        whether to return the whole figure instance
        or just the text

    Returns
    -------
    text : str
        the figure supertitle text
    TODO should this return the whole figure instance?
    """
    fig = scf(fig)

    if text:
        return fig._suptitle._text
    else:
        return fig._suptitle


# /def


get_supertitle = get_suptitle  # alias for get_suptitle


def set_suptitle(t, fig=None, **kw):
    """Add a title to the figure.

    Parameters
    ----------
    t : str
        The title text.
    fig : Figure, None  (default None)
        figure to set supertitle
        None -> current figure
    # TODO explanantion of _parsexkwandopts
    # TODO use SetFigArg
    """
    fig = scf(fig)

    t, stkw = _parsexkwandopts(t, kw, "suptitle", _suptitlek, _parsestrandopts)

    res = fig.suptitle(t, **stkw)
    return res


# /def


set_supertitle = set_suptitle  # alias for set_suptitle
suptitle = set_suptitle  # alias for set_suptitle
supertitle = set_supertitle  # alias for set_suptitle


###############################################################################
# DPI

get_dpi = GetFigArg(pyplot.Figure.get_dpi)


set_dpi = SetFigArg(pyplot.Figure.set_dpi)


###############################################################################
# Facecolor

get_facecolor = GetFigArg(pyplot.Figure.get_facecolor)


set_facecolor = SetFigArg(pyplot.Figure.set_facecolor)


###############################################################################
# Edgecolor

get_edgecolor = GetFigArg(pyplot.Figure.get_edgecolor)


set_edgecolor = SetFigArg(pyplot.Figure.set_edgecolor)


###############################################################################
# Frameon

get_frameon = GetFigArg(pyplot.Figure.get_frameon)


set_frameon = SetFigArg(pyplot.Figure.set_frameon)


###############################################################################
# Override Figure


def override_figure(fig=None, **kw):
    r"""override figure properties
    Parameters
    ---------
    figsize:
        uses set_size_inches
    dpi:
        uses set_dpi
    facecolor:
        uses set_facecolor
    edgecolor:
        uses edgecolor
    frameon:
        uses frameon
    """
    fig = scf(fig)

    if kw.get("figsize", None) is not None:
        fig.set_size_inches(kw.get("figsize"), forward=True)

    if "dpi" in kw:  # TODO better methods
        fig.set_dpi(kw.get("dpi"))
    elif "fig_dpi" in kw:
        fig.set_dpi(kw.get("fig_dpi"))

    if "facecolor" in kw:  # TODO better methods
        fig.set_facecolor(kw.get("facecolor"))
    elif "fig_facecolor" in kw:
        fig.set_facecolor(kw.get("fig_facecolor"))

    if "edgecolor" in kw:  # TODO better methods
        fig.set_edgecolor(kw.get("edgecolor"))
    elif "fig_edgecolor" in kw:
        fig.set_edgecolor(kw.get("fig_edgecolor"))

    if "frameon" in kw:  # TODO better methods
        fig.set_frameon(kw.get("frameon"))
    elif "fig_frameon" in kw:
        fig.set_frameon(kw.get("fig_frameon"))

    # FigureClass
    # clear
    # subplotpars
    # tight_layout
    # constrained_layout


# /def


###############################################################################
# tight_layout

tight_layout = SetFigArg(pyplot.Figure.tight_layout)


# TODO
# def tightLayout(fig=None, tlkw={}, **kw):
#     r"""
#     """
#     fig = _gcf(fig)

#     _, tlkw = _parsexkwandopts(tlkw, kw, 'tight_layout', _tightlayoutk,
#                                _parseoptsdict)

#     fig.tight_layout(**tlkw)
# # /def


###############################################################################
# protem decorator

# class protem_decorator():
#     r"""
#     TODO docstring pass-through
#     """
#     def __new__(cls, func=None, *args, **kwargs):
#         self = super().__new__(cls)
#         if func is None:
#             return self
#         else:
#             # self.__doc__ = func.__doc__
#             return self(func)

#     @decorator.contextmanager
#     def __call__(self, func, *args, **kwargs):
#         # BEFORE
#         # store old fig
#         oldfig = pyplot.gcf().number

#         yield func(*args, **kwargs)  # DURING

#         # AFTER
#         # restore old figure
#         pyplot.figure(oldfig)
#     # /def

# @protem_decorator
# def protem_figure(*args, **kw):
#     """`with` enabled figure
#     when used in `with` statement:
#         stores current figure & creates a pro-tem figure
#         executes with statment
#         restores old figure
#     """
#     return pyplot.figure(*args, **kw)
# # /def
