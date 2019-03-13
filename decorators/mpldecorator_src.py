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
import types
from warnings import warn

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# 3rd Party Imports

try:
    from astropy.utils.decorators import wraps
except ImportError as e:
    print("could not import wraps from astropy. using functools' instead")
    from functools import wraps

# Custom Imports

from ..util import ObjectWrapper
from ..util import axisLabels, axisScales, axisLimits, invertAxis
from ..util import _stripprefix, _parseoptsdict, _latexstr, _parselatexstrandopts, _parsestrandopts

from ..util import _newfigk, _savefigk, _suptitlek
from ..util import _titlek, _xlabelk, _ylabelk, _zlabelk
from ..util import _cbark

from ..util import prepareFigure, saveFigure, overrideFigure, setSuptitle, tightLayout
from ..util import prepareAxes, setTitle

from ..docstring import dedent, strthentwoline

from .util import MatplotlibDecoratorBase, _funcdocprefix

# decorators
from .figuredecorator_src import FigureDecorator, fig_decorator
from .sidehists_src import SideHists, sidehist_decorator
from .colorbardecorator_src import ColorbarDecorator, cbar_decorator
from .axesdecorator_src import AxesDecorator, ax_decorator

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
    rtcf = None: only if passing fig=Figure()
        ie. fig='new' will not return to old Figure at end
    rtcf = False: does not return to current figure
figsize: tuple, None
    default: {figsize}
    auto used if fig='new' else only if overridefig=True
    None does nothing
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
    'fig', 'rtcf',
    'figsize', 'overridefig', 'savefig', 'closefig',
    'suptitle',
    # style
    'stylesheet', 'tight_layout',
    # axes
    'ax',
    'title', 'xlabel', 'ylabel', 'zlabel', 'unit_labels',
    'xlim', 'ylim', 'zlim', 'invert_axis',
    'xscale', 'yscale', 'zscale', 'aspect',
    'legend',
    # colorbar arguments
    'colorbar', 'clabel', 'clim', 'cloc',
    # sidehist arguments
    'sidehists',
    'shtype', 'shbins', 'shcolor', 'shfc', 'shec',
    'shxdensity', 'shydensity', 'shxweights', 'shyweights',
    # colorbar arguments
    'colorbar', 'clabel', 'clim', 'cloc',
    # sidehist arguments
    'sidehists',
    'shtype', 'shbins', 'shcolor', 'shfc', 'shec',
    'shxdensity', 'shydensity', 'shxweights', 'shyweights',
    # Options
    'xkw'
)


class MatplotlibDecorator(MatplotlibDecoratorBase):
    """docstring for MatplotlibDecorator

    call signature::
        FigureDecorator(
            func=None, funcdoc=None,
            # fig
            fig={fig}, rtcf={rtcf},
            figsize={figsize}, overridefig={overridefig},
            suptitle={suptitle},
            savefig={savefig},
            # ax
            ax={ax},
            title={title},
            xlabel={xlabel}, ylabel={ylabel}, zlabel={zlabel},
            unit_labels={unit_labels},
            xlim={xlim}, ylim={ylim}, zlim={zlim},
            invert_axis={invert_axis},
            xscale={xscale}, yscale={yscale}, zscale={zscale},
            aspect={aspect},
            legend={legend},
            # colorbar arguments
            colorbar={colorbar}, clabel={clabel}, clim={clim}, cloc={cloc},
            # sidehist arguments
            sidehists={sidehists}, shtype={shtype},
            shbins={shbins}, shcolor={shcolor}, shfc={shfc}, shec={shec},
            shxdensity={shxdensity}, shydensity={shydensity},
            shxweights={shxweights}, shyweights={shyweights},
            # style
            stylesheet={stylesheet},
            tight_layout={tight_layout},
            # modifying arguments
            xkw={xkw}, **kwargs
        )

    Methods
    -------
    .as_decorator

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
        rtcf = None: only if passing fig=Figure()
            ie. fig='new' will not return to old Figure at end
        rtcf = False: does not return to current figure
    figsize: tuple, None
        default: {figsize}
        auto used if fig='new' else only if overridefig=True
        None does nothing
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
    invert_axis: str
        # TODO
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

    sidehists: bool
        whether to use sidehists
        default: {sidehists}
    shtype: str
        ax.hist histtype
        default: {shtype}
    shbins: None, int, array
        ax.hist bins
        default: {shbins}
        None uses function args if arg is ndarray, list, or tuple, else shbins=30
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

    @classmethod
    def as_decorator(cls, func=None, funcdoc=None,
                     # figure
                     fig=None, rtcf=None,
                     figsize=None, overridefig=True,
                     savefig=False, closefig=False,
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
                     # colorbar
                     colorbar=False, clabel=None, clim=None, cloc=None,
                     # sidehists
                     sidehists=False, shtype='stepfilled',
                     shbins=None, shcolor='k',
                     shfc=None, shec='k',
                     shxdensity=True, shydensity=True,
                     shxweights=None, shyweights=None,
                     # style
                     stylesheet=None,
                     tight_layout=False,
                     # modifying arguments
                     xkw={}):
        r"""MatplotlibDecorator

        Arguments  # TODO fill out text
        ---------
        func:

        funcdoc:

        fig: Figure, None, 'new'
            default: None
            uses Figure, current figure (if None), or makes new figure (if 'new')
            if fig='new': options from xkw (key, value)
            prefers xkw['fig'] else tries from xkw:
                (override key prefix: 'fig_')
                'num', 'dpi', 'facecolor' 'edgecolor', 'frameon' 'FigureClass',
                'clear', 'sublotpars', 'constrained_layout', 'linewidth',
                * uses figsize arguments
        rtcf: bool, None
            whether to return to the current Figure at the end
            default: None
            rtcf = True: always return to current Figure
            rtcf = None: only if passing fig=Figure()
                ie. fig='new' will not return to old Figure at end
            rtcf = False: does not return to current figure
        figsize: tuple, None
            default: None
            auto used if fig='new' else only if overridefig=True
            None does nothing
        overridefig: bool
            to override current figure properties.
            default: True
            If True calls from xkw:
                figsize, dpi, facecolor, edgecolor, frameon
        savefig: None, str, (str, dict)
            default: False
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
            default: False
        suptitle: None, str, (str, dict)
            default: None
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
            default: False
            dict: tight_layout is kwargs for fig.tight_layout()
            True: call tight_layout with options from xkw
            False, empty dict: do not call tight_layout
            prefers xkw['tight_layout'] else tries from xkw:
                (override key prefix: 'tight_layout_')
                'pad', 'h_pad', 'w_pad', 'rect'
        stylesheet: None, str
            temporary stylesheet
            default: None

        ax: Axes Artist, None, int, False,
            default: None
            uses Axes, gets current axes (if None), make/get subplot (at int),
            turns off all axes controls (if False)
            **Warning if ax=False then all further methods should
                NOT be used, nor have user-set defaults.
        title: None, str, (str, dict)
            default: None
            None: no title
            dict: title kwargs. If no dict, draws from xkw.
            prefers xkw['title'] else tries from xkw:
                'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
        xlabel: None, str, (str, dict)
            default: None
            None: no xlabel
            dict: xlabel kwargs. If no dict, draws from xkw.
            prefers xkw['xlabel'] else tries from xkw:
                'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
        ylabel: None, str, (str, dict)
            default: None
            None: no ylabel
            dict: ylabel kwargs. If no dict, draws from xkw.
            prefers xkw['ylabel'] else tries from xkw:
                'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
        zlabel: None, str, (str, dict)
            default: None
            None: no zlabel
            dict: zlabel kwargs. If no dict, draws from xkw.
            prefers xkw['zlabel'] else tries from xkw:
                'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
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
            None: no xscale
            dict: xscale kwargs. If no dict, draws from xkw.
            prefers xkw['xscale'] else tries from xkw:
                depends on scale type
        yscale: None, str, (str, dict)
            default: 'linear'
            None: no yscale
            dict: yscale kwargs. If no dict, draws from xkw.
            prefers xkw['yscale'] else tries from xkw:
                depends on scale type
        zscale: None, str, (str, dict)
            default: 'linear'
            None: no zscale
            dict: zscale kwargs. If no dict, draws from xkw.
            prefers xkw['zscale'] else tries from xkw:
                depends on scale type
        aspect: str
            the axes aspect
            default: 'auto'
        legend: dict
            kwargs for ax.legend()
            default: empty dict()

        ax: Axes Artist, None, int, False,
            default: None
            uses Axes, gets current axes (if None), make/get subplot (at int),
            turns off all axes controls (if False)
            **Warning if ax=False then all further methods should
                NOT be used, nor have user-set defaults.
        colorbar: dict, bool
            default: True
            dict: colorbar is kwargs for colorbar()
            True: call colorbar with options from xkw
            False, empty dict: do not call colorbar
            prefers xkw['colorbar'] else tries from xkw:
                (override key prefix: 'colorbar')
                'use_gridspec'
        clabel: str, None
            colorbar label
            default: None
        clim: tuple, none
            colorbar limits
            default: None
            does nothing if None
        cloc: str, None, mpl.axes.Axes
            default: None
            None: uses plt.colorbar(ax=)
            'in': uses plt.colorbar(cax=)
            'out': uses plt.colorbar(ax=)
            Axes: uses plt.colorbar(ax=)

        sidehists: bool
            whether to use sidehists
            default: True
        shtype: str
            ax.hist histtype
            default: 'stepfilled'
        shbins: None, int, array
            ax.hist bins
            default: None
            None uses function args if arg is ndarray, list, or tuple,
                else shbins=30
        shcolor:
            ax.hist color
            default: 'k'
        shfc:
            ax.hist facecolor (fc)
            default: None
        shec:
            ax.hist edgecolor (ec)
            default: 'k'
        shxdensity:
            xaxis ax.hist density
            default: True
        shydensity:
            yaxis ax.hist density
            default: True
        shxweights:
            xaxis ax.hist weights
            default: None
        shyweights:
            yaxis ax.hist weights
            default: None

        xkw: dict
            all the other figure, axes, colorbar options
            any method (listed below) will first look for a same-named item.
                failing that, it will draw from the general dict,
                preferring items with keys suffixed by the method's name
                order: 1) 'fig'=dict(...)
                       2) 'fig_dpi', ...   3) 'dpi', ...
            default: empty dict()
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

        # making instance from base class
        self = super(MatplotlibDecorator, cls).__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            # classname=func.__repr__() if func is not None else 'SideHists',
            **{k: _locals.get(k).__repr__() for k in set(_mplattrs)})

        # init
        self.__init__(
            funcdoc=funcdoc,
            # figure
            fig=fig, rtcf=rtcf,
            figsize=figsize, overridefig=overridefig,
            savefig=savefig, closefig=closefig,
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
            # colorbar
            colorbar=colorbar, clabel=clabel, clim=clim, cloc=cloc,
            # sidehists
            sidehists=sidehists, shbins=shbins,
            shtype=shtype, shcolor=shcolor,
            shfc=shfc, shec=shec,
            shxdensity=shxdensity, shydensity=shydensity,
            shxweights=shxweights, shyweights=shyweights,
            # style
            stylesheet=stylesheet,
            tight_layout=tight_layout,
            # modifying arguments
            xkw=xkw,
        )
        if func is not None:
            return self(func)
        else:
            return self
    # /def

    # __new__
    def __new__(cls, func=None, funcdoc=None,
                # figure
                fig=None, rtcf=None,
                figsize=None, overridefig=False,
                savefig=False, closefig=False,
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
                # colorbar
                colorbar=False, clabel=None, clim=None, cloc=None,
                # sidehists
                sidehists=False, shbins=None,
                shtype='stepfilled', shcolor='k',
                shfc=None, shec='k',
                shxdensity=True, shydensity=True,
                shxweights=None, shyweights=None,
                # style
                stylesheet=None, tight_layout=True,
                # modifying arguments
                xkw={}, **kw):

        # making instance from base class
        self = super(MatplotlibDecorator, cls).__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            # classname=func.__repr__() if func is not None else 'SideHists',
            **{k: _locals.get(k).__repr__() for k in set(_mplattrs)})

        # init
        self.__init__(
            # func=newfunc,
            funcdoc=funcdoc,
            # figure
            fig=fig, rtcf=rtcf,
            figsize=figsize, overridefig=overridefig,
            savefig=savefig, closefig=closefig,
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
            # colorbar
            colorbar=colorbar, clabel=clabel, clim=clim, cloc=cloc,
            # sidehists
            sidehists=sidehists, shbins=shbins,
            shtype=shtype, shcolor=shcolor,
            shfc=shfc, shec=shec,
            shxdensity=shxdensity, shydensity=shydensity,
            shxweights=shxweights, shyweights=shyweights,
            # style
            stylesheet=stylesheet,
            tight_layout=tight_layout,
            # modifying arguments
            xkw=xkw, **kw
        )

        return self.as_decorator
    # /def

    # __init__
    def __init__(self, func=None, funcdoc=None,
                 # figure
                 fig=None, rtcf=None,
                 figsize=None, overridefig=False,
                 savefig=False, closefig=False,
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
                 # colorbar
                 colorbar=False, clabel=None, clim=None, cloc=None,
                 # sidehists
                 sidehists=False, shtype='stepfilled', shbins=None,
                 shcolor='k', shfc=None, shec='k',
                 shxdensity=True, shydensity=True,
                 shxweights=None, shyweights=None,
                 # style
                 stylesheet=None, tight_layout=False,
                 # modifying arguments
                 xkw={}, **kw):
        r""""""

        super().__init__()

        # +----------- -----------+

        if kw.get('_topdecorator', True):
            if isinstance(funcdoc, str):
                self.funcdoc = _funcdocprefix + funcdoc
            elif isinstance(funcdoc, types.FunctionType):
                self.funcdoc = _funcdocprefix + funcdoc.__doc__
            else:
                self.funcdoc = ''
            self.funcdoc = strthentwoline(self.funcdoc)  # ensure '\n\n' ending

            # extra arguments
            self.xkw = xkw

            # stylesheet
            self.stylesheet = stylesheet

        # +----------- Figure -----------+

        # figure and return-to-current figure
        self.fig = fig
        self.rtcf = rtcf

        # figsize & s
        self.figsize = figsize
        self.overridefig = overridefig
        self.savefig = savefig
        self.closefig = closefig

        self.suptitle = suptitle

        self.tight_layout = tight_layout

        # +----------- Axes -----------+

        self.ax = ax

        self.title = title

        self.xlabel = xlabel
        self.ylabel = ylabel
        self.zlabel = zlabel
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

        # +----------- Colorbar -----------+

        self.colorbar = colorbar
        self.clabel = clabel
        self.clim = clim
        self.cloc = cloc

        # +----------- Side Hists -----------+
        self.sidehists = sidehists
        self.shtype = shtype
        self.shbins = shbins
        self.shcolor = shcolor
        self.shfc = shfc
        self.shec = shec
        self.shxdensity = shxdensity
        self.shydensity = shydensity
        self.shxweights = shxweights
        self.shyweights = shyweights

        # +----------- Documentation -----------+

        self.attrs += _mplattrs

        self._doc = _descrargs.format(**{k: getattr(self, k).__repr__()
                                         for k in set(_mplattrs)})

        if kw.get('_topdecorator', True):
            self._doc += xkwargs.format(xkw=getattr(self, 'xkw').__repr__())

        return
    # /def

    # __call__
    def __call__(self, wrapped_function):

        @wraps(wrapped_function)
        def wrapped(*func_args,
                    # figure
                    fig=self.fig, rtcf=self.rtcf,
                    figsize=self.figsize, overridefig=self.overridefig,
                    savefig=self.savefig, closefig=self.closefig,
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
                    # colorbar
                    colorbar=self.colorbar, clabel=self.clabel,
                    clim=self.clim, cloc=self.cloc,
                    # sidehists
                    sidehists=self.sidehists,
                    shtype=self.shtype, shbins=self.shbins,
                    shcolor=self.shcolor, shfc=self.shfc,
                    shec=self.shec,
                    shxdensity=self.shxdensity,
                    shydensity=self.shydensity,
                    shxweights=self.shxweights,
                    shyweights=self.shyweights,
                    # style
                    stylesheet=self.stylesheet,
                    tight_layout=self.tight_layout,
                    # modifying arguments
                    xkw=self.xkw,
                    **func_kwargs):
            """
            """
            # PRE

            # combining dictionaries
            wkw = self.xkw.copy()
            wkw.update(xkw)

            # +---- figure ----+
            overridefig = True if fig == 'new' else overridefig
            fig, oldfig = prepareFigure(fig=fig, rtcf=rtcf,
                                        figsize=figsize, **wkw)

            # override currrent figure properties
            if overridefig:
                overrideFigure(fig, figsize=figsize, **wkw)

            # set supertitle
            if suptitle is not None:
                setSuptitle(suptitle, fig=fig, **wkw)

            # +---- axes ----+
            ax = prepareAxes(ax=ax, fig=fig)

            # /PRE
            # CALL

            if stylesheet is not None:
                with plt.style.context(stylesheet):
                    _res = wrapped_function(*func_args, **func_kwargs)
            else:
                _res = wrapped_function(*func_args, **func_kwargs)

            # /CALL
            # POST

            # +---- axes ----+
            if ax is not None:
                ax = plt.gca()

                # set title
                if title is not None:
                    setTitle(title, ax=ax, **wkw)

                ax.set_aspect(aspect)

                # setting axisLabels/limits/scales
                axisLabels(ax, x=xlabel, y=ylabel, z=zlabel,
                           units=unit_labels, **wkw)
                axisLimits(ax, x=xlim, y=ylim, z=zlim)

                if invert_axis is not None:
                    invertAxis(ax, x='x' in invert_axis, y='y' in invert_axis,
                               z='z' in invert_axis)

                axisScales(ax, x=xscale, y=yscale, z=zscale, **wkw)

                # Legend
                handles, labels = ax.get_legend_handles_labels()
                if labels:
                    legend = _parseoptsdict(legend)
                    ax.legend(handles=handles, labels=labels, **legend)

            # +---- figure ----+
            # tight layout
            if tight_layout:
                tightLayout(fig=fig, tlkw=tight_layout, **wkw)

            # saving
            if savefig is not None:
                saveFigure(savefig, fig=fig, **wkw)

            if closefig:
                plt.close(fig)

            # old figure
            if oldfig is not None:  # Returning old figure to current status
                plt.figure(oldfig.number)

            # +---- colorbar ----+
            if colorbar:
                print('colorbar')

                ckw = xkw.get('colorbar', {})
                if not ckw:
                    # allowable arguments
                    ckw = {k: xkw.get(k) for k in _cbark if k in xkw}
                    # any specific overrides
                    ckw.update({_stripprefix(k, 'colorbar_'): v
                                for k, v in ckw.items()
                                if k.startswith('colorbar_')})

                # make colorbar
                if cloc is None:
                    cbar = fig.colorbar(_res, ax=ax, **ckw)
                elif cloc == 'in':
                    cbar = fig.colorbar(_res, cax=ax, **ckw)
                elif cloc == 'out':
                    cbar = fig.colorbar(_res, ax=ax, **ckw)
                elif isinstance(cloc, mpl.axes.Axes):
                    cbar = fig.colorbar(_res, ax=cloc, **ckw)
                # TODO cax in arbitrary axes
                # elif cloc[0] == 'in & isinstance(cloc[1], mpl.axes.Axes):
                #     cbar = fig.colorbar(return_, cax=cloc[1], **ckw)

                if clim is not None:
                    cbar.set_clim(*clim)
                if clabel is not None:
                    cbar.set_label(clabel)

            # +---- sidehists ----+
            if sidehists:

                ax.set_aspect(1.)  # so same size sidehists

                # create new axes on the right and top of the current axes
                # The first argument of the new_vertical/horizontal method is
                # the height (width) of the axes to be created in inches.
                divider = make_axes_locatable(ax)
                axHistx = divider.append_axes("top", 1.2, pad=0.1, sharex=ax)
                axHisty = divider.append_axes("right", 1.2, pad=0.1, sharey=ax)

                # make some labels invisible
                plt.setp(axHistx.get_xticklabels() + axHisty.get_yticklabels(),
                         visible=False)

                if shbins is None:
                    if isinstance(func_args[0], np.ndarray):
                        shbins = round(0.3 * np.sqrt(func_args[0].shape[0]))
                    if isinstance(func_args[0], (list, tuple)):
                        shbins = round(0.3 * np.sqrt(len(func_args[0])))
                    else:
                        shbins = 30
                else:
                    pass

                # _xrange = func_kwargs.get('xlim', None)

                histx, edges, patches = axHistx.hist(
                    func_args[0], bins=shbins,
                    histtype=shtype, weights=shxweights, density=shxdensity,
                    # range=_xrange,
                    color=shcolor, fc=shfc, ec=shec
                )
                histy, edges, patches = axHisty.hist(
                    func_args[1], bins=shbins, orientation='horizontal',
                    histtype=shtype, weights=shyweights, density=shydensity,
                    # range=sorted(ylim),
                    color=shcolor, fc=shfc, ec=shec
                )

            # /POST

            # Returning
            # res = ObjectWrapper(_res, figure=fig)
            return _res
        # /def

        # modifying wrapped_function docstring
        _doc = (self.funcdoc +
                _descrhead.format(func=wrapped_function.__name__) +
                self._doc)
        wrapped.__doc__ = dedent(wrapped.__doc__) + _doc

        return wrapped
    # /def


###############################################################################
# as_decorator

mpl_decorator = MatplotlibDecorator.as_decorator

###############################################################################
