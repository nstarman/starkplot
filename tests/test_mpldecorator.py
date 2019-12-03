#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_mpldecorator
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""

__author__ = "Nathaniel Starkman"


##############################################################################
### IMPORTS

from starkplot import MatplotlibDecorator
from starkplot import mpl_decorator

#############################################################################
# mpl_decorator


def test_making_decorator():
    r"""
    mpl_decorator = MatplotlibDecorator()
    """

    assert (
        mpl_decorator == MatplotlibDecorator()
    ), "mpl_decorator != MatplotlibDecorator()"

    return None


# /def


# -------------------------------------------------------------------------


def test_making_new_decorator_defaults():
    r"""
    """
    dec1 = MatplotlibDecorator(_as_decorator=False)

    # checking it's none, should never be triggered
    assert dec1.fig is None, "decorator has wrong default"

    # making decorator with new default
    dec2 = MatplotlibDecorator(fig="new", _as_decorator=False)
    # checking
    assert dec2.fig == "new", "could not change defaults"

    # checking original decorator default did not change
    assert dec1.fig is None, "decorator default changed"

    return None


# /def


# -------------------------------------------------------------------------


def test_can_wrap_function():  # TODO
    def function(*args, **kwargs):
        return

    newfunc = MatplotlibDecorator(func=function)
    # now what?

    print("not yet implemented")
    return None


# /def
