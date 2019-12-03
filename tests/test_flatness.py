#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_flatness
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

from importlib import import_module


#############################################################################
# mpl_decorator


def _can_import(name):
    import importlib

    try:
        i = import_module(name)
    except ImportError:
        return False
    else:
        print(i)
        return True


# -------------------------------------------------------------------------

# def _import_from_string(*path):
#     import importlib

#     try:
#         i = importlib.import_module('.'.join(path[:-1]), )
#     except ImportError:
#         return False
#     else:
#         print(i)
# return True


# -------------------------------------------------------------------------


def test_import_starkplot():
    r"""
    import starkplot as splt
    """

    assert _can_import("starkplot")

    return None


# /def


# -------------------------------------------------------------------------


def test_import_folders():
    r"""
    import starkplot as splt
    TODO update as add new functions
    """
    # testing folders
    #####################
    assert _can_import("starkplot._axes")

    assert _can_import("starkplot._figure")

    assert _can_import("starkplot._info")

    assert _can_import("starkplot.decorators")

    assert _can_import("starkplot.util")

    # testing equivalence  # TODO programmatic way to do this
    #####################
    from starkplot import decorators

    assert import_module("starkplot.decorators") == decorators

    from starkplot import _info

    assert import_module("starkplot._info") == _info

    return None


# /def


# -------------------------------------------------------------------------


def test_call_starkplot_functions():
    r"""
    must be put after test_import_starkplot
    TODO update as add new functions
    """

    import starkplot as plt

    # folders
    plt.decorators
    plt._info

    return None


# /def


# -------------------------------------------------------------------------
# def test_import_starkplot():
#     r"""
#     import starkplot as splt
#     """

#     import starkplot as plt

#     return None
# # /def


# -------------------------------------------------------------------------
