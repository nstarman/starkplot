#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _save
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**

TODO:
- merge savefig and save_figure
"""

__author__ = "Nathaniel Starkman"
__credits__ = ["matplotlib"]

__all__ = ["savefig", "save_figure", "save_and_close"]


##############################################################################
### IMPORTS

## General
from matplotlib import pyplot
from matplotlib.pyplot import figure

## Project-Specific
from ._info import _savefigk
from ._figure_properties import scf

from .decorators import GetFigArg, SetFigArg
from ..decorators import docstring

from .._util import _parsexkwandopts, _parsestrandopts


###############################################################################
### Saving & Closing

# TODO docstring
def savefig(*fnames, fig=None, **kw):
    """save figure

    Parameters
    ----------
    fnames : str(s)
        filename or list of filenames, which is(are) the location(s) to 
        save the figure
    fig: Figure, int, None  (default None)
        figure to save
        passed to *scf*, see documentation
        None -> current figure
    **kw : savefig arguments

    Exceptions
    ----------
    raised by scf for invalid arguments, see documentation
    """
    fig = scf(fig)
    for fname in fnames:
        pyplot.savefig(fname, **kw)


# /def


# -------------------------------------------------------------------------


def save_figure(*fnames, fig=None, **kw):
    r"""save figure

    # TODO explanantion of _parsexkwandopts
    # TODO merge with savefig

    Parameters
    ----------
    fnames: str or file-like object
    fig: Figure, None
        figure to save
        None -> current figure

    Exceptions
    ----------
    raised by scf for invalid arguments, see documentation
    """
    fig = scf(fig)

    for fname in fnames:

        fname, sfgkw = _parsexkwandopts(
            fname, kw, "savefig", _savefigk, _parsestrandopts
        )

        if fname is None:
            fname = "plot" + str(fig.number)

        fig.savefig(fname, **sfgkw)


# /def


# -------------------------------------------------------------------------


@docstring.Appender(
    pyplot.savefig.__doc__, join="\n\n{}\n".format("=" * 78), prededent=True
)
@SetFigArg
def save_and_close(filename, fig=None, **kw):
    """Wrapper for pyplot.savefig
    Calls pyplot.savefig() & pyplot.close()

    Exceptions
    ----------
    raised by scf for invalid arguments, see documentation
    """
    fig = scf(fig)  # set fig to current

    fig.savefig(filename, **kw)
    pyplot.close(fig)


# /def


# -------------------------------------------------------------------------

close = pyplot.close
closefig = pyplot.close


# -------------------------------------------------------------------------
