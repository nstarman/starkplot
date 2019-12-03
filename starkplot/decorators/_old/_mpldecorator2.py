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

import numpy as np
import types
from warnings import warn

# plotting
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

try:
    from astropy.utils.decorators import wraps
except ImportError as e:
    print("could not import wraps from astropy. using functools' instead")
    from functools import wraps

# Custom Imports
# decorators
# from ._figuredecorator import FigureDecorator, fig_decorator
# from ._sidehists import SideHists, sidehist_decorator
# from ._colorbardecorator import ColorbarDecorator, cbar_decorator
# from ._axesdecorator import AxesDecorator, ax_decorator
#
from .docstring import cleandoc, strthentwoline
from .util import MatplotlibDecoratorBase, _funcdocprefix

# from ..util import ObjectWrapper
from ..util import axisLabels, axisScales, axisLimits, invertAxis
from ..util import (
    _stripprefix,
    _parseoptsdict,
    _latexstr,
    _parselatexstrandopts,
    _parsestrandopts,
)

from ..util import (
    # figure
    _newfigk,
    _savefigk,
    _suptitlek,
    # axes
    _titlek,
    _xlabelk,
    _ylabelk,
    _zlabelk,
    _cbark,
)

from ..util import (
    # figure
    _prepare_figure,
    save_figure,
    set_suptitle,
    tightLayout,
    override_figure,
    set_figsize,
    # axes
    prepare_axes,
    set_title,
)

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

###############################################################################
# Full Decorator

_decorator_doc = """MatplotlibDecorator

Arguments  # TODO fill out text
---------
func:

funcdoc:

fig: Figure, None, 'new'
    default: {fig}
    uses Figure, current figure (if None), or makes new figure (if 'new')
    if fig='new': options from xkw (key, value)
    prefers xkw['fig'] else tries from xkw:
        (override key prefix: 'fig_')
        'num', 'dpi', 'facecolor' 'edgecolor', 'frameon' 'FigureClass',
        'clear', 'sublotpars', 'constrained_layout', 'linewidth',
        * uses figsize arguments
rtcf: bool, None
    whether to return to the current Figure at the end
    default: {rtcf}
    rtcf = True: always return to current Figure
    rtcf = None: only if passing fig=Figure(), int
        ie. fig='new' will not return to old Figure at end
    rtcf = False: does not return to current figure
figsize: tuple, None
    default: {figsize}
    auto used if fig='new', overridefig=True
    used if figsize is not None
overridefig: bool
    to override current figure properties.
    default: {overridefig}
    If True calls from xkw:
        figsize, dpi, facecolor, edgecolor, frameon
savefig: None, str, (str, dict)
    default: {savefig}
    None: does not save
    str: fname
    dict: savefig kwargs. If no dict, draws from xkw.
    prefers xkw['savefig'] else tries from xkw:
        (override key prefix: 'savefig_')
        'dpi', 'quality', 'facecolor', 'edgecolor', 'orientation',
        'portrait', 'papertype', 'format', 'transparent', 'bbox_inches',
        'pad_inches', 'frameon', 'metadata'
    # TODO allow file-like object, not only str
closefig: bool
    whether to close figure after plotting
    default: {closefig}
suptitle: None, str, (str, dict)
    default: {suptitle}
    None: does not assign
    str: suptitle
    dict: kwargs. If no dict, draws from xkw.
    prefers xkw['suptitle'] else tries from xkw:
        (override key prefix: 'suptitle_')
        'suptitle_x', 'suptitle_y',
        'suptitle_horizontalalignment', 'suptitle_ha',
        'suptitle_verticalalignment', 'suptitle_va',
        'fontsize', 'fontweight'
tight_layout: dict, bool
    default: {tight_layout}
    dict: tight_layout is kwargs for fig.tight_layout()
    True: call tight_layout with options from xkw
    False, empty dict: do not call tight_layout
    prefers xkw['tight_layout'] else tries from xkw:
        (override key prefix: 'tight_layout_')
        'pad', 'h_pad', 'w_pad', 'rect'
stylesheet: None, str
    temporary stylesheet
    default: {stylesheet}

ax: Axes Artist, None, int, False,
    default: {ax}
    uses Axes, gets current axes (if None), make/get subplot (at int),
    turns off all axes controls (if False)
    **Warning if ax=False then all further methods should
        NOT be used, nor have user-set defaults.
title: None, str, (str, dict)
    default: {title}
    None: no title
    dict: title kwargs. If no dict, draws from xkw.
    prefers xkw['title'] else tries from xkw:
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
xlabel: None, str, (str, dict)
    default: {xlabel}
    None: no xlabel
    dict: xlabel kwargs. If no dict, draws from xkw.
    prefers xkw['xlabel'] else tries from xkw:
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
ylabel: None, str, (str, dict)
    default: {ylabel}
    None: no ylabel
    dict: ylabel kwargs. If no dict, draws from xkw.
    prefers xkw['ylabel'] else tries from xkw:
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
zlabel: None, str, (str, dict)
    default: {zlabel}
    None: no zlabel
    dict: zlabel kwargs. If no dict, draws from xkw.
    prefers xkw['zlabel'] else tries from xkw:
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
unit_labels: bool
    whether to use auto labels from astropy.quantity_support()
    default: {unit_labels}
xlim: (lim1, lim2) or (lim1, lim2, emit, auto)
    default: xlim
    can ignore all by (None, None, True, False)
ylim:(lim1, lim2) or (lim1, lim2, emit, auto)
    default: {ylim}
    can ignore all by (None, None, True, False)
zlim: (lim1, lim2) or (lim1, lim2, emit, auto)
    default: {zlim}
    can ignore all by (None, None, True, False)
xscale: None, str, (str, dict)
    default: {xscale}
    None: no xscale
    dict: xscale kwargs. If no dict, draws from xkw.
    prefers xkw['xscale'] else tries from xkw:
        depends on scale type
yscale: None, str, (str, dict)
    default: {yscale}
    None: no yscale
    dict: yscale kwargs. If no dict, draws from xkw.
    prefers xkw['yscale'] else tries from xkw:
        depends on scale type
zscale: None, str, (str, dict)
    default: {zscale}
    None: no zscale
    dict: zscale kwargs. If no dict, draws from xkw.
    prefers xkw['zscale'] else tries from xkw:
        depends on scale type
aspect: str
    the axes aspect
    default: {aspect}
legend: dict
    kwargs for ax.legend()
    default: {legend}

ax: Axes Artist, None, int, False,
    default: {ax}
    uses Axes, gets current axes (if None), make/get subplot (at int),
    turns off all axes controls (if False)
    **Warning if ax=False then all further methods should
        NOT be used, nor have user-set defaults.
colorbar: dict, bool
    default: {colorbar}
    dict: colorbar is kwargs for colorbar()
    True: call colorbar with options from xkw
    False, empty dict: do not call colorbar
    prefers xkw['colorbar'] else tries from xkw:
        (override key prefix: 'colorbar')
        'use_gridspec'
clabel: str, None
    colorbar label
    default: {clabel}
clim: tuple, none
    colorbar limits
    default: {clim}
    does nothing if None
cloc: str, None, mpl.axes.Axes
    default: {cloc}
    None: uses plt.colorbar(ax=)
    'in': uses plt.colorbar(cax=)
    'out': uses plt.colorbar(ax=)
    Axes: uses plt.colorbar(ax=)

sidehists: bool
    whether to use sidehists
    default: {sidehists}
shtype: str
    ax.hist histtype
    default: {shtype}
shbins: None, int, array
    ax.hist bins
    default: {shbins}
    None uses function args if arg is ndarray, list, or tuple,
        else shbins=30
shcolor:
    ax.hist color
    default: {shcolor}
shfc:
    ax.hist facecolor (fc)
    default: {shfc}
shec:
    ax.hist edgecolor (ec)
    default: {shec}
shxdensity:
    xaxis ax.hist density
    default: {shxdensity}
shydensity:
    yaxis ax.hist density
    default: {shydensity}
shxweights:
    xaxis ax.hist weights
    default: {shxweights}
shyweights:
    yaxis ax.hist weights
    default: {shyweights}

xkw: dict
    all the other figure, axes, colorbar options
    any method (listed below) will first look for a same-named item.
        failing that, it will draw from the general dict,
        preferring items with keys suffixed by the method's name
        order: 1) 'fig'=dict(...)
               2) 'fig_dpi', ...   3) 'dpi', ...
    default: {xkw}
    possible keys:
        # full keys
        fig, savefig, suptitle, tight_layout,
        title, xlabel, ylabel, zlabel, colorbar
        # general keys
        num, dpi, facecolor, edgecolor, frameon, FigureClass,
        clear, subplotpars, constrained_layout, line_width,
        pad, h_pad, w_pad, rect,
        orientation, portrait, papertype, format, transparent,
        bbox_inches, pad_inches, metadata,
        fontsize, fontweight,
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
        'use_gridspec', plt.colorbar kwargs
    used in:
        fig, overridefig, suptitle[*], savefig[*], tight_layout[*],
        title[*], xlabel[*], ylabel[*], zlabel[*], xlim, ylim, zlim,
        invert_xaxis, invert_yaxis, invert_zaxis,
        xscale[*], yscale[*], zscale[*],
        colorbar[*]
        [*] if options not in argument
        # TODO add more
    ex:  xkw['savefig'] = **savefig kwargs
         dict(xkw[o] for o in option_names)

Returns
-------
decorator if func = None
decorated function otherwise
"""

_descrhead = """
===============================================================================
                    MatplotlibDecorator Docstring Arguments
===============================================================================
these are available as kwargs for {func}()
"""

_descrargs = """
# figure controls
fig: Figure, None, 'new'
    default: {fig}
    uses Figure, current figure (if None), or makes new figure (if 'new')
    if fig='new': options from xkw (key, value)
    prefers xkw['fig'] else tries from xkw:
        (override key prefix: 'fig_')
        'num', 'dpi', 'facecolor' 'edgecolor', 'frameon' 'FigureClass',
        'clear', 'sublotpars', 'constrained_layout', 'linewidth',
        * uses figsize arguments
rtcf: bool, None
    whether to return to the current Figure at the end
    default: {rtcf}
    rtcf = True: always return to current Figure
    rtcf = None: only if passing fig=Figure(), int
        ie. fig='new' will not return to old Figure at end
    rtcf = False: does not return to current figure
figsize: tuple, None
    default: {figsize}
    auto used if fig='new' else only if overridefig=True
    None does nothing
overridefig: bool
    to override current figure properties (like figsize).
    default: {overridefig}
    If True calls from xkw:
        figsize, dpi, facecolor, edgecolor, frameon
savefig: None, str, (str, dict)
    default: {savefig}
    None: does not save
    str: fname
    dict: savefig kwargs. If no dict, draws from xkw.
    prefers xkw['savefig'] else tries from xkw:
        (override key prefix: 'savefig_')
        'dpi', 'quality', 'facecolor', 'edgecolor', 'orientation',
        'portrait', 'papertype', 'format', 'transparent', 'bbox_inches',
        'pad_inches', 'frameon', 'metadata'
    # TODO allow file-like object, not only str
closefig: bool
    whether to close figure after plotting
    default: {closefig}
suptitle: None, str, (str, dict)
    default: {suptitle}
    None: does not assign
    str: suptitle
    dict: kwargs. If no dict, draws from xkw.
    prefers xkw['suptitle'] else tries from xkw:
        (override key prefix: 'suptitle_')
        'suptitle_x', 'suptitle_y',
        'suptitle_horizontalalignment', 'suptitle_ha',
        'suptitle_verticalalignment', 'suptitle_va',
        'fontsize', 'fontweight'
tight_layout: dict, bool
    kwargs for plt.tight_layout()
    default: {tight_layout}
    dict: tight_layout is kwargs for fig.tight_layout()
    True: call tight_layout with options from xkw
    False, empty dict: do not call tight_layout
    prefers xkw['tight_layout'] else tries from xkw:
        (override key prefix: 'tight_layout_')
        'pad', 'h_pad', 'w_pad', 'rect'
stylesheet: None, str
    temporary stylesheet
    default: {stylesheet}
    ** NOT WORKING

ax: Axes Artist, None, int, False,
    default: {ax}
    uses Axes, gets current axes (if None), makes/gets subplot (at int),
    turns off all axes controls (if False)
    **Warning if ax=False then all further methods should
        NOT be used, nor have user-set defaults.
title: None, str, (str, dict)
    default: {title}
    None: no title
    dict: title kwargs. If no dict, draws from xkw.
    prefers xkw['title'] else tries from xkw:
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
xlabel: None, str, (str, dict)
    default: {xlabel}
    None: no xlabel
    dict: xlabel kwargs. If no dict, draws from xkw.
    prefers xkw['xlabel'] else tries from xkw:
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
ylabel: None, str, (str, dict)
    default: {ylabel}
    None: no ylabel
    dict: ylabel kwargs. If no dict, draws from xkw.
    prefers xkw['ylabel'] else tries from xkw:
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
zlabel: None, str, (str, dict)
    default: {zlabel}
    None: no zlabel
    dict: zlabel kwargs. If no dict, draws from xkw.
    prefers xkw['zlabel'] else tries from xkw:
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
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
    None: no xscale
    dict: xscale kwargs. If no dict, draws from xkw.
    prefers xkw['xscale'] else tries from xkw:
        depends on scale type
yscale: None, str, (str, dict)
    default: {yscale}
    None: no yscale
    dict: yscale kwargs. If no dict, draws from xkw.
    prefers xkw['yscale'] else tries from xkw:
        depends on scale type
zscale: None, str, (str, dict)
    default: {zscale}
    None: no zscale
    dict: zscale kwargs. If no dict, draws from xkw.
    prefers xkw['zscale'] else tries from xkw:
        depends on scale type
aspect: str
    the axes aspect
    default: {aspect}
legend: dict
    kwargs for ax.legend()
    default: {legend}

colorbar: dict, bool
    default: {colorbar}
    dict: colorbar is kwargs for colorbar()
    True: call colorbar with options from xkw
    False, empty dict: do not call colorbar
    prefers xkw['colorbar'] else tries from xkw:
        (override key prefix: 'colorbar')
        'use_gridspec'
clabel: str, None
    colorbar label
    default: {clabel}
clim: tuple, none
    colorbar limits
    default: {clim}
    does nothing if None
cloc: str, None, mpl.axes.Axes
    default: {cloc}
    None: uses plt.colorbar(ax=)
    'in': uses plt.colorbar(cax=)
    'out': uses plt.colorbar(ax=)
    Axes: uses plt.colorbar(ax=)
"""

xkwargs = """
xkw: dict
    all the other figure, axes, colorbar options
    any method (listed below) will first look for a same-named item.
        failing that, it will draw from the general dict, preferring items
        with keys suffixed by the method's name
        order: 1) 'fig'=dict(...)
               2) 'fig_dpi', ...   3) 'dpi', ...
    default: {xkw}
    possible keys:
        # full keys
        fig, savefig, suptitle, tight_layout,
        title, xlabel, ylabel, zlabel, colorbar
        # general keys
        num, dpi, facecolor, edgecolor, frameon, FigureClass,
        clear, subplotpars, constrained_layout, line_width,
        pad, h_pad, w_pad, rect,
        orientation, portrait, papertype, format, transparent,
        bbox_inches, pad_inches, metadata,
        fontsize, fontweight,
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
        'use_gridspec', plt.colorbar kwargs
    used in:
        fig, overridefig, suptitle[*], savefig[*], tight_layout[*], savefig[*]
        title[*], xlabel[*], ylabel[*], zlabel[*], xlim, ylim, zlim,
        invert_xaxis, invert_yaxis, invert_zaxis,
        xscale[*], yscale[*], zscale[*],
        colorbar[*]
        [*] if options not in argument
        # TODO add more
    ex:  xkw['savefig'] = **savefig kwargs
         dict(xkw[o] for o in option_names)
"""

_mplattrs = (
    # figure
    "fig",
    "rtcf",
    "figsize",
    "overridefig",
    "savefig",
    "closefig",
    "suptitle",
    # style
    "stylesheet",
    "tight_layout",
    # axes
    "ax",
    "title",
    "xlabel",
    "ylabel",
    "zlabel",
    "unit_labels",
    "xlim",
    "ylim",
    "zlim",
    "invert_axis",
    "xscale",
    "yscale",
    "zscale",
    "aspect",
    "legend",
    # colorbar arguments
    "colorbar",
    "clabel",
    "clim",
    "cloc",
    # sidehist arguments
    "sidehists",
    "shtype",
    "shbins",
    "shcolor",
    "shfc",
    "shec",
    "shxdensity",
    "shydensity",
    "shxweights",
    "shyweights",
    # colorbar arguments
    "colorbar",
    "clabel",
    "clim",
    "cloc",
    # sidehist arguments
    "sidehists",
    "shtype",
    "shbins",
    "shcolor",
    "shfc",
    "shec",
    "shxdensity",
    "shydensity",
    "shxweights",
    "shyweights",
    # Options
    "xkw",
)
