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
"""**DOCSTRING**

TODO
- Change GetFigArg and AddFigArg to be contextmanagers
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
from ._current_figure import gcf, scf


###############################################################################


class GetFigArg:
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
        def wrapped(fig=None):

            oldfig = pyplot.gcf()  # saving old figure
            fig = scf(fig=fig)  # get figure from fig argument

            return_ = wrapped_func(fig)

            scf(fig=oldfig)  # make old fig current

            return return_

        # /def

        # assign documentation
        wrapped.__doc__ = wrapped_func.__doc__

        return wrapped

    # /def


# /class


###############################################################################


class SetFigArg:
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
        def wrapped(*args, fig=None, **kwargs):

            oldfig = pyplot.gcf()  # saving old figure
            fig = scf(fig)  # get right figure

            # apply function with correct figure
            return_ = wrapped_func(fig, *args, **kwargs)

            scf(fig=oldfig)  # make old fig current

            return return_

        # /def

        # assign documentation
        wrapped.__doc__ = wrapped_func.__doc__

        return wrapped

    # /def


# /class
