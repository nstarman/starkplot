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
### Imports

## General
import numpy as np
from matplotlib import pyplot

## Project-Specific
# import starkplot as plt
from starkplot._figure._figure_properties import (
    figure,
    get_figsize, set_figsize,

    suptitle, supertitle,
    get_suptitle, set_suptitle,
    get_supertitle, set_supertitle,

    get_dpi, set_dpi,
    get_facecolor, set_facecolor,
    get_edgecolor, set_edgecolor,
    get_frameon, set_frameon,

    override_figure,
    tight_layout,
)


#############################################################################
# figure

def test_figure():

    # -----------------
    # Making Figure
    fig1 = figure()
    assert fig1.number == 1               # checking figure 1

    # -----------------
    # Making Figure
    fig2 = figure()
    assert fig2.number == 2               # checking figure 2

    # -----------------
    # Other tests
    # TODO

    pyplot.close('all')
    return
# /def


#############################################################################
# Figsize

def test_get_figsize():

    # ----------------
    # Making 2 figures
    fig1 = pyplot.figure()
    fig1.set_size_inches(15, 3)

    fig2 = pyplot.figure()
    figsize2 = fig2.get_size_inches()

    # ----------------
    # get figure size
    figsize1 = get_figsize(fig1)

    # ----------------
    assert (figsize1 == np.array([15., 3.])).all()
    assert (figsize2 == fig2.get_size_inches()).all()

    # ----------------
    pyplot.close('all')
    return
# /def


def test_set_figsize():
    # TODO test set by number and set by None

    # ----------------
    # Making 2 figures
    fig1 = pyplot.figure()

    fig2 = pyplot.figure()
    figsize = fig2.get_size_inches()

    # ----------------
    # set figure size
    set_figsize(15, 3, fig=fig1)

    # ----------------
    assert (fig1.get_size_inches() == np.array([15., 3.])).all()
    assert (fig2.get_size_inches() == figsize).all()

    # ----------------
    pyplot.close('all')
    return
# /def


#############################################################################
# Suptitle

def test_set_suptitle():

    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    assert fig1.number == 1              # checking figure 1
    assert pyplot.gcf().number == 1      # gcf

    fig2 = pyplot.figure()
    assert fig2.number == 2              # checking figure 2
    assert pyplot.gcf().number == 2      # gcf

    # -----------------
    # Setting Suptitle
    set_suptitle('figure 1 suptitle', fig=fig1)
    set_suptitle('figure 2 suptitle', fig=fig2)

    # -----------------
    # Testing
    assert fig2._suptitle._text == 'figure 2 suptitle'
    assert fig1._suptitle._text == 'figure 1 suptitle'

    # ---------------------------
    # _parsexkwandopts options
    # TODO

    pyplot.close('all')
    return
# /def


def test_set_supertitle():
    # TODO actual test
    pass
# /def


def test_suptitle():
    # TODO actual test
    pass
# /def


def test_supertitle():
    # TODO actual test
    pass
# /def


def test_get_suptitle():
    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    pyplot.suptitle('figure 1 suptitle')

    fig2 = pyplot.figure()
    pyplot.suptitle('figure 2 suptitle')

    # -----------------
    # Getting Suptitle
    assert get_suptitle() == 'figure 2 suptitle'          # current
    assert get_suptitle(fig=fig1) == 'figure 1 suptitle'  # fig 1
    assert get_suptitle(fig=1) == 'figure 1 suptitle'     # fig 1
    assert get_suptitle(fig=fig2) == 'figure 2 suptitle'  # fig 2
    assert get_suptitle(fig=2) == 'figure 2 suptitle'     # fig 2

    pyplot.close('all')
    return
# /def


def test_get_supertitle():
    # TODO actual test
    pass
# /def


#############################################################################
# DPI

def test_get_dpi():
    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    fig1.set_dpi(30)

    fig2 = pyplot.figure()
    fig2.set_dpi(40)

    # -----------------
    # Test DPI
    # fig1
    assert fig1.get_dpi() == 30
    assert get_dpi(fig=fig1) == 30      # by figure
    assert get_dpi(fig=1) == 30         # by number
    # fig2
    assert fig2.get_dpi() == 40
    assert get_dpi(fig=None) == 40      # current figure
    assert get_dpi(fig=fig2) == 40      # by figure
    assert get_dpi(fig=2) == 40         # by number

    pyplot.close('all')
    return
# /def


def test_set_dpi():
    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    fig1.set_dpi(72)

    fig2 = pyplot.figure()
    fig2.set_dpi(72)

    # setting
    set_dpi(30, fig=fig1)
    set_dpi(40, fig=fig2)

    # -----------------
    # Test DPI
    assert fig1.get_dpi() == 30
    assert fig2.get_dpi() == 40

    pyplot.close('all')
    return
# /def


###############################################################################
# Facecolor

def test_get_facecolor():

    black = (0.0, 0.0, 0.0, 1.0)

    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    fig1.set_facecolor(black)

    fig2 = pyplot.figure()
    fig2.set_facecolor(black)

    # -----------------
    # Test Facecolor
    assert fig2.get_facecolor() == black         # fig2 facecolor
    assert get_facecolor() == black          # current facecolor
    # fig1
    assert get_facecolor(fig=fig1) == black  # fig1 facecolor
    assert get_facecolor(fig=1) == black     # fig1 facecolor
    # fig2
    assert get_facecolor(fig=fig2) == black  # fig2 facecolor
    assert get_facecolor(fig=2) == black     # fig2 facecolor

    pyplot.close('all')
    return
# /def


def test_set_facecolor():

    black = (0.0, 0.0, 0.0, 1.0)
    white = (1.0, 1.0, 1.0, 1.0)

    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    fig1.set_facecolor('grey')

    fig2 = pyplot.figure()
    fig2.set_facecolor('grey')

    # -----------------
    # Test DPI
    set_facecolor('black', fig=fig1)       # figure 1 by figure
    assert fig1.get_facecolor() == black

    set_facecolor('white', fig=1)          # figure 1 by number
    assert fig1.get_facecolor() == white

    set_facecolor('black', fig=None)       # current figure
    assert fig2.get_facecolor() == black

    set_facecolor('black', fig=fig2)       # figure 2 by figure
    assert fig2.get_facecolor() == black

    set_facecolor('white', fig=2)          # figure 2 by number
    assert fig2.get_facecolor() == white

    pyplot.close('all')
    return
# /def


###############################################################################
# Edgecolor


def test_get_edgecolor():

    black = (0.0, 0.0, 0.0, 1.0)

    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    fig1.set_edgecolor(black)

    fig2 = pyplot.figure()
    fig2.set_edgecolor(black)

    # -----------------
    # Test edgecolor
    assert fig2.get_edgecolor() == black         # fig2 edgecolor
    assert get_edgecolor() == black          # current edgecolor
    # fig1
    assert get_edgecolor(fig=fig1) == black  # fig1 edgecolor
    assert get_edgecolor(fig=1) == black     # fig1 edgecolor
    # fig2
    assert get_edgecolor(fig=fig2) == black  # fig2 edgecolor
    assert get_edgecolor(fig=2) == black     # fig2 edgecolor

    pyplot.close('all')
    return
# /def


def test_set_edgecolor():

    black = (0.0, 0.0, 0.0, 1.0)
    white = (1.0, 1.0, 1.0, 1.0)

    # -----------------
    # Making 2 Figures
    fig1 = pyplot.figure()
    fig1.set_edgecolor('grey')

    fig2 = pyplot.figure()
    fig2.set_edgecolor('grey')

    # -----------------
    # Test DPI
    set_edgecolor('black', fig=fig1)       # figure 1 by figure
    assert fig1.get_edgecolor() == black

    set_edgecolor('white', fig=1)          # figure 1 by number
    assert fig1.get_edgecolor() == white

    set_edgecolor('black', fig=None)       # current figure
    assert fig2.get_edgecolor() == black

    set_edgecolor('black', fig=fig2)       # figure 2 by figure
    assert fig2.get_edgecolor() == black

    set_edgecolor('white', fig=2)          # figure 2 by number
    assert fig2.get_edgecolor() == white

    pyplot.close('all')
    return
# /def


###############################################################################
# Frameon

def test_get_frameon():
    pass  # TODO
# /def


def test_set_frameon():
    pass  # TODO
# /def


###############################################################################
# Override Figure

def test_override_figure():
    pass  # TODO
# /def


###############################################################################
# tight_layout

def test_tight_layout():
    pass  # TODO
# /def


###############################################################################
### DONE
