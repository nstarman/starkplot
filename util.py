#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Docstring
"""

#############################################################################
# Imports

from matplotlib import pyplot
from matplotlib.figure import Figure

from matplotlib import pyplot as plt

from . import docstring

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


#############################################################################
# NoneType

NoneType = type(None)


#############################################################################
# Wrapper

class ObjectWrapper(object):
    def __init__(self, obj, **kwargs):
        # r"""
        # TODO: does this assign **kwargs into the object or keep them separate?
        #       does setattr() set into the obj or this wrapper?
        # """

        if obj is None:
            obj = NoneType
        self.__class__ = type(obj.__class__.__name__,
                              (self.__class__, obj.__class__),
                              {})
        self.__dict__ = obj.__dict__

        for key, val in kwargs.items():
            setattr(self, key, val)

    # def overriddenMethod(self):
    #     pass


class Wrapper(object):
    """Wrapper class that provides proxy access to an instance of some
       internal instance."""

    __wraps__ = None
    __ignore__ = "class mro new init setattr getattr getattribute"

    def __init__(self, obj, **kwargs):
        if self.__wraps__ is None:
            raise TypeError("base class Wrapper may not be instantiated")
        elif isinstance(obj, self.__wraps__):
            self._obj = obj
        else:
            raise ValueError("wrapped object must be of %s" % self.__wraps__)

        for key, val in kwargs.items():
            setattr(self, key, val)

    # provide proxy access to regular attributes of wrapped object
    def __getattr__(self, name):
        return getattr(self._obj, name)

    # create proxies for wrapped object's double-underscore attributes
    class __metaclass__(type):
        def __init__(cls, name, bases, dct):

            def make_proxy(name):
                def proxy(self, *args):
                    return getattr(self._obj, name)
                return proxy

            type.__init__(cls, name, bases, dct)
            if cls.__wraps__:
                ignore = set("__%s__" % n for n in cls.__ignore__.split())
                for name in dir(cls.__wraps__):
                    if name.startswith("__"):
                        if name not in ignore and name not in dct:
                            setattr(cls, name, property(make_proxy(name)))


class FigureWrapper(Wrapper):
    __wraps__ = Figure


# class ObjectWrapper(object):
#     """docstring for ObjectWrapper"""
#     def __new__(cls, obj, **kwargs):

#         class objectWrapper(Wrapper):
#             __wraps__ = type(obj)

#         return objectWrapper(obj, **kwargs)


#############################################################################
# Allowable Key Words

_newfigk = (
    'num',
    # 'figsize'  # already a kwarg
    'dpi',
    'facecolor' 'edgecolor'
    'frameon' 'FigureClass', 'clear',
    # from kwargs: (extra .Figure options)
    'sublotpars'
    # 'tight_layout'  # already a kwarg, used later
    'constrained_layout',
    'linewidth',
)
# # keys & default values for a new figure
# self._newfigkdf = (
#     ('num', None),
#     # ('figsize', None),
#     ('dpi', None),
#     ('facecolor', None), ('edgecolor', None),
#     ('frameon', None), ('FigureClass', Figure), ('clear', False),
#     # from kwargs
#     ('sublotpars', None),
#     # ('tight_layout', None),
#     ('constrained_layout', None)
# )

_tightlayoutk = (
    'pad', 'h_pad', 'w_pad', 'rect'
)

_savefigk = (
    'dpi',
    'quality',
    'facecolor', 'edgecolor',
    'orientation', 'portrait', 'papertype',
    'format', 'transparent',
    'bbox_inches', 'pad_inches', 'frameon',
    'metadata'
)
# self._savefigkdf = (
#     ('dpi', None),
#     ('quality', None),
#     ('facecolor', None), ('edgecolor', None),
#     ('orientation', 'portrait'), ('papertype', None),
#     ('format', None), ('transparent', False),
#     ('bbox_inches', None), ('pad_inches', None), ('frameon', None),
#     ('metadata', None)
# )

_suptitlek = (
    # x, y
    # horizontalalignment, ha, verticalalignment, va
    'fontsize', 'fontweight',
    # size, weight
    # fontproperties  # include?
    # kwargs
)
# self._suptitlekdf = (
#     # ('suptitle_x', .5), ('suptitle_y', .98),
#     # ('suptitle_ha', 'center'), ('suptitle_va', 'top'),
#     ('fontsize', None), ('fontweight', None),
#     # ('fontproperties', None),  # include?
# )

_titlek = (
    # fontdict, loc, pad,
    'fontsize', 'fontweight',
    # size, weight
    # fontproperties  # include?
    # kwargs
)

_xlabelk = ('labelpad', 'fontsize', 'fontweight',)
_ylabelk = ('labelpad', 'fontsize', 'fontweight',)
_zlabelk = ('labelpad', 'fontsize', 'fontweight',)

_xlabelkdf = (
    ('xlabel_labelpad', None),
    ('fontsize', None), ('fontweight', None))
_ylabelkdf = (
    ('xlabel_labelpad', None),
    ('fontsize', None), ('fontweight', None))
_zlabelkdf = (
    ('xlabel_labelpad', None),
    ('fontsize', None), ('fontweight', None))

# Colorbar
_cbark = (
    # axes properties
    'orientation', 'fraction', 'pad', 'shrink', 'aspect',
    'anchor', 'panchor',
    # colorbar properties
    'extend', 'extendfrac', 'extendrect', 'spacing', 'ticks', 'format', 'drawedges', 'boundaries', 'values',
    )


#############################################################################
# Helper Functions

def _stripprefix(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix):]
    else:
        return s


def _parseoptsdict(attr):
    attr = attr if isinstance(attr, dict) else {}
    return attr


def _latexstr(attr):
    if not attr:  # empty string
        return rf'{attr}'
    # elif not attr.startswith('$'):
    #     return rf'${attr}$'
    else:
        return rf'{attr}'


def _parselatexstrandopts(attr):
    r"""for parsing input when function signature is func(str, **kw)
    """
    # more from _parsestrandopts
    if isinstance(attr, str):
        return _latexstr(attr), {}
    else:
        return _latexstr(attr[0]), attr[1]


def _parsestrandopts(attr):
    r"""
    """
    if attr is True:
        return None, {}
    if attr is False:
        return '', {}
    elif isinstance(attr, NoneType):
        return '', {}
    elif isinstance(attr, str):
        return attr, {}
    else:
        return attr[0], attr[1]


###############################################################################
# Figure

def _gcf(fig):
    return fig if fig is not None else plt.gcf()
# /def


def prepareFigure(fig=None, rtcf=True, figsize=None, **kw):
    r"""
    """
    fig = _gcf(fig)
    # Figure
    # Checking on the state of the figure
    # gets / makes figure and determines whether to return the old figure.
    oldfig = None  # default oldfig to None. Does not return to old fig.

    # fig is Figure instance
    if isinstance(fig, Figure):
        if rtcf in (True, None):  # preserve oldfig
            oldfig = plt.gcf()
        plt.figure(fig.number)  # makes figure current

    # get current figure
    elif fig is None:
        fig = plt.gcf()

    # make new figure
    elif fig == 'new':
        if rtcf is True:  # preserve oldfig
            oldfig = plt.gcf()
        # figure kwargs if included
        nfkw = kw.get('fig', {})
        if not nfkw:
            nfkw = {k: kw.get(k) for k in _newfigk if k in kw}
            nfkw.update({_stripprefix(k, 'fig_'): v
                         for k, v in kw.items() if k.startswith('fig_')})
        # making the figure
        fig = plt.figure(figsize=figsize, **nfkw)

    # not yet covered
    else:
        raise ValueError("fig is not Figure, None, or 'new'")

    return fig, oldfig
# /def


def overrideFigure(fig=None, **kw):
    r"""
    """
    fig = _gcf(fig)

    if kw.get('figsize', None) is not None:
        fig.set_size_inches(kw.get('figsize'), forward=True)

    fig.set_dpi(kw.get(_stripprefix('dpi', 'fig_'), fig.get_dpi()))
    fig.set_facecolor(kw.get(_stripprefix('facecolor', 'fig_'), fig.get_facecolor()))
    fig.set_edgecolor(kw.get(_stripprefix('edgecolor', 'fig_'), fig.get_edgecolor()))
    fig.set_frameon(kw.get(_stripprefix('frameon', 'fig_'), fig.get_frameon()))
    # FigureClass
    # clear
    # subplotpars
    # tight_layout
    # constrained_layout
# /def


def setSuptitle(suptitle, fig=None, **kw):
    r"""
    """
    fig = _gcf(fig)

    suptitle, stkw = _parsestrandopts(suptitle)  # get val & kw
    if not stkw:  # if no kwargs, try from kw
        stkw = kw.get('suptitle', {})
        if not stkw:  # still no kwargs, scrape together from kw
            # allowable arguments
            stkw = {k: kw.get(k) for k in _suptitlek if k in kw}
            # any specific overrides
            stkw.update({_stripprefix(k, 'suptitle_'): v
                         for k, v in kw.items()
                         if k.startswith('suptitle_')})
    fig.suptitle(suptitle, **stkw)


def tightLayout(fig=None, tlkw={}, **kw):
    r"""
    """
    fig = _gcf(fig)

    tlkw = _parseoptsdict(tlkw)
    if not tlkw:  # if empty
        tlkw = kw.get('tight_layout', {})
        if not tlkw:  # if empty
            # allowable arguments
            tlkw = {k: kw.get(k) for k in _tightlayoutk if k in kw}
            # any specific overrides
            tlkw.update({_stripprefix(k, 'tight_layout_'): v
                         for k, v in kw.items()
                         if k.startswith('tight_layout_')})

    fig.tight_layout(**tlkw)


def saveFigure(fname, fig=None, **kw):
    r"""
    """
    fig = _gcf(fig)

    fname, sfgkw = _parsestrandopts(fname)  # get val & kw
    if not sfgkw:  # if no kwargs
        sfgkw = kw.get('savefig', {})
        if not sfgkw:  # still no kwargs
            # allowable arguments
            sfgkw = {k: kw.get(k) for k in _savefigk if k in kw}
            # any specific overrides
            sfgkw.update({_stripprefix(k, 'savefig_'): v
                          for k, v in kw.items()
                          if k.startswith('savefig_')})

    if fname is None:
        fname = 'plot' + str(fig.number)

    fig.savefig(fname, **sfgkw)


###############################################################################
# Axes

def _gca(ax):
    return ax if ax is not None else plt.gca()
# /def


def prepareAxes(ax=None, fig=None):
    r"""
    """
    fig = _gcf(fig)

    # Axes
    # Explaining axes options
    # ax = False means all axes stuff must be done in wrapped_function
    # ax = None uses current axes
    # ax = int geta/sets subplot with this number
    # ex = next # TODO
    # #TODO should ax=False impact how the figure is treated?

    if ax is False:  # this turns off most stuff
        pass
    elif ax is None:  # get current axes
        ax = fig.gca()
    elif isinstance(ax, int):  # make / get subplot @ int
        fig.add_subplot(ax)  # also gets old axes if exists
        # TODO have to check if axes exists see docstring above
    elif ax == 'next':
        raise ValueError("`next' not yet supported")
    elif isinstance(ax, str):
        raise ValueError("not supported")
    else:  # TODO check it's an axes instance
        ax = fig.sca(ax)

    return ax
# /def


def setTitle(title, ax=None, **kw):
    ax = _gca(ax)
    title, titlekw = _parsestrandopts(title)
    if not titlekw:  # if no kwargs
        titlekw = kw.get('title', {})
        if not titlekw:  # still no kwargs
            titlekw = {k: kw.get(k) for k in _titlek if k in kw}
            titlekw.update({_stripprefix(k, 'title_'): v
                            for k, v in kw.items()
                            if k.startswith('title_')})
    ax.set_title(title, **titlekw)
# /def


###############################################################################
# Axis Labels

@docstring.Appender(pyplot.Axes.set_xlabel.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
def set_xlabel(ax=None, x=None, units=True, **kw):
    r"""starkplot wrapper for set_xlabel

    Arguments
    ---------
    ax: axis, None
    x:
    units: bool
    xkw:
    """

    if x is None:
        return

    ax = ax if ax is not None else pyplot.gca()

    x, nkw = _parselatexstrandopts(x)
    if not kw:  # if no kwargs
        nkw = kw.get('xlabel', {})
        if not kw:
            nkw = {k: kw.get(k) for k in _xlabelk if k in kw}
            nkw.update({_stripprefix(k, 'xlabel_'): v
                        for k, v in kw.items()
                        if k.startswith('xlabel_')})
    if units is True:
        x = rf"{x} [{ax.get_xlabel()}]"
    ax.set_xlabel(x, **nkw)


@docstring.Appender(pyplot.Axes.set_ylabel.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
def set_ylabel(ax=None, y=None, units=True, **kw):
    r"""starkplot wrapper for set_ylabel

    Arguments
    ---------
    ax: axis, None
    y:
    units: bool
    xkw:
    """

    if y is None:
        return

    ax = ax if ax is not None else pyplot.gca()

    y, nkw = _parselatexstrandopts(y)
    if not kw:  # if no kwargs
        nkw = kw.get('ylabel', {})
        if not kw:
            nkw = {k: kw.get(k) for k in _ylabelk if k in kw}
            nkw.update({_stripprefix(k, 'ylabel_'): v
                        for k, v in kw.items()
                        if k.startswith('ylabel_')})
    if units is True:
        y = rf"{y} [{ax.get_ylabel()}]"
    ax.set_ylabel(y, **nkw)


# @docstring.Appender(pyplot.Axes.set_zlabel.__doc__,
#                     join='\n\n{}\n'.format('=' * 78), prededent=True)
def set_zlabel(ax=None, z=None, units=True, **kw):
    r"""starkplot wrapper for set_zlabel

    Arguments
    ---------
    ax: axis, None
    z:
    units: bool
    **kw:
    """
    if z is None:
        return

    ax = ax if ax is not None else pyplot.gca()

    try:
        ax.get_zlabel()
    except AttributeError:
        pass
    else:
        z, nkw = _parselatexstrandopts(z)
        if not kw:  # if no kwargs
            nkw = kw.get('zlabel', {})
            if not kw:
                nkw = {k: kw.get(k) for k in _zlabelk if k in kw}
                nkw.update({_stripprefix(k, 'zlabel_'): v
                            for k, v in kw.items()
                            if k.startswith('zlabel_')})
        if units is True:
            rf"{z} [{ax.get_zlabel()}]"
        ax.set_zlabel(z, **nkw)


@docstring.Appender(pyplot.Axes.set_xlabel.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
@docstring.Appender(pyplot.Axes.set_ylabel.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
# @docstring.Appender(pyplot.Axes.set_xlabel.__doc__,
#                     join='\n\n{}\n'.format('=' * 78), prededent=True)
def axisLabels(ax=None, x=None, y=None, z=None, units=True, **kw):
    """Add axis labels to given axis
    starkplot wrapper for set_x/y/zlabel

    Call signature::

      add_axis_labels(ax=None, x=None, y=None, z=None, units=False)

    Arguments
    ---------
    ax: axes or None
        axes instance or None, which will then call pyplot.gca()
        to get the current axes
    x/y/z: str or 2-item tuple
        the x/y/z axis label
        str: axis label
        2-item tuple: (str label, dict of label kwargs)
    units: bool
        whether plotting astropy quantities with units & quantity_support
        designed for:
        >> from astropy.visualization import quantity_support; quantity_support()
        >> from astropy.visualization import astropy_mpl_style; plt.style.use(astropy_mpl_style)

    History
    -------
    2018-10-30 - written - Starkman (Toronto)
    2019-02-09 - modified - Starkman (Toronto) ref bovy_plot._add_axislabels
    """
    ax = ax if ax is not None else pyplot.gca()

    set_xlabel(ax=ax, x=x, units=units, **kw)
    set_ylabel(ax=ax, y=y, units=units, **kw)
    set_zlabel(ax=ax, z=z, units=units, **kw)


###############################################################################
# Axis Limits

@docstring.Appender(pyplot.Axes.set_xlim.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
def set_xlim(ax=None, x=None):
    r"""starkplot wrapper for set_xlim
    """
    if x is None:
        return

    ax = ax if ax is not None else pyplot.gca()
    return ax.set_xlim(*x)
# /def


@docstring.Appender(pyplot.Axes.set_ylim.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
def set_ylim(ax=None, y=None):
    r"""starkplot wrapper for set_ylim
    """
    if y is None:
        return

    ax = ax if ax is not None else pyplot.gca()
    return ax.set_ylim(*y)
# /def


# @docstring.Appender(pyplot.Axes.set_zlim.__doc__,
#                     join='\n\n{}\n'.format('=' * 78), prededent=True)
def set_zlim(ax=None, z=None):
    r"""starkplot wrapper for set_zlim
    """
    if z is None:
        return

    ax = ax if ax is not None else pyplot.gca()
    try:
        return ax.set_zlim(*z)
    except AttributeError:
        pass
# /def


@docstring.Appender(pyplot.Axes.set_xlim.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
@docstring.Appender(pyplot.Axes.set_ylim.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
# @docstring.Appender(pyplot.Axes.set_zlim.__doc__,
#                     join='\n\n{}\n'.format('=' * 78), prededent=True)
def axisLimits(ax=None, x=None, y=None, z=None):
    r"""starkplot wrapper for set_x/y/zlim
    """
    ax = ax if ax is not None else pyplot.gca()
    set_xlim(ax=ax, x=x)
    set_ylim(ax=ax, y=y)
    set_zlim(ax=ax, z=z)


###############################################################################
# Axis Inversion

@docstring.Appender(pyplot.Axes.invert_xaxis.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
def invert_xaxis(ax=None):
    r"""starkplot wrapper for invert_xaxis
    """
    ax = ax if ax is not None else pyplot.gca()
    ax.invert_xaxis()


@docstring.Appender(pyplot.Axes.invert_yaxis.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
def invert_yaxis(ax=None):
    r"""starkplot wrapper for invert_yaxis
    """
    ax = ax if ax is not None else pyplot.gca()
    ax.invert_yaxis()


# @docstring.Appender(pyplot.Axes.invert_zaxis.__doc__,
#                     join='\n\n{}\n'.format('=' * 78), prededent=True)
def invert_zaxis(ax=None):
    r"""starkplot wrapper for invert_zaxis
    """
    ax = ax if ax is not None else pyplot.gca()
    try:
        ax.invert_zaxis()
    except AttributeError:
        pass


@docstring.Appender(pyplot.Axes.invert_xaxis.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
@docstring.Appender(pyplot.Axes.invert_yaxis.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
# @docstring.Appender(pyplot.Axes.invert_zaxis.__doc__,
#                     join='\n\n{}\n'.format('=' * 78), prededent=True)
def invertAxis(ax=None, x=False, y=False, z=False):
    r"""starkplot wrapper for invert_x/y/zaxis
    """
    ax = ax if ax is not None else pyplot.gca()
    if x:
        invert_xaxis(ax=ax)
    if y:
        invert_yaxis(ax=ax)
    if z:
        invert_zaxis(ax=ax)


###############################################################################
# Axis Scales

@docstring.Appender(pyplot.Axes.set_xscale.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
def set_xscale(ax=None, x=None, **kw):
    r"""starkplot wrapper for set_xscale
    """
    if x is None:
        return

    ax = ax if ax is not None else pyplot.gca()
    x, nkw = _parsestrandopts(x)
    if not nkw:  # if no kwargs
        nkw = kw.get('xscale', {})
    ax.set_xscale(x, **nkw)


@docstring.Appender(pyplot.Axes.set_yscale.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
def set_yscale(ax=None, y=None, **kw):
    r"""starkplot wrapper for set_yscale
    """
    if y is None:
        return

    ax = ax if ax is not None else pyplot.gca()
    y, nkw = _parsestrandopts(y)
    if not nkw:  # if no kwargs
        nkw = kw.get('yscale', {})
    ax.set_yscale(y, **nkw)


# @docstring.Appender(pyplot.Axes.set_zscale.__doc__,
#                     join='\n\n{}\n'.format('=' * 78), prededent=True)
def set_zscale(ax=None, z=None, **kw):
    r"""starkplot wrapper for set_zscale
    """
    if z is None:
        return

    ax = ax if ax is not None else pyplot.gca()
    try:
        ax.get_zscale()
    except AttributeError:
        pass
    else:
        z, nkw = _parsestrandopts(z)
        if not nkw:  # if no kwargs
            nkw = kw.get('zscale', {})
        ax.set_zscale(z, **nkw)


@docstring.Appender(pyplot.Axes.set_xscale.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
@docstring.Appender(pyplot.Axes.set_yscale.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
# @docstring.Appender(pyplot.Axes.set_zscale.__doc__,
#                     join='\n\n{}\n'.format('=' * 78), prededent=True)
def axisScales(ax=None, x=None, y=None, z=None, **kw):
    r"""starkplot wrapper for set_x/y/zscale
    """
    set_xscale(ax=ax, x=x, **kw)
    set_yscale(ax=ax, y=y, **kw)
    set_zscale(ax=ax, z=z, **kw)


###############################################################################
# Axis Ticks

# axisTicks(ax, x=None, y=None)
