#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_figure
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

## General
from matplotlib import pyplot

## Project-Specific
from starkplot._figure._current_figure import gcf, scf


#############################################################################
# figure


def test_gcf():

    # -----------------
    # Making Figure
    fig1 = pyplot.figure()
    assert fig1.number == 1  # checking figure 1
    assert gcf().number == 1  # check gcf

    # -----------------
    # Making Figure
    fig2 = pyplot.figure()
    assert fig2.number == 2  # checking figure 2
    assert gcf().number == 2  # check gcf

    pyplot.close("all")
    return


# /def


#############################################################################
# scf


def test_scf_None():

    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    assert fig1.number == 1  # checking figure 1
    assert gcf().number == 1  # gcf

    fig2 = pyplot.figure()
    assert fig2.number == 2  # checking figure 2
    assert gcf().number == 2  # gcf

    # -----------------
    # Testing SCF
    scf(None)  # scf should keep the figure as 2
    assert gcf().number == 2  # checking didn't change

    pyplot.close("all")
    return


# /def


# -------------------------------------------------------------------------


def test_scf_fig():

    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    assert fig1.number == 1  # checking figure 1
    assert gcf().number == 1  # gcf

    fig2 = pyplot.figure()
    assert fig2.number == 2  # checking figure 2
    assert gcf().number == 2  # gcf

    # -----------------
    # Testing SCF
    scf(fig1)  # change the current figure to 1
    assert gcf().number == 1  # checking changed

    pyplot.close("all")
    return


# /def


# -------------------------------------------------------------------------


def test_scf_number():

    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    assert fig1.number == 1  # checking figure 1

    fig2 = pyplot.figure()
    assert fig2.number == 2  # checking figure 2
    assert gcf().number == 2  # gcf

    # -----------------
    # Testing SCF
    scf(1)  # change the current figure to 1
    assert gcf().number == 1  # checking changed

    pyplot.close("all")
    return


# /def
