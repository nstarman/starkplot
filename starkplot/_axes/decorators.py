#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : AddFigArg
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""TODO
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
from ._current_axes import gca, sca


###############################################################################


class GetAxArg:
    r"""
    Make a function from a Figure method which accepts a figure as a kwarg

    ex:
        pyplot.Figure.set_size_inches(self, ...)
        becomes
        myfunc(..., fig=None)

    fig kwarg options:
    None: uses current figure
    Figure: uses figure instance
    int: uses figure with that number

    TODO test it as a decorator
    TODO use decorator.FunctionMaker.create to perserve docstring & signature
    """

    def __new__(cls, func=None, **kw):
        # make self from super
        self = super().__new__(cls)

        # -------- docs --------

        # Control the __doc__ options
        # default to wrapped functions documentation, if available
        _doc_default = func.__doc__ if func is not None else None
        doc = kw.get("_doc", _doc_default)

        # if _doc is
        if callable(doc):
            self._doc = doc.__doc__
        else:
            self._doc = doc

        # -------- decorator return --------

        # the function
        if func is None:
            return self
        else:
            return self(func)

    # /def

    def __call__(self, wrapped_func):
        def wrapped(ax=None):

            oldax = pyplot.gca()  # saving old figure
            ax = gca(ax=ax)  # get figure from fig argument

            return_ = wrapped_func(ax)

            sca(ax=oldax)  # make old fig current

            return return_

        # /def

        # assign documentation
        wrapped.__doc__ = wrapped_func.__doc__

        return wrapped

    # /def


# /class


###############################################################################


class SetAxArg:
    r"""
    Make a function from a Figure method which accepts a figure as a kwarg

    ex:
        pyplot.Figure.set_size_inches(self, ...)
        becomes
        myfunc(..., fig=None)

    fig kwarg options:
    None: uses current figure
    Figure: uses figure instance
    int: uses figure with that number

    TODO test it as a decorator
    TODO use decorator.FunctionMaker.create to perserve docstring & signature
    """

    def __new__(cls, func=None, **kw):
        # make self from super
        self = super().__new__(cls)

        # -------- docs --------

        # Control the __doc__ options
        # default to wrapped functions documentation, if available
        _doc_default = func.__doc__ if func is not None else None
        doc = kw.get("_doc", _doc_default)

        # if _doc is
        if callable(doc):
            self._doc = doc.__doc__
        else:
            self._doc = doc

        # -------- decorator return --------

        # the function
        if func is None:
            return self
        else:
            return self(func)

    # /def

    def __call__(self, wrapped_func):
        def wrapped(*args, ax=None, **kwargs):

            oldax = pyplot.gca()  # saving old figure
            ax = sca(ax=ax)  # get right figure

            # apply function with correct figure
            return_ = wrapped_func(pyplot.gca(), *args, **kwargs)

            sca(ax=oldax)  # make old fig current

            return return_

        # /def

        # assign documentation
        wrapped.__doc__ = wrapped_func.__doc__

        return wrapped

    # /def


# /class
