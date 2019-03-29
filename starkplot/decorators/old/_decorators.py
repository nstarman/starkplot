#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
"""
  Docstring


#############################################################################

Copyright (c) 2018-  Nathaniel Starkman
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  Redistributions in binary form must reproduce the above copyright notice,
     this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  The name of the author may not be used to endorse or promote products
     derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

#############################################################################
Planned Features
- change over to mpl_decorator(func) for all functions which are only
  wrapped and need the funcdocs=func.__doc__ to have their docs

- incorporate the side hists from bovy_plot.bovy_plot into plot
    & do this as a decorator so can attach to functions easily

"""

#############################################################################
# Imports

# import pdb
import numpy as np
from warnings import warn

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import NullFormatter

try:
    from astropy.utils.decorators import wraps
except ImportError as e:
    print("could not import wraps from astropy. using functools' instead")
    from functools import wraps

from matplotlib.cbook import dedent

from .util import axisLabels, axisScales, axisLimits, invertAxis
from .util import _stripprefix, _parseoptsdict, _latexstr, _parselatexstrandopts, _parsestrandopts

#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = ["astropy, matplotlib"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"

#############################################################################
# Docstring Stuff

_descrhead = """
-------------------------------------------------------------------------------
MatplotlibDecorator Docstring Arguments
these are available as kwargs for {func}()
"""

_descrargs = """
# figure controls
fig: Figure, None, 'new'
    default: {fig}
    uses Figure, current figure (if None), or makes new figure (if 'new')
    if fig='new': calls from xkw (key, default value)
        (num, None), (FigureClass, Figure),
        # (line_width, 0.0), (sublotpars, None), (constrained_layout, None)
rtcf: bool, None
    whether to return to the current Figure at the end
    default: {rtcf}
    rtcf = True: always return to current Figure
    rtcf = None: only if passing fig=Figure()
        ie. fig='new' will not return to old Figure at end
    rtcf = False: does not return to current figure
figsize: tuple, None
    auto used if fig='new' else only if overridefig=True
    allows funcs a default if own fig & work in a subplot
    default: {figsize}
    None does nothing
overridefig: bool
    to override current figure properties.
    default: {overridefig}
    If True calls calls from xkw (key, default value)
        (dpi, None), (facecolor, None), (edgecolor, None),
        (frameon, None),
        # TODO (clear, False)
        # TODO add more
savefig: None, str, (str, dict)
    None: does not save
    str: fname
    dict: savefig kwargs. If no dict, draws from xkw.
    prefers xkw['savefig'] else scrapes together (key, default):
        ('dpi', None), ('facecolor', 'w'), ('edgecolor', 'w'),
        ('orientation', 'portrait'), ('papertype', None),
        ('format', None), ('transparent', False),
        ('bbox_inches', None), ('pad_inches', .1),
        ('frameon', None), ('metadata', None)
    default: {savefig}
suptitle: None, str, (str, dict)
    default: {suptitle}
    None: does not assign
    str: suptitle
    dict: kwargs. If no dict, draws from xkw.
    prefers xkw['suptitle'] else scrapes together (key, default):
        ('suptitle_x', .5), ('suptitle_y', .98),
        ('suptitle_ha', 'center'), ('suptitle_va', 'top'),
        ('fontsize', None), ('fontweight', None)
    *xkw['suptitle'] keys should omit prefix 'suptitle_'
tight_layout: dict, bool
    default: {tight_layout}
    True: call tight_layout
    dict: tight_layout is kwargs for fig.tight_layout()
stylesheet: None, str
    temporary stylesheet
    TODO

xkw: dict
    all the other figure, axes options
    default: {xkw}
    possible keys:
        dpi, facecolor, edgecolor, frameon, (clear # TODO),
        num, FigureClass, line_width, subplotpars,
        constrained_layout, orientation, papertype, format,
        transparent, bbox_inches, pad_inches, metadata,
        suptitle_x, suptitle_y, suptitle_ha, suptitle_va,
        fontsize, fontweight,
         savefig, suptitle
    any method (listed below) will first look for an same-key item. failing that, it will draw from the general dict.
    ex:  xkw['savefig'] = **savefig kwargs
         dict(xkw[o] for o in option_names)
    used in:
        savefig (if options not in savefig)
        # TODO add more

# axes controls
ax: Axes Artist, None, int, False, 'next'
    default: {ax}
    uses Axes, gets current axes (if None), makes/gets subplot (at int),
    turns off all axes controls (if False)
    # TODO 'next'
    **Warning if ax=False then all further methods should
        NOT be used, nor have user-set defaults.
title: None, str, (str, dict)
    default: {title}
    (title_loc, 'center'), (title_pad, None), (fontsize, None), (fontweight, None), ...
xlabel: None, str, (str, dict)
    default: {xlabel}
ylabel: None, str, (str, dict)
    default: {ylabel}
zlabel: None, str, (str, dict)
    default: {zlabel}
unit_labels: bool
    whether to use auto labels from astropy.quantity_support()
    default: {unit_labels}
xlim: (lim1, lim2) or (lim1, lim2, emit, auto)
    default: {xlim}
    can ignore all by (None, None, True, False)
ylim:(lim1, lim2) or (lim1, lim2, emit, auto)
    default: {ylim}
    can ignore all by (None, None, True, False)
zlim: (lim1, lim2) or (lim1, lim2, emit, auto)
    default: {zlim}
    can ignore all by (None, None, True, False)
xscale: None, str, (str, dict)
    default: {xscale}
    **does not scrape xkw if no xkw['xscale']
yscale: None, str, (str, dict)
    default: {yscale}
    **does not scrape xkw if no xkw['yscale']
zscale: None, str, (str, dict)
    default: {zscale}
    **does not scrape xkw if no xkw['zscale']
legend: dict
    kwargs for ax.legend()
    default: {legend}


# TODO sidehist bins
"""


###############################################################################
# Functions

class MatplotlibDecorator():
    """docstring for QuantityInputOutput
    """

    @classmethod
    def as_decorator(cls, func=None, funcdoc=None,
                     # figure
                     fig=None, rtcf=None,
                     figsize=None, overridefig=False,
                     savefig=None,
                     suptitle=None,
                     # axes
                     ax=None,
                     title=None,
                     xlabel=None, ylabel=None, zlabel=None, unit_labels=False,
                     xlim=None, ylim=None, zlim=None,
                     invert_axis=None,
                     xscale='linear', yscale='linear', zscale='linear',
                     aspect='auto',
                     legend={},
                     # side hists
                     sidehists=False, shbins=None,
                     shtype='step', shcolor='k',
                     shfc='w', shec='k',
                     shxnormed=True, shynormed=True,
                     shxweights=None, shyweights=None,
                     colorbar=False, clabel=None, clim=None,
                     # style
                     tight_layout={},
                     stylesheet=None,
                     xkw={}):
        r"""MatplotlibDecorator
        func:
        funcdoc:

        # figure controls
        fig: Figure, None, 'new'
            default: None
            uses Figure, current figure (if None), or makes new figure (if 'new')
            if fig='new': calls from xkw (key, default value)
                (num, None), (FigureClass, Figure), (line_width, 0.0),
                (sublotpars, None), (constrained_layout, None)
        rtcf: bool, None
            whether to return to the current Figure at the end
            default: None
            rtcf = True: always return to current Figure
            rtcf = None: only if passing fig=Figure()
                ie. fig='new' will not return to old Figure at end
            rtcf = False: does not return to current figure
        figsize: tuple, None
            auto used if fig='new' else only if overridefig=True
            allows funcs a default if own fig & work in a subplot
            default: None
            None does nothing
        overridefig: bool
            to override current figure properties.
            default: {overridefig}
            If True calls calls from xkw (key, default value)
                (dpi, None), (facecolor, None), (edgecolor, None),
                (frameon, None),
                # TODO (clear, False)
                # TODO add more
        savefig: None, str, (str, dict)
            None: does not save
            str: fname
            dict: savefig kwargs. If no dict, draws from xkw.
            prefers xkw['savefig'] else scrapes together (key, default):
                ('dpi', None), ('facecolor', 'w'), ('edgecolor', 'w'),
                ('orientation', 'portrait'), ('papertype', None),
                ('format', None), ('transparent', False),
                ('bbox_inches', None), ('pad_inches', .1),
                ('frameon', None), ('metadata', None)
            default: None
        suptitle: None, str, (str, dict)
            default: None
            None: does not assign
            str: suptitle
            dict: kwargs. If no dict, draws from xkw.
            prefers xkw['suptitle'] else scrapes together (key, default):
                ('suptitle_x', .5), ('suptitle_y', .98),
                ('suptitle_ha', 'center'), ('suptitle_va', 'top'),
                ('fontsize', None), ('fontweight', None)
            *xkw['suptitle'] keys should omit prefix 'suptitle_'
        tight_layout: dict, bool
            default: {}
            True: call tight_layout
            dict: tight_layout is kwargs for fig.tight_layout()
        stylesheet: None, str
            TODO

        xkw: dict
            all the other figure, axes options
            default: {}
            possible keys:
                dpi, facecolor, edgecolor, frameon, (clear # TODO),
                num, FigureClass, line_width, subplotpars,
                constrained_layout, orientation, papertype, format,
                transparent, bbox_inches, pad_inches, metadata,
                suptitle_x, suptitle_y, suptitle_ha, suptitle_va,
                fontsize, fontweight,
                 savefig, suptitle
            any method (listed below) will first look for an same-key item. failing that, it will draw from the general dict.
            ex:  xkw['savefig'] = **savefig kwargs
                 dict(xkw[o] for o in option_names)
            used in:
                savefig (if options not in savefig)
                # TODO add more

        # axes controls
        ax: Axes Artist, None, int, False, 'next'
            default: None
            uses Axes, gets current axes (if None), makes/gets subplot (at int),
            turns off all axes controls (if False)
            # TODO 'next'
            **Warning if ax=False then all further methods should
                NOT be used, nor have user-set defaults.
        title: None, str, (str, dict)
            default: None
            (title_loc, 'center'), (title_pad, None), (fontsize, None), (fontweight, None), ...
        xlabel: None, str, (str, dict)
            default: None
        ylabel: None, str, (str, dict)
            default: None
        zlabel: None, str, (str, dict)
            default: None
        unit_labels: bool
            whether to use auto labels from astropy.quantity_support()
            default: False
        xlim: (lim1, lim2) or (lim1, lim2, emit, auto)
            default: None
            can ignore all by (None, None, True, False)
        ylim:(lim1, lim2) or (lim1, lim2, emit, auto)
            default: None
            can ignore all by (None, None, True, False)
        zlim: (lim1, lim2) or (lim1, lim2, emit, auto)
            default: None
            can ignore all by (None, None, True, False)
        xscale: None, str, (str, dict)
            default: 'linear'
            **does not scrape xkw if no xkw['xscale']
        yscale: None, str, (str, dict)
            default: 'linear'
            **does not scrape xkw if no xkw['yscale']
        zscale: None, str, (str, dict)
            default: 'linear'
            **does not scrape xkw if no xkw['zscale']
        legend: dict
            kwargs for ax.legend()
            default: {}
        """
        self = cls(
            funcdoc=funcdoc,
            # figure
            fig=fig, rtcf=rtcf,
            figsize=figsize, overridefig=overridefig,
            savefig=savefig,
            suptitle=suptitle,
            # axes
            ax=ax,
            title=title,
            xlabel=xlabel, ylabel=ylabel, zlabel=zlabel,
            unit_labels=unit_labels,
            xlim=xlim, ylim=ylim, zlim=zlim,
            invert_axis=invert_axis,
            xscale=xscale, yscale=yscale, zscale=zscale,
            aspect=aspect,
            legend=legend,
            tight_layout=tight_layout,
            colorbar=colorbar, clabel=clabel, clim=clim,
            sidehists=sidehists, shbins=shbins,
            shtype=shtype, shcolor=shcolor,
            shfc=shfc, shec=shec,
            shxnormed=shxnormed, shynormed=shynormed,
            shxweights=shxweights, shyweights=shyweights,
            stylesheet=stylesheet,
            xkw=xkw,
        )
        if func is not None:
            return self(func)
        else:
            return self

    def __init__(self, func=None, funcdoc=None,
                 # figure
                 fig=None, rtcf=None,
                 figsize=None, overridefig=False, savefig=None,
                 suptitle=None,
                 # axes
                 ax=None,
                 title=None,
                 xlabel=None, ylabel=None, zlabel=None, unit_labels=False,
                 xlim=None, ylim=None, zlim=None,
                 invert_axis=None,
                 xscale='linear', yscale='linear', zscale='linear',
                 aspect='auto',
                 legend={},
                 tight_layout={},
                 colorbar=False, clabel=None, clim=None,
                 sidehists=False, shbins=None,
                 shtype='step', shcolor='k',
                 shfc='w', shec='k',
                 shxnormed=True, shynormed=True,
                 shxweights=None, shyweights=None,
                 stylesheet=None,
                 xkw={}):
        r"""init
        """

        if isinstance(funcdoc, str):
            s = "\n\n{}\n(Wrapped Function's Documentation)\n\n"
            self.funcdoc = s.format('=' * 78) + funcdoc
        else:
            self.funcdoc = ''

        self.xkw = xkw
        self.stylesheet = stylesheet

        self.fig = fig
        self.rtcf = rtcf

        self.figsize = figsize
        self.overridefig = overridefig
        self.savefig = savefig
        # keys & default values for savefig
        self._savefigkdf = (
            ('dpi', None), ('facecolor', 'w'), ('edgecolor', 'w'),
            ('orientation', 'portrait'), ('papertype', None),
            ('format', None), ('transparent', False),
            ('bbox_inches', None), ('pad_inches', .1), ('frameon', None),
            ('metadata', None))

        self.suptitle = suptitle
        self._suptitlekdf = (
            ('suptitle_x', .5), ('suptitle_y', .98),
            ('suptitle_ha', 'center'), ('suptitle_va', 'top'),
            ('fontsize', None), ('fontweight', None))

        self.ax = ax

        self.title = title
        self._titlekdf = (
            ('title_loc', 'center'), ('title_pad', None),
            ('fontsize', None), ('fontweight', None))

        self.xlabel = xlabel
        self._xlabelkdf = (
            ('xlabel_labelpad', None),
            ('fontsize', None), ('fontweight', None))
        self.ylabel = ylabel
        self._ylabelkdf = (
            ('ylabel_labelpad', None),
            ('fontsize', None), ('fontweight', None))
        self.zlabel = zlabel
        self._zlabelkdf = (
            ('zlabel_labelpad', None),
            ('fontsize', None), ('fontweight', None))
        self.unit_labels = unit_labels

        self.xlim = xlim
        self.ylim = ylim
        self.zlim = zlim
        self.invert_axis = invert_axis

        self.xscale = xscale
        self.yscale = yscale
        self.zscale = zscale

        self.aspect = aspect

        self.legend = legend

        self.tight_layout = tight_layout

        self.colorbar = colorbar
        self.clabel = clabel
        self.clim = clim

        self.sidehists = sidehists
        self.shtype = shtype
        self.shbins = shbins
        self.shcolor = shcolor
        self.shfc = shfc
        self.shec = shec
        self.shxnormed = shxnormed
        self.shynormed = shynormed
        self.shxweights = shxweights
        self.shyweights = shyweights

        attrs = ('fig', 'rtcf',
                 'figsize', 'overridefig', 'savefig',
                 'suptitle', 'tight_layout',
                 'ax',
                 'title',
                 'xlabel', 'ylabel', 'zlabel', 'unit_labels',
                 'xlim', 'ylim', 'zlim',
                 'xscale', 'yscale', 'zscale',
                 'legend', 'colorbar', 'xkw')
        self._doc = _descrargs.format(**{k: getattr(self, k).__repr__()
                                         for k in attrs})
        return
    # /def

    def __call__(self, wrapped_function):

        @wraps(wrapped_function)
        def wrapped(*func_args,
                    # figure
                    fig=self.fig, rtcf=self.rtcf,
                    figsize=self.figsize, overridefig=self.overridefig,
                    savefig=self.savefig,
                    suptitle=self.suptitle,
                    # axes
                    ax=self.ax,
                    title=self.title,
                    xlabel=self.xlabel, ylabel=self.ylabel, zlabel=self.zlabel,
                    unit_labels=self.unit_labels,
                    xlim=self.xlim, ylim=self.ylim, zlim=self.zlim,
                    invert_axis=self.invert_axis,
                    xscale=self.xscale, yscale=self.yscale, zscale=self.zscale,
                    aspect=self.aspect,
                    legend=self.legend,
                    tight_layout=self.tight_layout,
                    colorbar=self.colorbar, clabel=self.clabel, clim=self.clim,
                    # sidehists
                    sidehists=self.sidehists, shbins=self.shbins,
                    shtype=self.shtype, shcolor=self.shcolor,
                    shfc=self.shfc, shec=self.shec,
                    shxnormed=self.shxnormed, shynormed=self.shynormed,
                    shxweights=self.shxweights, shyweights=self.shyweights,
                    # styles
                    stylesheet=self.stylesheet,
                    xkw=self.xkw,
                    **func_kwargs):
            """

            fig = plt.figure()
            ax = fig.add_subplot(221)
            ax = fig.add_subplot(222)
            ax = fig.add_subplot(223)
            ax = fig.add_subplot(224)

            print(ax._label)
            ax.set_label(224)
            print(ax._label)

            axs = fig.get_axes()

            num = 121
            def get_digit(number, n):
                return number // 10**n % 10

            # check that shape is right
            # if right, get the number
            axs = fig.get_axes()
            fig.sca(axs[get_digit(num, 2) - 1])
            """

            wkw = self.xkw.copy()
            wkw.update(xkw)

            # Figure
            # Checking on the state of the figure
            # gets / makes figure and determines whether to return the old figure.
            oldfig = None  # default oldfig to None. Does not return to old fig.

            if isinstance(fig, Figure):
                if rtcf in (True, None):  # preserve oldfig
                    oldfig = plt.gcf()
                plt.figure(fig.number)  # makes figure current
            elif fig is None:
                fig = plt.gcf()  # unnecessary?
            elif fig == 'new':
                if rtcf is True:  # preserve oldfig
                    oldfig = plt.gcf()
                _newfigkdf = (('num', None), ('FigureClass', Figure),
                              # ('suplotpars', None), ('line_width', 0.0)
                              ('constrained_layout', None))
                fig = plt.figure(figsize=figsize,
                                 **{k: wkw.pop(k, v) for k, v in _newfigkdf})
            else:
                raise ValueError("fig is not Figure, None, or 'new'")

            # override currrent figure properties
            if overridefig:
                if figsize is not None:
                    fig.set_size_inches(figsize, forward=True)
                fig.set_dpi(wkw.get('dpi', None))
                fig.set_facecolor(wkw.get('facecolor', None))
                fig.set_edgecolor(wkw.get('edgecolor', None))
                fig.set_frameon(wkw.get('frameon', True))
                # TODO add more set_

            # set supertitle
            if suptitle is not None:
                suptitle, sptkw = _parsestrandopts(suptitle)  # get val & kw
                if not sptkw:  # if no kwargs, try from wkw
                    sptkw = wkw.get('suptitle', {})
                    if not sptkw:  # still no kwargs, scrape together from wkw
                        sptkw = {_stripprefix(k, 'suptitle_'): wkw.get(k, v)
                                 for k, v in self._suptitlekdf}
                fig.suptitle(suptitle, **sptkw)

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
                fig.sca(ax)

            # Calling the Function
            if stylesheet is not None:
                with plt.style.context(stylesheet):
                    return_ = wrapped_function(*func_args, **func_kwargs)
            else:
                return_ = wrapped_function(*func_args, **func_kwargs)

            # Setting Axes properties
            # Worries:
            # should this e fig.gca instead of plt.gca ?
            #     if the wrapped_function changes up the figure, then I'd need to
            #     think about what is the optimal behavior
            # what if the wrapped function changes up the axes?
            #     then all the setting of titles and whatnot would be wrong
            #     however, I don't think I can move this above the wrapped function
            #     because ax=False (not the default) allows the wrapped_function
            #     to do whatever it wants.
            #     this means the user has to realize they cannot use any of the
            #     axes specific options if wrapped_function does any axis-change
            #     or other shenanigans.
            # TODO check that all these play well with
            # Getting current axis for assigning plot properties
            ax = plt.gca()

            # set title
            if title is not None:
                title, titlekw = _parsestrandopts(title)
                if not titlekw:  # if no kwargs
                    titlekw = wkw.get('title', {})
                    if not titlekw:  # still no kwargs
                        titlekw = {_stripprefix(k, 'title_'): wkw.get(k, v)
                                   for k, v in self._titlekdf}
                ax.set_title(title, **titlekw)

            ax.set_aspect(aspect)

            # setting axisLabels/limits/scales
            axisLabels(ax, x=xlabel, y=ylabel, z=zlabel,
                       units=unit_labels, xkw=wkw)
            axisLimits(ax, x=xlim, y=ylim, z=zlim)

            if invert_axis is not None:
                invertAxis(ax, x='x' in invert_axis, y='y' in invert_axis,
                           z='z' in invert_axis)

            axisScales(ax, x=xscale, y=yscale, z=zscale, xkw=wkw)

            # Legend
            handles, labels = ax.get_legend_handles_labels()
            if labels:
                legend = _parseoptsdict(legend)
                ax.legend(handles=handles, labels=labels, **legend)

            # Colorbar
            if colorbar:
                cbar = fig.colorbar(return_, ax=ax)
                if clim is not None:
                    cbar.set_clim(*clim)
                if clabel is not None:
                    cbar.set_label(clabel)

            # Tight Layout
            if tight_layout:
                tight_layout = _parseoptsdict(tight_layout)
                fig.tight_layout(**tight_layout)

            # +---- Cleanup ----+
            # saving
            if savefig is not None:
                fname, sfgkw = _parsestrandopts(savefig)  # get val & kw
                if not sfgkw:  # if no kwargs
                    sfgkw = wkw.get('savefig', {})
                    if not sfgkw:  # still no kwargs
                        sfgkw = {k: wkw.get(k, v) for k, v in self._savefigkdf}
                fig.savefig(fname, **sfgkw)

            # old figure
            if oldfig is not None:  # Returning old figure to current status
                plt.figure(oldfig.number)

            # Returning
            return return_
        # /def

        # modifying wrapped_function docstring
        _doc = (self.funcdoc +
                _descrhead.format(func=wrapped_function.__name__) +
                self._doc)
        wrapped.__doc__ = wrapped.__doc__ and dedent(wrapped.__doc__) + _doc
        # if wrapped.__doc__ is None:
        #     wrapped.__doc__ = self.funcdoc + _doc
        # else:
        #     wrapped.__doc__ = dedent(wrapped.__doc__) + self.funcdoc + _doc

        return wrapped
    # /def


###############################################################################

_descrargs = """
# figure controls
fig: Figure, None, 'new'
    default: {fig}
    uses Figure, current figure (if None), or makes new figure (if 'new')
    if fig='new': calls from xkw (key, default value)
        (num, None), (FigureClass, Figure),
        # (line_width, 0.0), (sublotpars, None), (constrained_layout, None)
rtcf: bool, None
    whether to return to the current Figure at the end
    default: {rtcf}
    rtcf = True: always return to current Figure
    rtcf = None: only if passing fig=Figure()
        ie. fig='new' will not return to old Figure at end
    rtcf = False: does not return to current figure
figsize: tuple, None
    auto used if fig='new' else only if overridefig=True
    allows funcs a default if own fig & work in a subplot
    default: {figsize}
    None does nothing
overridefig: bool
    to override current figure properties.
    default: {overridefig}
    If True calls calls from xkw (key, default value)
        (dpi, None), (facecolor, None), (edgecolor, None),
        (frameon, None),
        # TODO (clear, False)
        # TODO add more
savefig: None, str, (str, dict)
    None: does not save
    str: fname
    dict: savefig kwargs. If no dict, draws from xkw.
    prefers xkw['savefig'] else scrapes together (key, default):
        ('dpi', None), ('facecolor', 'w'), ('edgecolor', 'w'),
        ('orientation', 'portrait'), ('papertype', None),
        ('format', None), ('transparent', False),
        ('bbox_inches', None), ('pad_inches', .1),
        ('frameon', None), ('metadata', None)
    default: {savefig}
suptitle: None, str, (str, dict)
    default: {suptitle}
    None: does not assign
    str: suptitle
    dict: kwargs. If no dict, draws from xkw.
    prefers xkw['suptitle'] else scrapes together (key, default):
        ('suptitle_x', .5), ('suptitle_y', .98),
        ('suptitle_ha', 'center'), ('suptitle_va', 'top'),
        ('fontsize', None), ('fontweight', None)
    *xkw['suptitle'] keys should omit prefix 'suptitle_'
tight_layout: dict, bool
    default: {tight_layout}
    True: call tight_layout
    dict: tight_layout is kwargs for fig.tight_layout()
stylesheet: None, str
    temporary stylesheet
    TODO

xkw: dict
    all the other figure, axes options
    default: {xkw}
    possible keys:
        dpi, facecolor, edgecolor, frameon, (clear # TODO),
        num, FigureClass, line_width, subplotpars,
        constrained_layout, orientation, papertype, format,
        transparent, bbox_inches, pad_inches, metadata,
        suptitle_x, suptitle_y, suptitle_ha, suptitle_va,
        fontsize, fontweight,
         savefig, suptitle
    any method (listed below) will first look for an same-key item. failing that, it will draw from the general dict.
    ex:  xkw['savefig'] = **savefig kwargs
         dict(xkw[o] for o in option_names)
    used in:
        savefig (if options not in savefig)
        # TODO add more
"""

# _newfigkdf = 


class FigureDecorator():
    """docstring for QuantityInputOutput
    """

    @classmethod
    def as_decorator(cls, func=None, funcdoc=None,
                     # figure
                     fig=None, rtcf=None,
                     figsize=None, overridefig=False,
                     savefig=None,
                     suptitle=None, stylesheet=None,
                     tight_layout={}, xkw={}):
        r"""FigureDecorator
        func:
        funcdoc:

        # figure controls
        fig: Figure, None, 'new'
            default: None
            uses Figure, current figure (if None), or makes new figure (if 'new')
            if fig='new': calls from xkw (key, default value)
                (num, None), (FigureClass, Figure), (line_width, 0.0),
                (sublotpars, None), (constrained_layout, None)
        rtcf: bool, None
            whether to return to the current Figure at the end
            default: None
            rtcf = True: always return to current Figure
            rtcf = None: only if passing fig=Figure()
                ie. fig='new' will not return to old Figure at end
            rtcf = False: does not return to current figure
        figsize: tuple, None
            auto used if fig='new' else only if overridefig=True
            allows funcs a default if own fig & work in a subplot
            default: None
            None does nothing
        overridefig: bool
            to override current figure properties.
            default: {overridefig}
            If True calls calls from xkw (key, default value)
                (dpi, None), (facecolor, None), (edgecolor, None),
                (frameon, None),
                # TODO (clear, False)
                # TODO add more
        savefig: None, str, (str, dict)
            None: does not save
            str: fname
            dict: savefig kwargs. If no dict, draws from xkw.
            prefers xkw['savefig'] else scrapes together (key, default):
                ('dpi', None), ('facecolor', 'w'), ('edgecolor', 'w'),
                ('orientation', 'portrait'), ('papertype', None),
                ('format', None), ('transparent', False),
                ('bbox_inches', None), ('pad_inches', .1),
                ('frameon', None), ('metadata', None)
            default: None
        suptitle: None, str, (str, dict)
            default: None
            None: does not assign
            str: suptitle
            dict: kwargs. If no dict, draws from xkw.
            prefers xkw['suptitle'] else scrapes together (key, default):
                ('suptitle_x', .5), ('suptitle_y', .98),
                ('suptitle_ha', 'center'), ('suptitle_va', 'top'),
                ('fontsize', None), ('fontweight', None)
            *xkw['suptitle'] keys should omit prefix 'suptitle_'
        tight_layout: dict, bool
            default: {}
            True: call tight_layout
            dict: tight_layout is kwargs for fig.tight_layout()
        stylesheet: None, str
            TODO

        xkw: dict
            all the other figure, axes options
            default: {}
            possible keys:
                dpi, facecolor, edgecolor, frameon, (clear # TODO),
                num, FigureClass, line_width, subplotpars,
                constrained_layout, orientation, papertype, format,
                transparent, bbox_inches, pad_inches, metadata,
                suptitle_x, suptitle_y, suptitle_ha, suptitle_va,
                fontsize, fontweight,
                 savefig, suptitle
            any method (listed below) will first look for an same-key item. failing that, it will draw from the general dict.
            ex:  xkw['savefig'] = **savefig kwargs
                 dict(xkw[o] for o in option_names)
            used in:
                savefig (if options not in savefig)
                # TODO add more
        """
        self = cls(
            funcdoc=funcdoc,
            # figure
            fig=fig, rtcf=rtcf,
            figsize=figsize, overridefig=overridefig,
            savefig=savefig,
            suptitle=suptitle, stylesheet=stylesheet,
            tight_layout=tight_layout, xkw=xkw,
        )
        if func is not None:
            return self(func)
        else:
            return self

    def __init__(self, func=None, funcdoc=None,
                 # figure
                 fig=None, rtcf=None,
                 figsize=None, overridefig=False, savefig=None,
                 suptitle=None,
                 stylesheet=None, tight_layout={}, xkw={}):
        r"""init
        """

        if isinstance(funcdoc, str):
            s = "\n\n{}\n(Wrapped Function's Documentation)\n\n"
            self.funcdoc = s.format('=' * 78) + funcdoc
        else:
            self.funcdoc = ''

        self.xkw = xkw
        self.stylesheet = stylesheet

        self.fig = fig
        self.rtcf = rtcf

        self.figsize = figsize
        self.overridefig = overridefig
        self.savefig = savefig
        # keys & default values for savefig
        self._savefigkdf = (
            ('dpi', None), ('facecolor', 'w'), ('edgecolor', 'w'),
            ('orientation', 'portrait'), ('papertype', None),
            ('format', None), ('transparent', False),
            ('bbox_inches', None), ('pad_inches', .1), ('frameon', None),
            ('metadata', None))

        self.suptitle = suptitle
        self._suptitlekdf = (
            ('suptitle_x', .5), ('suptitle_y', .98),
            ('suptitle_ha', 'center'), ('suptitle_va', 'top'),
            ('fontsize', None), ('fontweight', None))

        attrs = ('fig', 'rtcf',
                 'figsize', 'overridefig', 'savefig',
                 'suptitle', 'tight_layout')
        self._doc = _descrargs.format(**{k: getattr(self, k).__repr__()
                                         for k in attrs})
        return
    # /def

    def __call__(self, wrapped_function):

        @wraps(wrapped_function)
        def wrapped(*func_args,
                    # figure
                    fig=self.fig, rtcf=self.rtcf,
                    figsize=self.figsize, overridefig=self.overridefig,
                    savefig=self.savefig,
                    suptitle=self.suptitle,
                    stylesheet=self.stylesheet,
                    xkw=self.xkw, tight_layout=self.tight_layout,
                    **func_kwargs):
            """
            """

            # Combining dictionaries
            wkw = self.xkw.copy()
            wkw.update(xkw)

            # Figure
            # Checking on the state of the figure
            # gets / makes figure and determines whether to return the old figure.
            oldfig = None  # default oldfig to None. Does not return to old fig.

            if isinstance(fig, Figure):
                if rtcf in (True, None):  # preserve oldfig
                    oldfig = plt.gcf()
                plt.figure(fig.number)  # makes figure current
            elif fig is None:
                fig = plt.gcf()  # unnecessary?
            elif fig == 'new':
                if rtcf is True:  # preserve oldfig
                    oldfig = plt.gcf()
                _newfigkdf = (('num', None), ('FigureClass', Figure),
                              # ('suplotpars', None), ('line_width', 0.0)
                              ('constrained_layout', None))
                fig = plt.figure(figsize=figsize,
                                 **{k: wkw.get(k, v) for k, v in _newfigkdf})
            else:
                raise ValueError("fig is not Figure, None, or 'new'")

            # override currrent figure properties
            if overridefig:
                if figsize is not None:
                    fig.set_size_inches(figsize, forward=True)
                fig.set_dpi(wkw.pop('dpi', None))
                fig.set_facecolor(wkw.pop('facecolor', None))
                fig.set_edgecolor(wkw.pop('edgecolor', None))
                fig.set_frameon(wkw.pop('frameon', True))
                # TODO add more set_

            # set supertitle
            if suptitle is not None:
                suptitle, sptkw = _parsestrandopts(suptitle)  # get val & kw
                if not sptkw:  # if no kwargs, try from wkw
                    sptkw = wkw.pop('suptitle', {})
                    if not sptkw:  # still no kwargs, scrape together from wkw
                        sptkw = {_stripprefix(k, 'suptitle_'): wkw.get(k, v)
                                 for k, v in self._suptitlekdf}
                fig.suptitle(suptitle, **sptkw)

            # Calling the Function
            if stylesheet is not None:
                with plt.style.context(stylesheet):
                    return_ = wrapped_function(*func_args, **func_kwargs)
            else:
                return_ = wrapped_function(*func_args, **func_kwargs)

            # Tight Layout
            if tight_layout:
                tight_layout = _parseoptsdict(tight_layout)
                fig.tight_layout(**tight_layout)

            # +---- Cleanup ----+
            # saving
            if savefig is not None:
                fname, sfgkw = _parsestrandopts(savefig)  # get val & kw
                if not sfgkw:  # if no kwargs
                    sfgkw = wkw.pop('savefig', {})
                    if not sfgkw:  # still no kwargs
                        sfgkw = {k: wkw.get(k, v) for k, v in self._savefigkdf}
                fig.savefig(fname, **sfgkw)

            # old figure
            if oldfig is not None:  # Returning old figure to current status
                plt.figure(oldfig.number)

            # Returning
            return return_
        # /def

        # modifying wrapped_function docstring
        _doc = (self.funcdoc +
                _descrhead.format(func=wrapped_function.__name__) +
                self._doc)
        wrapped.__doc__ = wrapped.__doc__ and dedent(wrapped.__doc__) + _doc

        return wrapped
    # /def


class SideHists(object):
    """docstring for SideHists"""

    @classmethod
    def as_decorator(cls, func=None,
                     sidehists=False, shbins=None,
                     shtype='step', shcolor='k',
                     shfc='w', shec='k',
                     shxnormed=True, shynormed=True,
                     shxweights=None, shyweights=None,
                     colorbar=False, clabel=None, clim=None,
                     xlabel=None, ylabel=None, unit_labels=False,
                     xlim=None, ylim=None,
                     ):
        self = cls(
            sidehists=sidehists, shtype=shtype, shbins=shbins,
            shcolor=shcolor, shfc=shfc,
            shec=shec,
            shxnormed=shxnormed, shynormed=shynormed,
            shxweights=shxweights,
            shyweights=shyweights,
            colorbar=colorbar, clabel=clabel, clim=clim,
            xlabel=xlabel, ylabel=ylabel, unit_labels=unit_labels,
            xlim=xlim, ylim=ylim,
        )
        if func is not None:
            return self(func)
        else:
            return self

    def __init__(self, func=None,
                 sidehists=False, shtype='step', shbins=None,
                 shcolor='k', shfc='w', shec='k',
                 shxnormed=True, shynormed=True,
                 shxweights=None, shyweights=None,
                 colorbar=False, clabel=None, clim=None,
                 xlabel=None, ylabel=None, unit_labels=False,
                 xlim=None, ylim=None,
                 ):
        self.sidehists = sidehists
        self.shtype = shtype
        self.shbins = shbins
        self.shcolor = shcolor
        self.shfc = shfc
        self.shec = shec
        self.shxnormed = shxnormed
        self.shynormed = shynormed
        self.shxweights = shxweights
        self.shyweights = shyweights

        self.colorbar = colorbar
        self.clabel = clabel
        self.clim = clim

        self.xlabel = xlabel
        self.ylabel = ylabel
        self.unit_labels = unit_labels

        self.xlim = xlim
        self.ylim = ylim

    def __call__(self, wrapped_function):

        @wraps(wrapped_function)
        def wrapped(*func_args,
                    sidehists=self.sidehists,
                    shtype=self.shtype, shbins=self.shbins,
                    shcolor=self.shcolor, shfc=self.shfc,
                    shec=self.shec,
                    shxnormed=self.shxnormed,
                    shynormed=self.shynormed,
                    shxweights=self.shxweights,
                    shyweights=self.shyweights,
                    colorbar=self.colorbar, clabel=self.clabel, clim=self.clim,
                    xlabel=self.xlabel, ylabel=self.ylabel,
                    unit_labels=self.unit_labels,
                    xlim=self.xlim, ylim=self.ylim,
                    **func_kwargs):

            ax = plt.gca()

            if shbins is None:
                if isinstance(func_args[0], np.ndarray):
                    shbins = round(0.3 * np.sqrt(func_args[0].shape[0]))
                if isinstance(func_args[0], (list, tuple)):
                    shbins = round(0.3 * np.sqrt(len(func_args[0])))
                else:
                    shbins = 30

            if sidehists:
                nullfmt = NullFormatter()         # no labels
                # definitions for the axes
                # this is directly from bovy_plot
                left, width = 0.1, 0.65
                bottom, height = 0.1, 0.65
                bottom_h = left_h = left + width
                rect_scatter = [left, bottom, width, height]
                rect_histx = [left, bottom_h, width, 0.2]
                rect_histy = [left_h, bottom, 0.2, height]

                ax.set_position(rect_scatter)
                axHistx = plt.axes(rect_histx)
                axHisty = plt.axes(rect_histy)

                # no labels
                axHistx.xaxis.set_major_formatter(nullfmt)
                axHistx.yaxis.set_major_formatter(nullfmt)
                axHisty.xaxis.set_major_formatter(nullfmt)
                axHisty.yaxis.set_major_formatter(nullfmt)

            ax.set_autoscale_on(False)

            # Limits
            if xlim is None:
                arg0 = np.array(func_args[0])
                xlim = (arg0.min(), arg0.max())
            if ylim is None:
                arg1 = np.array(func_args[1])
                ylim = (arg1.min(), arg1.max())

            if clim is None:
                c = func_kwargs.get('c', None)
                if isinstance(c, (list, tuple, np.ndarray)):
                    clim = (min(c), max(c))
                else:
                    clim = None

            return_ = wrapped_function(*func_args, **func_kwargs)

            axisLabels(x=xlabel, y=ylabel, units=unit_labels)
            axisLimits(x=xlim, y=ylim)

            #Add colorbar
            if colorbar:
                cbar = plt.colorbar(return_, ax=ax)
                if clim is not None:
                    cbar.set_clim(*clim)
                if clabel is not None:
                    cbar.set_label(clabel)

            # Add onedhists
            if sidehists:
                histx, edges, patches = axHistx.hist(
                    func_args[0], bins=shbins, normed=shxnormed,
                    weights=shxweights, histtype=shtype,
                    range=sorted(xlim), color=shcolor, fc=shfc, ec=shec)
                histy, edges, patches = axHisty.hist(
                    func_args[1], bins=shbins, orientation='horizontal',
                    weights=shyweights, normed=shynormed, histtype=shtype,
                    range=sorted(ylim), color=shcolor, fc=shfc, ec=shec)
                axHistx.set_xlim(ax.get_xlim())
                axHisty.set_ylim(ax.get_ylim())
                axHistx.set_ylim(0, 1.2 * np.amax(histx))
                axHisty.set_xlim(0, 1.2 * np.amax(histy))

            return return_
            # /def
        return wrapped
    # /def


###############################################################################

mpl_decorator = MatplotlibDecorator.as_decorator

sidehist_decorator = SideHists.as_decorator


###############################################################################

if __name__ == '__main__':

    pass
