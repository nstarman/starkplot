#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
"""
  starkplot.py: general wrappers for matplotlib plotting

      'public' methods:
            plot

  Methods derived from bovy_plot
        end_print <--- bovy_end_print


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

import re
from warnings import warn
import numpy as np
from scipy import special
from scipy import interpolate

from astropy.utils.decorators import wraps

from matplotlib import pyplot
from matplotlib.figure import Figure
# import matplotlib.ticker as ticker
import matplotlib.cm as cm
from matplotlib.ticker import NullFormatter, MultipleLocator

# custom imports
from .decorators import mpl_decorator
from . import docstring
from .util import _stripprefix, _parseoptsdict, _latexstr, _parselatexstrandopts, _parsestrandopts
from .util import axisLabels, axisScales

# TODO get rid of
try:
    from galpy.util import bovy_plot
except Exception as e:
    print('cannot import galpy.bovy_plot')

    BOVY_PLOT_IMPORTED = False
else:
    BOVY_PLOT_IMPORTED = True
    from galpy.util.bovy_plot import bovy_dens2d, bovy_plot


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
# Helper Stuff

_plttypes = (
    'acorr', 'angle_spectrum',
    'axhline', 'axhspan', 'axvline', 'axvspan',
    'bar', 'barbs', 'barh', 'broken_barh', 'box', 'boxplot',
    'cohere', 'contour', 'contourf', 'csd',
    'errorbar', 'eventplot',
    'figimage', 'fill', 'fill_between', 'fill_betweenx',
    'hexbin', 'hist', 'hist2d', 'hlines',
    'imshow',
    'loglog',
    'magnitude_spectrum', 'matshow',
    'pcolor', 'pcolormesh', 'phase_spectrum', 'pie',
    'plot', 'plot_date', 'plotfile', 'polar', 'psd',
    'quiver',
    'rgrids',
    'scatter', 'sci', 'semilogx', 'semilogy', 'specgram',
    'spy', 'stackplot', 'stem', 'step', 'streamplot',
    'tricontour', 'tricontourf', 'tripcolor', 'triplot',
    'violinplot', 'vlines',
    'xcorr',
)

_annotations = (
    'add_axis_labels', 'add_unit_axis_labels', 'annotate', 'clabel',
    'colorbar', 'figlegend', 'figtext', 'legend', 'suptitle',
    'table', 'text', 'title', 'xlabel', 'ylabel')

_customadded = (
    'add_axis_labels', 'add_unit_axis_labels',
    'add_axis_limits',
    'add_axis_scales',
                )

_other = (
    'autoscale', 'axes', 'axis',
    'cla', 'clf', 'clim', 'close', 'cm', 'colormaps', 'connect', 'cycler',
    'dedent', 'delaxes', 'deprecated', 'disconnect',
    'docstring', 'draw', 'draw_all', 'draw_if_interactive',
    'figaspect', 'fignum_exists', 'figure', 'findobj',
    'gca', 'gcf', 'gci', 'get', 'get_backend', 'get_cmap',
    'get_current_fig_manager', 'get_figlabels', 'get_fignums',
    'get_plot_commands', 'get_scale_docs', 'get_scale_names', 'getp',
    'ginput', 'grid',
    'importlib', 'imread', 'imsave', 'inspect', 'install_repl_displayhook',
    'interactive', 'ioff', 'ion', 'isinteractive',
    'locator_params', 'logging',
    'margins', 'matplotlib', 'minorticks_off', 'minorticks_on', 'mlab',
    'new_figure_manager',
    'pause', 'plotting', 'prism', 'pylab_setup',
    'quiverkey',
    'rc', 'rcParams', 'rcParamsDefault', 'rcParamsOrig', 'rc_context',
    'rcdefaults', 'rcsetup', 're', 'register_cmap',
    'savefig', 'sca', 'set_cmap', 'setp', 'show', 'silent_list', 'style',
    'subplot', 'subplot2grid', 'subplot_tool', 'subplots',
    'subplots_adjust', 'switch_backend', 'sys',
    'thetagrids', 'tick_params', 'ticklabel_format', 'tight_layout',
    'time', 'twinx', 'twiny',
    'uninstall_repl_displayhook',
    'waitforbuttonpress', 'warn_deprecated', 'warnings',
    'xkcd', 'xlim',
    'xscale', 'xticks',
    'ylim', 'yscale', 'yticks'
)


###############################################################################
# To Organize Functions

@mpl_decorator()
def axes(*args, **kw):
    return pyplot.axes(*args, **kw)


def gcf():
    return pyplot.gcf()

def gca():
    return pyplot.gca()


# @mpl_decorator()
# def figure(*args, **kw):
#     return pyplot.gcf()


###############################################################################
# Plotting Functions

@mpl_decorator()
def plot(*args, plttype='plot', **kwargs):
    r"""
    plttype:
    ====================== ===================================================
    Function               Description
    ====================== ===================================================
    `acorr`                Plot the autocorrelation of *x*.
    `angle_spectrum`       Plot the angle spectrum.
    `axhline`              Add a horizontal line across the axis.
    `axhspan`              Add a horizontal span (rectangle) across the axis.
    `axvline`              Add a vertical line across the axes.
    `axvspan`              Add a vertical span (rectangle) across the axes.
    `bar`                  Make a bar plot.
    `barbs`                Plot a 2-D field of barbs.
    `barh`                 Make a horizontal bar plot.
    `boxplot`              Make a box and whisker plot.
    `broken_barh`          Plot a horizontal sequence of rectangles.
    `cohere`               Plot the coherence between *x* and *y*.
    `contour`              Plot contours.
    `contourf`             Plot contours.
    `csd`                  Plot the cross-spectral density.
    `errorbar`             Plot y vs x as lines &/or markers w/ errorbars.
    `eventplot`            Plot identical parallel lines at given positions.
    `figimage`             Add a non-resampled image to the figure
    `fill`                 Plot filled polygons.
    `fill_between`         Fill the area between two horizontal curves.
    `fill_betweenx`        Fill the area between two vertical curves.
    `hexbin`               Make a hexagonal binning plot.
    `hist`                 Plot a histogram.
    `hist2d`               Make a 2D histogram plot.
    `hlines`               Plot horizontal lines at each *y* from *xmin*-*xmax*.
    `imshow`               Display an image, i.e.
    `loglog`               Make a plot with log scaling on both the x and y axis.
    `magnitude_spectrum`   Plot the magnitude spectrum.
    `matshow`              Display an array as a matrix in a new figure window.
    `pcolor`               Create a pseudocolor plot with a non-regular rectangular grid.
    `pcolormesh`           Create a pseudocolor plot with a non-regular rectangular grid.
    `phase_spectrum`       Plot the phase spectrum.
    `pie`                  Plot a pie chart.
    `plot`                 Plot y versus x as lines and/or markers.
    `plot_date`            Plot data that contains dates.
    `plotfile`             Plot the data in a file.
    `polar`                Make a polar plot.
    `psd`                  Plot the power spectral density.
    `quiver`               Plot a 2-D field of arrows.
    `scatter`              A scatter plot of *y* vs *x* with varying marker size and/or color.
    `semilogx`             Make a plot with log scaling on the x axis.
    `semilogy`             Make a plot with log scaling on the y axis.
    `specgram`             Plot a spectrogram.
    `spy`                  Plot the sparsity pattern of a 2D array
    `stackplot`            Draw a stacked area plot.
    `stem`                 Create a stem plot.
    `step`                 Make a step plot.
    `streamplot`           Draw streamlines of a vector flow.
    `table`                Add a table to the current axes.
    `tricontour`           Draw contours on an unstructured triangular grid.
    `tricontourf`          Draw contours on an unstructured triangular grid.
    `tripcolor`            Create a pseudocolor plot of an unstructured triangular grid.
    `triplot`              Draw a unstructured triangular grid as lines and/or markers.
    `violinplot`           Make a violin plot.
    `vlines`               Plot vertical lines.
    `xcorr`                Plot the cross correlation between *x* and *y*.
    ====================== ===================================================
    """

    # The Common Plot Types
    if plttype == 'plot':
        res = pyplot.plot(*args, **kwargs)

    elif plttype == 'scatter':
        res = pyplot.scatter(*args, **kwargs)

    elif plttype == 'errorbar':
        res = pyplot.errorbar(*args, **kwargs)

    elif plttype == 'loglog':
        res = pyplot.loglog(*args, **kwargs)

    elif plttype == 'semilogx':
        res = pyplot.semilogx(*args, **kwargs)

    elif plttype == 'semilogy':
        res = pyplot.semilogy(*args, **kwargs)

    elif plttype == 'hist':
        res = pyplot.hist(*args, **kwargs)

    # Try all options in _plttypes
    elif plttype in _plttypes:
        res = getattr(pyplot, plttype)(*args, **kwargs)

    # Permitting any pyplot function
    elif isinstance(plttype, str):
        try:
            getattr(pyplot, plttype)
        except Exception as e:
            raise ValueError(f'invalid plttype {plttype}')  #
        else:
            warn('using unsanctioned plotting method')
            getattr(pyplot, plttype)(*args, **kwargs)
    else:
        raise ValueError(f'invalid plttype {plttype}')

    return res


@mpl_decorator(funcdoc=pyplot.acorr.__doc__)
def acorr(*args, **kwargs):
    r"""starkplot wrapper for acorr"""
    return pyplot.acorr(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.angle_spectrum.__doc__)
def angle_spectrum(*args, **kwargs):
    r"""starkplot wrapper for angle_spectrum"""
    return pyplot.angle_spectrum(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.axhline.__doc__)
def axhline(*args, **kwargs):
    r"""starkplot wrapper for axhline"""
    return pyplot.axhline(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.axhspan.__doc__)
def axhspan(*args, **kwargs):
    r"""starkplot wrapper for axhspan"""
    return pyplot.axhspan(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.axvline.__doc__)
def axvline(*args, **kwargs):
    r"""starkplot wrapper for axvline"""
    return pyplot.axvline(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.axvspan.__doc__)
def axvspan(*args, **kwargs):
    r"""starkplot wrapper for axvspan"""
    return pyplot.axvspan(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.bar.__doc__)
def bar(*args, **kwargs):
    r"""starkplot wrapper for bar"""
    return pyplot.bar(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.barbs.__doc__)
def barbs(*args, **kwargs):
    r"""starkplot wrapper for barbs"""
    return pyplot.barbs(*args, **kwargs)

# barbs = mpl_decorator(pyplot.barbs)


@mpl_decorator(funcdoc=pyplot.barh.__doc__)
def barh(*args, **kwargs):
    r"""starkplot wrapper for barh"""
    return pyplot.barh(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.boxplot.__doc__)
def boxplot(*args, **kwargs):
    r"""starkplot wrapper for boxplot"""
    return pyplot.boxplot(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.broken_barh.__doc__)
def broken_barh(*args, **kwargs):
    r"""starkplot wrapper for broken_barh"""
    return pyplot.broken_barh(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.cohere.__doc__)
def cohere(*args, **kwargs):
    r"""starkplot wrapper for cohere"""
    return pyplot.cohere(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.contour.__doc__)
def contour(*args, **kwargs):
    r"""starkplot wrapper for contour"""
    return pyplot.contour(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.contourf.__doc__)
def contourf(*args, **kwargs):
    r"""starkplot wrapper for contourf"""
    return pyplot.contourf(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.csd.__doc__)
def csd(*args, **kwargs):
    r"""starkplot wrapper for csd"""
    return pyplot.csd(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.errorbar.__doc__)
def errorbar(*args, **kwargs):
    r"""starkplot wrapper for errorbar"""
    return pyplot.errorbar(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.eventplot.__doc__)
def eventplot(*args, **kwargs):
    r"""starkplot wrapper for eventplot"""
    return pyplot.eventplot(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.figimage.__doc__)
def figimage(*args, **kwargs):
    r"""starkplot wrapper for figimage"""
    return pyplot.figimage(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.fill.__doc__)
def fill(*args, **kwargs):
    r"""starkplot wrapper for fill"""
    return pyplot.fill(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.fill_between.__doc__)
def fill_between(*args, **kwargs):
    r"""starkplot wrapper for fill_between"""
    return pyplot.fill_between(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.fill_betweenx.__doc__)
def fill_betweenx(*args, **kwargs):
    r"""starkplot wrapper for fill_betweenx"""
    return pyplot.fill_betweenx(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.hexbin.__doc__)
def hexbin(*args, **kwargs):
    r"""starkplot wrapper for hexbin"""
    return pyplot.hexbin(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.hist.__doc__)
def hist(*args, **kwargs):
    r"""starkplot wrapper for hist"""
    return pyplot.hist(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.hist2d.__doc__)
def hist2d(*args, **kwargs):
    r"""starkplot wrapper for hist2d"""
    return pyplot.hist2d(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.hlines.__doc__)
def hlines(*args, **kwargs):
    r"""starkplot wrapper for hlines"""
    return pyplot.hlines(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.imshow.__doc__)
def imshow(*args, **kwargs):
    r"""starkplot wrapper for imshow"""
    return pyplot.imshow(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.loglog.__doc__)
def loglog(*args, **kwargs):
    r"""starkplot wrapper for loglog"""
    return pyplot.loglog(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.magnitude_spectrum.__doc__)
def magnitude_spectrum(*args, **kwargs):
    r"""starkplot wrapper for magnitude_spectrum"""
    return pyplot.magnitude_spectrum(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.matshow.__doc__)
def matshow(*args, **kwargs):
    r"""starkplot wrapper for matshow"""
    return pyplot.matshow(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.pcolor.__doc__)
def pcolor(*args, **kwargs):
    r"""starkplot wrapper for pcolor"""
    return pyplot.pcolor(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.pcolormesh.__doc__)
def pcolormesh(*args, **kwargs):
    r"""starkplot wrapper for pcolormesh"""
    return pyplot.pcolormesh(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.phase_spectrum.__doc__)
def phase_spectrum(*args, **kwargs):
    r"""starkplot wrapper for phase_spectrum"""
    return pyplot.phase_spectrum(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.pie.__doc__)
def pie(*args, **kwargs):
    r"""starkplot wrapper for pie"""
    return pyplot.pie(*args, **kwargs)


# @mpl_decorator(funcdoc=pyplot.plot.__doc__)
# def plot(*args, **kwargs):
#     r"""starkplot wrapper for plot"""
#     return pyplot.plot(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.plot_date.__doc__)
def plot_date(*args, **kwargs):
    r"""starkplot wrapper for plot_date"""
    return pyplot.plot_date(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.plotfile.__doc__)
def plotfile(*args, **kwargs):
    r"""starkplot wrapper for plotfile"""
    return pyplot.plotfile(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.polar.__doc__)
def polar(*args, **kwargs):
    r"""starkplot wrapper for polar"""
    return pyplot.polar(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.psd.__doc__)
def psd(*args, **kwargs):
    r"""starkplot wrapper for psd"""
    return pyplot.psd(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.quiver.__doc__)
def quiver(*args, **kwargs):
    r"""starkplot wrapper for quiver"""
    return pyplot.quiver(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.rgrids.__doc__)
def rgrids(*args, **kwargs):
    r"""starkplot wrapper for rgrids"""
    return pyplot.rgrids(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.scatter.__doc__)
def scatter(*args, **kwargs):
    r"""starkplot wrapper for scatter"""
    return pyplot.scatter(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.semilogx.__doc__)
def semilogx(*args, **kwargs):
    r"""starkplot wrapper for semilogx"""
    return pyplot.semilogx(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.semilogy.__doc__)
def semilogy(*args, **kwargs):
    r"""starkplot wrapper for semilogy"""
    return pyplot.semilogy(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.specgram.__doc__)
def specgram(*args, **kwargs):
    r"""starkplot wrapper for specgram"""
    return pyplot.specgram(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.spy.__doc__)
def spy(*args, **kwargs):
    r"""starkplot wrapper for spy"""
    return pyplot.spy(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.stackplot.__doc__)
def stackplot(*args, **kwargs):
    r"""starkplot wrapper for stackplot"""
    return pyplot.stackplot(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.stem.__doc__)
def stem(*args, **kwargs):
    r"""starkplot wrapper for stem"""
    return pyplot.stem(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.step.__doc__)
def step(*args, **kwargs):
    r"""starkplot wrapper for step"""
    return pyplot.step(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.streamplot.__doc__)
def streamplot(*args, **kwargs):
    r"""starkplot wrapper for streamplot"""
    return pyplot.streamplot(*args, **kwargs)


# def table(*args, **kwargs):  # is this an annotation?
#     r"""starkplot wrapper for table"""
#     return pyplot.table(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.tricontour.__doc__)
def tricontour(*args, **kwargs):
    r"""starkplot wrapper for tricontour"""
    return pyplot.tricontour(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.tricontourf.__doc__)
def tricontourf(*args, **kwargs):
    r"""starkplot wrapper for tricontourf"""
    return pyplot.tricontourf(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.tripcolor.__doc__)
def tripcolor(*args, **kwargs):
    r"""starkplot wrapper for tripcolor"""
    return pyplot.tripcolor(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.triplot.__doc__)
def triplot(*args, **kwargs):
    r"""starkplot wrapper for triplot"""
    return pyplot.triplot(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.violinplot.__doc__)
def violinplot(*args, **kwargs):
    r"""starkplot wrapper for violinplot"""
    return pyplot.violinplot(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.vlines.__doc__)
def vlines(*args, **kwargs):
    r"""starkplot wrapper for vlines"""
    return pyplot.vlines(*args, **kwargs)


@mpl_decorator(funcdoc=pyplot.xcorr.__doc__)
def xcorr(*args, **kwargs):
    r"""starkplot wrapper for xcorr"""
    return pyplot.xcorr(*args, **kwargs)


def scatterplot(x, y, *args, **kwargs):
    """ #TODO adapt to starkplot. Can test out my SideHists wrapper
    NAME:

       scatterplot

    PURPOSE:

       make a 'smart' scatterplot that is a density plot in high-density
       regions and a regular scatterplot for outliers

    INPUT:

       x, y

       xlabel - (raw string!) x-axis label, LaTeX math mode, no $s needed

       ylabel - (raw string!) y-axis label, LaTeX math mode, no $s needed

       xrange

       yrange

       bins - number of bins to use in each dimension

       weights - data-weights

       aspect - aspect ratio

       conditional - normalize each column separately (for probability densities, i.e., cntrmass=True)

       gcf=True does not start a new figure (does change the ranges and labels)

       contours - if False, don't plot contours

       justcontours - if True, only draw contours, no density

       cntrcolors - color of contours (can be array as for bovy_dens2d)

       cntrlw, cntrls - linewidths and linestyles for contour

       cntrSmooth - use ndimage.gaussian_filter to smooth before contouring

       levels - contour-levels; data points outside of the last level will be individually shown (so, e.g., if this list is descending, contours and data points will be overplotted)

       onedhists - if True, make one-d histograms on the sides

       onedhistx - if True, make one-d histograms on the side of the x distribution

       onedhisty - if True, make one-d histograms on the side of the y distribution

       onedhistcolor, onedhistfc, onedhistec

       onedhistxnormed, onedhistynormed - normed keyword for one-d histograms
       
       onedhistxweights, onedhistyweights - weights keyword for one-d histograms

       cmap= cmap for density plot

       hist= and edges= - you can supply the histogram of the data yourself, this can be useful if you want to censor the data, both need to be set and calculated using scipy.histogramdd with the given range

       retAxes= return all Axes instances

    OUTPUT:

       plot to output device, Axes instance(s) or not, depending on input

    HISTORY:

       2010-04-15 - written - Bovy (NYU)
       2019-02-09 - copied & modified - Starkman (Toronto)

    """
    xlabel = kwargs.pop('xlabel', None)
    ylabel = kwargs.pop('ylabel', None)
    if 'xrange' in kwargs:
        xrng = kwargs.pop('xrange')
    else:
        if isinstance(x, list):
            xrng = [np.amin(x), np.amax(x)]
        else:
            xrng = [x.min(), x.max()]
    if 'yrange' in kwargs:
        yrng = kwargs.pop('yrange')
    else:
        if isinstance(y, list):
            yrng = [np.amin(y), np.amax(y)]
        else:
            yrng = [y.min(), y.max()]
    ndata = len(x)
    bins = kwargs.pop('bins', round(0.3 * np.sqrt(ndata)))
    weights = kwargs.pop('weights', None)
    levels = kwargs.pop('levels', special.erf(np.arange(1, 4) / np.sqrt(2.)))
    aspect = kwargs.pop('aspect', (xrng[1] - xrng[0]) / (yrng[1] - yrng[0]))
    conditional = kwargs.pop('conditional', False)
    contours = kwargs.pop('contours', True)
    justcontours = kwargs.pop('justcontours', False)
    cntrcolors = kwargs.pop('cntrcolors', 'k')
    cntrlw = kwargs.pop('cntrlw', None)
    cntrls = kwargs.pop('cntrls', None)
    cntrSmooth = kwargs.pop('cntrSmooth', None)
    onedhists = kwargs.pop('onedhists', False)
    onedhistx = kwargs.pop('onedhistx', onedhists)
    onedhisty = kwargs.pop('onedhisty', onedhists)
    onedhisttype = kwargs.pop('onedhisttype', 'step')
    onedhistcolor = kwargs.pop('onedhistcolor', 'k')
    onedhistfc = kwargs.pop('onedhistfc', 'w')
    onedhistec = kwargs.pop('onedhistec', 'k')
    onedhistls = kwargs.pop('onedhistls', 'solid')
    onedhistlw = kwargs.pop('onedhistlw', None)
    onedhistsbins = kwargs.pop('onedhistsbins', round(0.3 * np.sqrt(ndata)))
    overplot = kwargs.pop('overplot', False)
    gcf = kwargs.pop('gcf', False)
    cmap = kwargs.pop('cmap', cm.gist_yarg)
    onedhistxnormed = kwargs.pop('onedhistxnormed', True)
    onedhistynormed = kwargs.pop('onedhistynormed', True)
    onedhistxweights = kwargs.pop('onedhistxweights', weights)
    onedhistyweights = kwargs.pop('onedhistyweights', weights)
    retAxes = kwargs.pop('retAxes', False)
    if onedhists or onedhistx or onedhisty:
        if overplot or gcf:
            fig = pyplot.gcf()
        else:
            fig = pyplot.figure()
        nullfmt = NullFormatter()         # no labels
        # definitions for the axes
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        bottom_h = left_h = left + width
        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom_h, width, 0.2]
        rect_histy = [left_h, bottom, 0.2, height]
        axScatter = pyplot.axes(rect_scatter)
        if onedhistx:
            axHistx = pyplot.axes(rect_histx)
            # no labels
            axHistx.xaxis.set_major_formatter(nullfmt)
            axHistx.yaxis.set_major_formatter(nullfmt)
        if onedhisty:
            axHisty = pyplot.axes(rect_histy)
            # no labels
            axHisty.xaxis.set_major_formatter(nullfmt)
            axHisty.yaxis.set_major_formatter(nullfmt)
        fig.sca(axScatter)
    data = np.array([x, y]).T
    if 'hist' in kwargs and 'edges' in kwargs:
        hist = kwargs['hist']
        kwargs.pop('hist')
        edges = kwargs['edges']
        kwargs.pop('edges')
    else:
        hist, edges = np.histogramdd(data, bins=bins, range=[xrng, yrng],
                                     weights=weights)
    if contours:
        cumimage = bovy_dens2d(hist.T, contours=contours, levels=levels,
                               cntrmass=contours, cntrSmooth=cntrSmooth,
                               cntrcolors=cntrcolors, cmap=cmap, origin='lower',
                               xrange=xrng, yrange=yrng, xlabel=xlabel,
                               ylabel=ylabel, interpolation='nearest',
                               retCumImage=True, aspect=aspect,
                               conditional=conditional,
                               cntrlw=cntrlw, cntrls=cntrls,
                               justcontours=justcontours,
                               zorder=5 * justcontours,
                               overplot=(gcf or onedhists or overplot or onedhistx or onedhisty))
    else:
        cumimage = bovy_dens2d(hist.T, contours=contours,
                               cntrcolors=cntrcolors,
                               cmap=cmap, origin='lower',
                               xrange=xrng, yrange=yrng, xlabel=xlabel,
                               ylabel=ylabel, interpolation='nearest',
                               conditional=conditional,
                               retCumImage=True, aspect=aspect,
                               cntrlw=cntrlw, cntrls=cntrls,
                               overplot=(gcf or onedhists or overplot or onedhistx or onedhisty))
    #Set axes and labels
    pyplot.axis(list(xrng) + list(yrng))
    if not overplot:
        add_axis_labels(xlabel, ylabel)
        add_minorticks()
    binxs = []
    xedge = edges[0]
    for ii in range(len(xedge) - 1):
        binxs.append((xedge[ii] + xedge[ii + 1]) / 2.)
    binxs = np.array(binxs)
    binys = []
    yedge = edges[1]
    for ii in range(len(yedge)-1):
        binys.append((yedge[ii]+yedge[ii+1])/2.)
    binys = np.array(binys)
    cumInterp = interpolate.RectBivariateSpline(binxs, binys, cumimage.T,
                                                kx=1, ky=1)
    cums = []
    for ii in range(len(x)):
        cums.append(cumInterp(x[ii], y[ii])[0, 0])
    cums = np.array(cums)
    plotx = x[cums > levels[-1]]
    ploty = y[cums > levels[-1]]
    if not len(plotx) == 0:
        if not weights == None:
            w8 = weights[cums > levels[-1]]
            for ii in range(len(plotx)):
                bovy_plot(plotx[ii], ploty[ii], overplot=True,
                          color='%.2f' % (1. - w8[ii]), *args, **kwargs)
        else:
            bovy_plot(plotx, ploty, overplot=True, zorder=1, *args, **kwargs)
    #Add onedhists
    if not (onedhists or onedhistx or onedhisty):
        if retAxes:
            return pyplot.gca()
        else:
            return None
    if onedhistx:
        histx, edges, patches = axHistx.hist(x, bins=onedhistsbins,
                                             normed=onedhistxnormed,
                                             weights=onedhistxweights,
                                             histtype=onedhisttype,
                                             range=sorted(xrng),
                                             color=onedhistcolor, fc=onedhistfc,
                                             ec=onedhistec, ls=onedhistls,
                                             lw=onedhistlw)
    if onedhisty:
        histy, edges, patches = axHisty.hist(y, bins=onedhistsbins,
                                             orientation='horizontal',
                                             weights=onedhistyweights,
                                             normed=onedhistynormed,
                                             histtype=onedhisttype,
                                             range=sorted(yrng),
                                             color=onedhistcolor, fc=onedhistfc,
                                             ec=onedhistec, ls=onedhistls,
                                             lw=onedhistlw)
    if onedhistx and not overplot:
        axHistx.set_xlim(axScatter.get_xlim() )
        axHistx.set_ylim(0, 1.2 * np.amax(histx))
    if onedhisty and not overplot:
        axHisty.set_ylim(axScatter.get_ylim() )
        axHisty.set_xlim(0, 1.2 * np.amax(histy))
    if not onedhistx:
        axHistx = None
    if not onedhisty:
        axHisty = None
    if retAxes:
        return (axScatter, axHistx, axHisty)
    else:
        return None


###############################################################################
# Save and Close

@docstring.Appender(pyplot.savefig.__doc__,
                    join='\n\n{}\n'.format('=' * 78), prededent=True)
def save_and_close(filename, **kw):
    """
    Wrapper for pyplot.savefig
    Calls pyplot.savefig() & pyplot.close()

    Arguments
    ---------
    see savefig docstring
    if format not included, tries to get format from filename

    History
    -------
    2009-12-23 - bovy_end_print written - Bovy (NYU)
    2019-02-08 - written - Starkman (Toronto)
    """

    if 'format' is not None:
        pyplot.savefig(filename, **kw)

    else:
        pyplot.savefig(filename,
                       format=re.split(r'\.', filename)[-1], **kw)
    pyplot.close()


###############################################################################
# Annotation Functions

def add_axis_labels(ax=None, x=None, y=None, z=None, units=False):
    """Add axis labels to given axis

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
            >> from astropy.visualization import quantity_support
            >> quantity_support()

    History
    -------
    2018-10-30 - written - Starkman (Toronto)
    2019-02-09 - modified - Starkman (Toronto) ref bovy_plot._add_axislabels
    """
    # ax = ax if ax is not None else pyplot.gca()

    # if x is not None:
    #     x, xkw = _parselatexstrandopts(x)
    #     if units is True:
    #         x = rf"{x} [{ax.get_xlabel()}]"
    #     ax.set_xlabel(x, **xkw)

    # if y is not None:
    #     y, ykw = _parselatexstrandopts(y)
    #     if units is True:
    #         y = rf"{y} [{ax.get_ylabel()}]"
    #     ax.set_ylabel(y, **ykw)

    # if z is not None:
    #     try:
    #         ax.get_zlabel()
    #     except AttributeError:
    #         pass
    #     else:
    #         z, zkw = _parselatexstrandopts(z)
    #         if units is True:
    #             z = rf"{z} [{ax.get_zlabel()}]"
    #         ax.set_zlabel(z, **zkw)
    axisLabels(ax=ax, x=x, y=y, z=z, units=units)


def add_unit_axis_labels(ax=None, x=None, y=None, z=None):
    """
    """
    add_axis_labels(ax=ax, x=x, y=y, z=z, units=True)


def add_text(ax=None, *args, **kwargs):
    """

    PURPOSE
    -------
       thin wrapper around matplotlib's text and annotate
       use keywords:
          'bottom_left=True'
          'bottom_right=True'
          'top_left=True'
          'top_right=True'
          'title=True'
       to place the text in one of the corners or use it as the title

    INPUT
    -----
    see matplotlib's text
       (http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.text)

    OUTPUT
    ------
    prints text on the current figure

    HISTORY
    -------
    2010-01-26 - written - Bovy (NYU)
    2019-02-09 - copied & modified - Starkman (Toronto)
    """
    ax = ax if ax is not None else pyplot.gca()

    if kwargs.pop('title', False):
        ax.annotate(args[0], (0.5, 1.05),
                    xycoords='axes fraction',
                    horizontalalignment='center', verticalalignment='top',
                    **kwargs)
    elif kwargs.pop('bottom_left', False):
        pyplot.annotate(args[0], (0.05, 0.05),
                        xycoords='axes fraction', **kwargs)
    elif kwargs.pop('bottom_right', False):
        pyplot.annotate(args[0], (0.95, 0.05), xycoords='axes fraction',
                        horizontalalignment='right', **kwargs)
    elif kwargs.pop('top_right', False):
        pyplot.annotate(args[0], (0.95, 0.95),
                        xycoords='axes fraction',
                        horizontalalignment='right', verticalalignment='top',
                        **kwargs)
    elif kwargs.pop('top_left', False):
        pyplot.annotate(args[0], (0.05, 0.95),
                        xycoords='axes fraction', verticalalignment='top',
                        **kwargs)
    else:
        pyplot.text(*args, **kwargs)


###############################################################################
# Plot Property Functions

@mpl_decorator()
def plotproperties(**kw):
    r"""A blanck function for accessing any mpl_decorator property
    __deprecated__
    """
    return None

@mpl_decorator()
def set(**kw):
    r"""A blanck function for accessing any mpl_decorator property
    """
    return None


def add_axis_limits(ax=None, x=None, y=None, z=None):
    r"""
    """

    ax = ax if ax is not None else pyplot.gca()

    if x is not None:
        ax.set_xlim(x)
    if y is not None:
        ax.set_ylim(y)
    if z is not None:
        try:
            ax.set_zlim(z)
        except AttributeError:
            pass


def add_axis_scales(ax=None, x=None, y=None, z=None, **kw):
    r"""
    """
    # ax = ax if ax is not None else pyplot.gca()
    # if x is not None:
    #     ax.set_xscale(x)
    # if y is not None:
    #     ax.set_yscale(y)
    # if z is not None:
    #     try:
    #         ax.set_zscale(z)
    #     except AttributeError:
    #         pass
    axisScales(ax=ax, x=x, y=y, z=z, **kw)


def add_minorticks(ax=None, x=True, y=True, z=True):
    """Add minor ticks

    HISTORY
    -------
       2009-12-23 - _add_ticks written - Bovy (NYU)
       2019-02-099 - written - Starkman (Toronto)
    """
    ax = ax if ax is not None else pyplot.gca()

    if x:
        xstep = ax.xaxis.get_majorticklocs()
        xstep = xstep[1] - xstep[0]
        ax.xaxis.set_minor_locator(MultipleLocator(xstep / 5.))

    if y:
        ystep = ax.yaxis.get_majorticklocs()
        ystep = ystep[1] - ystep[0]
        ax.yaxis.set_minor_locator(MultipleLocator(ystep / 5.))

    if z:
        try:
            zstep = ax.zaxis.get_majorticklocs()
        except AttributeError:
            pass
        else:
            zstep = zstep[1] - zstep[0]
            ax.yaxis.set_minor_locator(MultipleLocator(zstep / 5.))


##############################################################################
# Reference Functions

def plot_help():
    r"""

StarkPlot Plot Additions:
`scatterplot`
`save_and_close`
`add_axis_labels`
`add_unit_axis_labels`
`add_text`
`set`
`add_axis_limits`
`add_axis_limits`
`add_axis_scales`
`add_minorticks`




# TODO get this from pyplot.plotting
Matplotlib's Plotting (accessible via .pyplot):
============================ =============================================================================================================================
Function                     Description
============================ =============================================================================================================================
`acorr`                      Plot the autocorrelation of *x*.
`angle_spectrum`             Plot the angle spectrum.
`annotate`                   Annotate the point *xy* with text *s*.
`arrow`                      Add an arrow to the axes.
`autoscale`                  Autoscale the axis view to the data (toggle).
`axes`                       Add an axes to the current figure and make it the current axes.
`axhline`                    Add a horizontal line across the axis.
`axhspan`                    Add a horizontal span (rectangle) across the axis.
`axis`                       Convenience method to get or set some axis properties.
`axvline`                    Add a vertical line across the axes.
`axvspan`                    Add a vertical span (rectangle) across the axes.
`bar`                        Make a bar plot.
`barbs`                      Plot a 2-D field of barbs.
`barh`                       Make a horizontal bar plot.
`box`                        Turn the axes box on or off on the current axes.
`boxplot`                    Make a box and whisker plot.
`broken_barh`                Plot a horizontal sequence of rectangles.
`cla`                        Clear the current axes.
`clabel`                     Label a contour plot.
`clf`                        Clear the current figure.
`clim`                       Set the color limits of the current image
`close`                      Close a figure window.
`cohere`                     Plot the coherence between *x* and *y*.
`colorbar`                   Add a colorbar to a plot.
`contour`                    Plot contours.
`contourf`                   Plot contours.
`csd`                        Plot the cross-spectral density.
`delaxes`                    Remove the `Axes` *ax* (defaulting to the current axes) from its figure.
`draw`                       Redraw the current figure.
`errorbar`                   Plot y versus x as lines and/or markers with attached errorbars.
`eventplot`                  Plot identical parallel lines at the given positions.
`figimage`                   Add a non-resampled image to the figure
`figlegend`                  Place a legend in the figure.
`fignum_exists`              Return whether the figure with the given id exists.
`figtext`                    Add text to figure.
`figure`                     Create a new figure.
`fill`                       Plot filled polygons.
`fill_between`               Fill the area between two horizontal curves.
`fill_betweenx`              Fill the area between two vertical curves.
`findobj`                    Find artist objects.
`gca`                        Get the current :class:`~matplotlib.axes.Axes` instance on the current figure matching the given keyword args, or create one.
`gcf`                        Get a reference to the current figure.
`gci`                        Get the current colorable artist.
`get_figlabels`              Return a list of existing figure labels
`get_fignums`                Return a list of existing figure numbers.
`grid`                       Configure the grid lines.
`hexbin`                     Make a hexagonal binning plot.
`hist`                       Plot a histogram.
`hist2d`                     Make a 2D histogram plot.
`hlines`                     Plot horizontal lines at each *y* from *xmin* to *xmax*.
`imread`                     Read an image from a file into an array.
`imsave`                     Save an array as in image file.
`imshow`                     Display an image, i.e.
`install_repl_displayhook`   Install a repl display hook so that any stale figure are automatically redrawn when control is returned to the repl.
`ioff`                       Turn the interactive mode off.
`ion`                        Turn the interactive mode on.
`isinteractive`              Return the status of interactive mode.
`legend`                     Place a legend on the axes.
`locator_params`             Control behavior of tick locators.
`loglog`                     Make a plot with log scaling on both the x and y axis.
`magnitude_spectrum`         Plot the magnitude spectrum.
`margins`                    Set or retrieve autoscaling margins.
`matshow`                    Display an array as a matrix in a new figure window.
`minorticks_off`             Remove minor ticks from the axes.
`minorticks_on`              Display minor ticks on the axes.
`pause`                      Pause for *interval* seconds.
`pcolor`                     Create a pseudocolor plot with a non-regular rectangular grid.
`pcolormesh`                 Create a pseudocolor plot with a non-regular rectangular grid.
`phase_spectrum`             Plot the phase spectrum.
`pie`                        Plot a pie chart.
`plot`                       Plot y versus x as lines and/or markers.  ** + many extra options**
`plot_date`                  Plot data that contains dates.
`plotfile`                   Plot the data in a file.
`polar`                      Make a polar plot.
`psd`                        Plot the power spectral density.
`quiver`                     Plot a 2-D field of arrows.
`quiverkey`                  Add a key to a quiver plot.
`rc`                         Set the current rc params.
`rc_context`                 Return a context manager for managing rc settings.
`rcdefaults`                 Restore the rc params from Matplotlib's internal default style.
`rgrids`                     Get or set the radial gridlines on the current polar plot.
`savefig`                    Save the current figure.
`sca`                        Set the current Axes instance to *ax*.
`scatter`                    A scatter plot of *y* vs *x* with varying marker size and/or color.
`sci`                        Set the current image.
`semilogx`                   Make a plot with log scaling on the x axis.
`semilogy`                   Make a plot with log scaling on the y axis.
`set_cmap`                   Set the default colormap.
`setp`                       Set a property on an artist object.
`show`                       Display a figure.
`specgram`                   Plot a spectrogram.
`spy`                        Plot the sparsity pattern of a 2D array
`stackplot`                  Draw a stacked area plot.
`stem`                       Create a stem plot.
`step`                       Make a step plot.
`streamplot`                 Draw streamlines of a vector flow.
`subplot`                    Add a subplot to the current figure.
`subplot2grid`               Create an axis at specific location inside a regular grid.
`subplot_tool`               Launch a subplot tool window for a figure.
`subplots`                   Create a figure and a set of subplots.
`subplots_adjust`            Tune the subplot layout.
`suptitle`                   Add a centered title to the figure.
`switch_backend`             Close all open figures and set the Matplotlib backend.
`table`                      Add a table to the current axes.
`text`                       Add text to the axes.
`thetagrids`                 Get or set the theta gridlines on the current polar plot.
`tick_params`                Change the appearance of ticks, tick labels, and gridlines.
`ticklabel_format`           Change the `~matplotlib.ticker.ScalarFormatter` used by default for linear axes.
`tight_layout`               Automatically adjust subplot parameters to give specified padding.
`title`                      Set a title for the axes.
`tricontour`                 Draw contours on an unstructured triangular grid.
`tricontourf`                Draw contours on an unstructured triangular grid.
`tripcolor`                  Create a pseudocolor plot of an unstructured triangular grid.
`triplot`                    Draw a unstructured triangular grid as lines and/or markers.
`twinx`                      Make a second axes that shares the *x*-axis.
`twiny`                      Make a second axes that shares the *y*-axis.
`uninstall_repl_displayhook` Uninstall the matplotlib display hook.
`violinplot`                 Make a violin plot.
`vlines`                     Plot vertical lines.
`xcorr`                      Plot the cross correlation between *x* and *y*.
`xkcd`                       Turn on `xkcd <https://xkcd.com/>`_ sketch-style drawing mode.
`xlabel`                     Set the label for the x-axis.
`xlim`                       Get or set the x limits of the current axes.
`xscale`                     Set the x-axis scale.
`xticks`                     Get or set the current tick locations and labels of the x-axis.
`ylabel`                     Set the label for the y-axis.
`ylim`                       Get or set the y-limits of the current axes.
`yscale`                     Set the y-axis scale.
`yticks`                     Get or set the current tick locations and labels of the y-axis.
============================ =================================================
    """
    print(plot_help.__doc__)


##############################################################################
