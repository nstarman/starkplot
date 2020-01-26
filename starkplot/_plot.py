# -*- coding: utf-8 -*-

"""
  starkplot.py: general wrappers for matplotlib plotting

      'public' methods:
            plot

  Methods derived from bovy_plot
        end_print <--- bovy_end_print

TODO
----
- change over to mpl_decorator(func) for all functions which are only
  wrapped and need the funcdocs=func.__doc__ to have their docs

- incorporate the side hists from bovy_plot.bovy_plot into plot
    & do this as a decorator so can attach to functions easily

- switch over to gca() (in a way that respects ax=) so can access 3d plots
  when they happen

"""

#############################################################################
# Imports


## General Imports
from warnings import warn

# matplotlib
# from matplotlib.pyplot import *  # start by importing all of _pyplot
from matplotlib import pyplot as _pyplot  # for usage here


## Project-Specific
from .decorators import mpl_decorator, docstring
from ._util import (
    _parseoptsdict,
    _parsestrandopts,
    _parselatexstrandopts,
    _stripprefix,
    _latexstr,
    axisLabels,
    axisScales,
)

from ._info import _pltypes

# TODO get rid of
# try:
#     from galpy.util import bovy_plot as _bovy_plot
# except Exception as e:
#     print('cannot import galpy.bovy_plot')
# else:
#     from galpy.util.bovy_plot import bovy_dens2d, bovy_plot


# Overwriting for internal use
# TODO use import * b/c have __all__ inside?
# from ._figure import figure, save_and_close
# from ._axes import axes


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


# __all__ = ['']


###############################################################################
# Plotting Functions


@mpl_decorator(funcdoc=_pyplot.plot.__doc__)
def plot(*args, pltype="plot", **kwargs):
    r"""
    pltype:
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
    if pltype == "plot":
        res = _pyplot.plot(*args, **kwargs)

    elif pltype == "scatter":
        res = _pyplot.scatter(*args, **kwargs)

    elif pltype == "errorbar":
        res = _pyplot.errorbar(*args, **kwargs)

    elif pltype == "loglog":
        res = _pyplot.loglog(*args, **kwargs)

    elif pltype == "semilogx":
        res = _pyplot.semilogx(*args, **kwargs)

    elif pltype == "semilogy":
        res = _pyplot.semilogy(*args, **kwargs)

    elif pltype == "hist":
        res = _pyplot.hist(*args, **kwargs)

    # Try all options in _pltypes
    elif pltype in _pltypes:
        res = getattr(_pyplot, pltype)(*args, **kwargs)

    # Permitting any _pyplot function
    elif isinstance(pltype, str):
        try:
            getattr(_pyplot, pltype)
        except Exception as e:
            raise ValueError(f"invalid pltype {pltype}")  #
        else:
            warn("using unsanctioned plotting method")
            getattr(_pyplot, pltype)(*args, **kwargs)
    else:
        raise ValueError(f"invalid pltype {pltype}")

    return res


# /def


@mpl_decorator(funcdoc=_pyplot.acorr.__doc__)
def acorr(*args, **kwargs):
    r"""starkplot wrapper for acorr"""
    return _pyplot.acorr(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.angle_spectrum.__doc__)
def angle_spectrum(*args, **kwargs):
    r"""starkplot wrapper for angle_spectrum"""
    return _pyplot.angle_spectrum(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.axhline.__doc__)
def axhline(*args, **kwargs):
    r"""starkplot wrapper for axhline"""
    return _pyplot.axhline(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.axhspan.__doc__)
def axhspan(*args, **kwargs):
    r"""starkplot wrapper for axhspan"""
    return _pyplot.axhspan(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.axvline.__doc__)
def axvline(*args, **kwargs):
    r"""starkplot wrapper for axvline"""
    return _pyplot.axvline(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.axvspan.__doc__)
def axvspan(*args, **kwargs):
    r"""starkplot wrapper for axvspan"""
    return _pyplot.axvspan(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.bar.__doc__)
def bar(*args, **kwargs):
    r"""starkplot wrapper for bar"""
    return _pyplot.bar(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.barbs.__doc__)
def barbs(*args, **kwargs):
    r"""starkplot wrapper for barbs"""
    return _pyplot.barbs(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.barh.__doc__)
def barh(*args, **kwargs):
    r"""starkplot wrapper for barh"""
    return _pyplot.barh(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.boxplot.__doc__)
def boxplot(*args, **kwargs):
    r"""starkplot wrapper for boxplot"""
    return _pyplot.boxplot(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.broken_barh.__doc__)
def broken_barh(*args, **kwargs):
    r"""starkplot wrapper for broken_barh"""
    return _pyplot.broken_barh(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.cohere.__doc__)
def cohere(*args, **kwargs):
    r"""starkplot wrapper for cohere"""
    return _pyplot.cohere(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.contour.__doc__)
def contour(*args, **kwargs):
    r"""starkplot wrapper for contour"""
    return _pyplot.contour(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.contourf.__doc__)
def contourf(*args, **kwargs):
    r"""starkplot wrapper for contourf"""
    return _pyplot.contourf(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.csd.__doc__)
def csd(*args, **kwargs):
    r"""starkplot wrapper for csd"""
    return _pyplot.csd(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.errorbar.__doc__)
def errorbar(*args, **kwargs):
    r"""starkplot wrapper for errorbar"""
    return _pyplot.errorbar(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.eventplot.__doc__)
def eventplot(*args, **kwargs):
    r"""starkplot wrapper for eventplot"""
    return _pyplot.eventplot(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.figimage.__doc__)
def figimage(*args, **kwargs):
    r"""starkplot wrapper for figimage"""
    return _pyplot.figimage(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.fill.__doc__)
def fill(*args, **kwargs):
    r"""starkplot wrapper for fill"""
    return _pyplot.fill(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.fill_between.__doc__)
def fill_between(*args, **kwargs):
    r"""starkplot wrapper for fill_between"""
    return _pyplot.fill_between(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.fill_betweenx.__doc__)
def fill_betweenx(*args, **kwargs):
    r"""starkplot wrapper for fill_betweenx"""
    return _pyplot.fill_betweenx(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.hexbin.__doc__)
def hexbin(*args, **kwargs):
    r"""starkplot wrapper for hexbin"""
    return _pyplot.hexbin(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.hist.__doc__)
def hist(*args, **kwargs):
    r"""starkplot wrapper for hist"""
    return _pyplot.hist(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.hist2d.__doc__)
def hist2d(*args, **kwargs):
    r"""starkplot wrapper for hist2d"""
    return _pyplot.hist2d(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.hlines.__doc__)
def hlines(*args, **kwargs):
    r"""starkplot wrapper for hlines"""
    return _pyplot.hlines(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.imshow.__doc__)
def imshow(*args, **kwargs):
    r"""starkplot wrapper for imshow"""
    return _pyplot.imshow(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.loglog.__doc__)
def loglog(*args, **kwargs):
    r"""starkplot wrapper for loglog"""
    return _pyplot.loglog(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.magnitude_spectrum.__doc__)
def magnitude_spectrum(*args, **kwargs):
    r"""starkplot wrapper for magnitude_spectrum"""
    return _pyplot.magnitude_spectrum(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.matshow.__doc__)
def matshow(*args, **kwargs):
    r"""starkplot wrapper for matshow"""
    return _pyplot.matshow(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.pcolor.__doc__)
def pcolor(*args, **kwargs):
    r"""starkplot wrapper for pcolor"""
    return _pyplot.pcolor(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.pcolormesh.__doc__)
def pcolormesh(*args, **kwargs):
    r"""starkplot wrapper for pcolormesh"""
    return _pyplot.pcolormesh(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.phase_spectrum.__doc__)
def phase_spectrum(*args, **kwargs):
    r"""starkplot wrapper for phase_spectrum"""
    return _pyplot.phase_spectrum(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.pie.__doc__)
def pie(*args, **kwargs):
    r"""starkplot wrapper for pie"""
    return _pyplot.pie(*args, **kwargs)


# /def


# @mpl_decorator(funcdoc=_pyplot.plot.__doc__)
# def plot(*args, **kwargs):
#     r"""starkplot wrapper for plot"""
#     return _pyplot.plot(*args, **kwargs)# /def


@mpl_decorator(funcdoc=_pyplot.plot_date.__doc__)
def plot_date(*args, **kwargs):
    r"""starkplot wrapper for plot_date"""
    return _pyplot.plot_date(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.plotfile.__doc__)
def plotfile(*args, **kwargs):
    r"""starkplot wrapper for plotfile"""
    return _pyplot.plotfile(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.polar.__doc__)
def polar(*args, **kwargs):
    r"""starkplot wrapper for polar"""
    return _pyplot.polar(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.psd.__doc__)
def psd(*args, **kwargs):
    r"""starkplot wrapper for psd"""
    return _pyplot.psd(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.quiver.__doc__)
def quiver(*args, **kwargs):
    r"""starkplot wrapper for quiver"""
    return _pyplot.quiver(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.rgrids.__doc__)
def rgrids(*args, **kwargs):
    r"""starkplot wrapper for rgrids"""
    return _pyplot.rgrids(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.scatter.__doc__)
def scatter(*args, **kwargs):
    r"""starkplot wrapper for scatter"""
    return _pyplot.gca().scatter(
        *args, **kwargs
    )  # TODO check this works for ax argument


# /def


@mpl_decorator(funcdoc=_pyplot.semilogx.__doc__)
def semilogx(*args, **kwargs):
    r"""starkplot wrapper for semilogx"""
    return _pyplot.semilogx(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.semilogy.__doc__)
def semilogy(*args, **kwargs):
    r"""starkplot wrapper for semilogy"""
    return _pyplot.semilogy(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.specgram.__doc__)
def specgram(*args, **kwargs):
    r"""starkplot wrapper for specgram"""
    return _pyplot.specgram(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.spy.__doc__)
def spy(*args, **kwargs):
    r"""starkplot wrapper for spy"""
    return _pyplot.spy(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.stackplot.__doc__)
def stackplot(*args, **kwargs):
    r"""starkplot wrapper for stackplot"""
    return _pyplot.stackplot(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.stem.__doc__)
def stem(*args, **kwargs):
    r"""starkplot wrapper for stem"""
    return _pyplot.stem(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.step.__doc__)
def step(*args, **kwargs):
    r"""starkplot wrapper for step"""
    return _pyplot.step(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.streamplot.__doc__)
def streamplot(*args, **kwargs):
    r"""starkplot wrapper for streamplot"""
    return _pyplot.streamplot(*args, **kwargs)


# /def


# def table(*args, **kwargs):  # is this an annotation?
#     r"""starkplot wrapper for table"""
#     return _pyplot.table(*args, **kwargs)# /def


@mpl_decorator(funcdoc=_pyplot.tricontour.__doc__)
def tricontour(*args, **kwargs):
    r"""starkplot wrapper for tricontour"""
    return _pyplot.tricontour(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.tricontourf.__doc__)
def tricontourf(*args, **kwargs):
    r"""starkplot wrapper for tricontourf"""
    return _pyplot.tricontourf(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.tripcolor.__doc__)
def tripcolor(*args, **kwargs):
    r"""starkplot wrapper for tripcolor"""
    return _pyplot.tripcolor(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.triplot.__doc__)
def triplot(*args, **kwargs):
    r"""starkplot wrapper for triplot"""
    return _pyplot.triplot(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.violinplot.__doc__)
def violinplot(*args, **kwargs):
    r"""starkplot wrapper for violinplot"""
    return _pyplot.violinplot(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.vlines.__doc__)
def vlines(*args, **kwargs):
    r"""starkplot wrapper for vlines"""
    return _pyplot.vlines(*args, **kwargs)


# /def


@mpl_decorator(funcdoc=_pyplot.xcorr.__doc__)
def xcorr(*args, **kwargs):
    r"""starkplot wrapper for xcorr"""
    return _pyplot.xcorr(*args, **kwargs)


# /def


# TODO this is a replacement for scatterplot
# @mpl_decorator()
# def smartscatter(x, y,
#                  # contour stuff
#                  contours=True, justcontours=True,
#                  bins=None, weights=None, levels=None, aspect=None,
#                  conditional=False,
#                  cntrcolors='k', cntrlw=None, cntrls=None, cntrsmooth=None,
#                  **kw):
#     """"""
#     ndata = len(x)
#     bins = bins if bins is not None else round(0.3 * np.sqrt(ndata))
#     levels = (levels if levels is not None else
#               special.erf(np.arange(1, 4) / np.sqrt(2.)))
#     aspect = (aspect if aspect is not None else
#               (xrng[1] - xrng[0]) / (yrng[1] - yrng[0]))


#     data = np.array([x, y]).T


#     return
# # /def


# def scatterplot(x, y, *args, **kwargs):
#     """ #TODO adapt to starkplot. Can test out my SideHists wrapper
#     NAME:

#        scatterplot

#     PURPOSE:

#        make a 'smart' scatterplot that is a density plot in high-density
#        regions and a regular scatterplot for outliers

#     INPUT:

#        x, y

#        xlabel - (raw string!) x-axis label, LaTeX math mode, no $s needed

#        ylabel - (raw string!) y-axis label, LaTeX math mode, no $s needed

#        xrange

#        yrange

#        bins - number of bins to use in each dimension

#        weights - data-weights

#        aspect - aspect ratio

#        conditional - normalize each column separately (for probability densities, i.e., cntrmass=True)

#        gcf=True does not start a new figure (does change the ranges and labels)

#        contours - if False, don't plot contours

#        justcontours - if True, only draw contours, no density

#        cntrcolors - color of contours (can be array as for bovy_dens2d)

#        cntrlw, cntrls - linewidths and linestyles for contour

#        cntrSmooth - use ndimage.gaussian_filter to smooth before contouring

#        levels - contour-levels; data points outside of the last level will be individually shown (so, e.g., if this list is descending, contours and data points will be overplotted)

#        onedhists - if True, make one-d histograms on the sides

#        onedhistx - if True, make one-d histograms on the side of the x distribution

#        onedhisty - if True, make one-d histograms on the side of the y distribution

#        onedhistcolor, onedhistfc, onedhistec

#        onedhistxnormed, onedhistynormed - normed keyword for one-d histograms

#        onedhistxweights, onedhistyweights - weights keyword for one-d histograms

#        cmap= cmap for density plot

#        hist= and edges= - you can supply the histogram of the data yourself, this can be useful if you want to censor the data, both need to be set and calculated using scipy.histogramdd with the given range

#        retAxes= return all Axes instances# /def

#     OUTPUT:

#        plot to output device, Axes instance(s) or not, depending on input

#     HISTORY:

#        2010-04-15 - written - Bovy (NYU)
#        2019-02-09 - copied & modified - Starkman (Toronto)

#     """
#     from scipy import special, interpolate
#     import matplotlib.cm as cm
#     from matplotlib.ticker import NullFormatter, MultipleLocator

#     xlabel = kwargs.pop('xlabel', None)
#     ylabel = kwargs.pop('ylabel', None)
#     if 'xrange' in kwargs:
#         xrng = kwargs.pop('xrange')
#     else:
#         if isinstance(x, list):
#             xrng = [np.amin(x), np.amax(x)]
#         else:
#             xrng = [x.min(), x.max()]
#     if 'yrange' in kwargs:
#         yrng = kwargs.pop('yrange')
#     else:
#         if isinstance(y, list):
#             yrng = [np.amin(y), np.amax(y)]
#         else:
#             yrng = [y.min(), y.max()]
#     ndata = len(x)
#     bins = kwargs.pop('bins', round(0.3 * np.sqrt(ndata)))
#     weights = kwargs.pop('weights', None)
#     levels = kwargs.pop('levels', special.erf(np.arange(1, 4) / np.sqrt(2.)))
#     aspect = kwargs.pop('aspect', (xrng[1] - xrng[0]) / (yrng[1] - yrng[0]))
#     conditional = kwargs.pop('conditional', False)
#     contours = kwargs.pop('contours', True)
#     justcontours = kwargs.pop('justcontours', False)
#     cntrcolors = kwargs.pop('cntrcolors', 'k')
#     cntrlw = kwargs.pop('cntrlw', None)
#     cntrls = kwargs.pop('cntrls', None)
#     cntrSmooth = kwargs.pop('cntrSmooth', None)
#     onedhists = kwargs.pop('onedhists', False)
#     onedhistx = kwargs.pop('onedhistx', onedhists)
#     onedhisty = kwargs.pop('onedhisty', onedhists)
#     onedhisttype = kwargs.pop('onedhisttype', 'step')
#     onedhistcolor = kwargs.pop('onedhistcolor', 'k')
#     onedhistfc = kwargs.pop('onedhistfc', 'w')
#     onedhistec = kwargs.pop('onedhistec', 'k')
#     onedhistls = kwargs.pop('onedhistls', 'solid')
#     onedhistlw = kwargs.pop('onedhistlw', None)
#     onedhistsbins = kwargs.pop('onedhistsbins', round(0.3 * np.sqrt(ndata)))
#     overplot = kwargs.pop('overplot', False)
#     gcf = kwargs.pop('gcf', False)
#     cmap = kwargs.pop('cmap', cm.gist_yarg)
#     onedhistxnormed = kwargs.pop('onedhistxnormed', True)
#     onedhistynormed = kwargs.pop('onedhistynormed', True)
#     onedhistxweights = kwargs.pop('onedhistxweights', weights)
#     onedhistyweights = kwargs.pop('onedhistyweights', weights)
#     retAxes = kwargs.pop('retAxes', False)
#     if onedhists or onedhistx or onedhisty:
#         if overplot or gcf:
#             fig = _pyplot.gcf()
#         else:
#             fig = _pyplot.figure()
#         nullfmt = NullFormatter()         # no labels
#         # definitions for the axes
#         left, width = 0.1, 0.65
#         bottom, height = 0.1, 0.65
#         bottom_h = left_h = left + width
#         rect_scatter = [left, bottom, width, height]
#         rect_histx = [left, bottom_h, width, 0.2]
#         rect_histy = [left_h, bottom, 0.2, height]
#         axScatter = _pyplot.axes(rect_scatter)
#         if onedhistx:
#             axHistx = _pyplot.axes(rect_histx)
#             # no labels
#             axHistx.xaxis.set_major_formatter(nullfmt)
#             axHistx.yaxis.set_major_formatter(nullfmt)
#         if onedhisty:
#             axHisty = _pyplot.axes(rect_histy)
#             # no labels
#             axHisty.xaxis.set_major_formatter(nullfmt)
#             axHisty.yaxis.set_major_formatter(nullfmt)
#         fig.sca(axScatter)
#     data = np.array([x, y]).T
#     if 'hist' in kwargs and 'edges' in kwargs:
#         hist = kwargs['hist']
#         kwargs.pop('hist')
#         edges = kwargs['edges']
#         kwargs.pop('edges')
#     else:
#         hist, edges = np.histogramdd(data, bins=bins, range=[xrng, yrng],
#                                      weights=weights)
#     if contours:
#         cumimage = bovy_dens2d(hist.T, contours=contours, levels=levels,
#                                cntrmass=contours, cntrSmooth=cntrSmooth,
#                                cntrcolors=cntrcolors, cmap=cmap, origin='lower',
#                                xrange=xrng, yrange=yrng, xlabel=xlabel,
#                                ylabel=ylabel, interpolation='nearest',
#                                retCumImage=True, aspect=aspect,
#                                conditional=conditional,
#                                cntrlw=cntrlw, cntrls=cntrls,
#                                justcontours=justcontours,
#                                zorder=5 * justcontours,
#                                overplot=(gcf or onedhists or overplot or onedhistx or onedhisty))
#     else:
#         cumimage = bovy_dens2d(hist.T, contours=contours,
#                                cntrcolors=cntrcolors,
#                                cmap=cmap, origin='lower',
#                                xrange=xrng, yrange=yrng, xlabel=xlabel,
#                                ylabel=ylabel, interpolation='nearest',
#                                conditional=conditional,
#                                retCumImage=True, aspect=aspect,
#                                cntrlw=cntrlw, cntrls=cntrls,
#                                overplot=(gcf or onedhists or overplot or onedhistx or onedhisty))
#     #Set axes and labels
#     _pyplot.axis(list(xrng) + list(yrng))
#     if not overplot:
#         add_axis_labels(xlabel, ylabel)
#         add_minorticks()
#     binxs = []
#     xedge = edges[0]
#     for ii in range(len(xedge) - 1):
#         binxs.append((xedge[ii] + xedge[ii + 1]) / 2.)
#     binxs = np.array(binxs)
#     binys = []
#     yedge = edges[1]
#     for ii in range(len(yedge)-1):
#         binys.append((yedge[ii]+yedge[ii+1])/2.)
#     binys = np.array(binys)
#     cumInterp = interpolate.RectBivariateSpline(binxs, binys, cumimage.T,
#                                                 kx=1, ky=1)
#     cums = []
#     for ii in range(len(x)):
#         cums.append(cumInterp(x[ii], y[ii])[0, 0])
#     cums = np.array(cums)
#     plotx = x[cums > levels[-1]]
#     ploty = y[cums > levels[-1]]
#     if not len(plotx) == 0:
#         if not weights == None:
#             w8 = weights[cums > levels[-1]]
#             for ii in range(len(plotx)):
#                 bovy_plot(plotx[ii], ploty[ii], overplot=True,
#                           color='%.2f' % (1. - w8[ii]), *args, **kwargs)
#         else:
#             bovy_plot(plotx, ploty, overplot=True, zorder=1, *args, **kwargs)
#     #Add onedhists
#     if not (onedhists or onedhistx or onedhisty):
#         if retAxes:
#             return _pyplot.gca()# /def
#         else:
#             return None# /def
#     if onedhistx:
#         histx, edges, patches = axHistx.hist(x, bins=onedhistsbins,
#                                              normed=onedhistxnormed,
#                                              weights=onedhistxweights,
#                                              histtype=onedhisttype,
#                                              range=sorted(xrng),
#                                              color=onedhistcolor, fc=onedhistfc,
#                                              ec=onedhistec, ls=onedhistls,
#                                              lw=onedhistlw)
#     if onedhisty:
#         histy, edges, patches = axHisty.hist(y, bins=onedhistsbins,
#                                              orientation='horizontal',
#                                              weights=onedhistyweights,
#                                              normed=onedhistynormed,
#                                              histtype=onedhisttype,
#                                              range=sorted(yrng),
#                                              color=onedhistcolor, fc=onedhistfc,
#                                              ec=onedhistec, ls=onedhistls,
#                                              lw=onedhistlw)
#     if onedhistx and not overplot:
#         axHistx.set_xlim(axScatter.get_xlim() )
#         axHistx.set_ylim(0, 1.2 * np.amax(histx))
#     if onedhisty and not overplot:
#         axHisty.set_ylim(axScatter.get_ylim() )
#         axHisty.set_xlim(0, 1.2 * np.amax(histy))
#     if not onedhistx:
#         axHistx = None
#     if not onedhisty:
#         axHisty = None
#     if retAxes:
#         return (axScatter, axHistx, axHisty)# /def
#     else:
#         return None# /def


###############################################################################
# Annotation Functions


def add_axis_labels(ax=None, x=None, y=None, z=None, units=False):
    """Add axis labels to given axis

    Call signature::

      add_axis_labels(ax=None, x=None, y=None, z=None, units=False)

    Parameters
    ---------
    ax: axes or None
        axes instance or None, which will then call _pyplot.gca()
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
       (http://matplotlib.sourceforge.net/api/_pyplot_api.html#matplotlib._pyplot.text)

    OUTPUT
    ------
    prints text on the current figure

    HISTORY
    -------
    2010-01-26 - written - Bovy (NYU)
    2019-02-09 - copied & modified - Starkman (Toronto)
    """
    ax = ax if ax is not None else _pyplot.gca()

    if kwargs.pop("title", False):
        ax.annotate(
            args[0],
            (0.5, 1.05),
            xycoords="axes fraction",
            horizontalalignment="center",
            verticalalignment="top",
            **kwargs,
        )
    elif kwargs.pop("bottom_left", False):
        _pyplot.annotate(
            args[0], (0.05, 0.05), xycoords="axes fraction", **kwargs
        )
    elif kwargs.pop("bottom_right", False):
        _pyplot.annotate(
            args[0],
            (0.95, 0.05),
            xycoords="axes fraction",
            horizontalalignment="right",
            **kwargs,
        )
    elif kwargs.pop("top_right", False):
        _pyplot.annotate(
            args[0],
            (0.95, 0.95),
            xycoords="axes fraction",
            horizontalalignment="right",
            verticalalignment="top",
            **kwargs,
        )
    elif kwargs.pop("top_left", False):
        _pyplot.annotate(
            args[0],
            (0.05, 0.95),
            xycoords="axes fraction",
            verticalalignment="top",
            **kwargs,
        )
    else:
        _pyplot.text(*args, **kwargs)


###############################################################################
# Plot Property Functions


@mpl_decorator()
def plotproperties(**kw):
    r"""A blanck function for accessing any mpl_decorator property
    __deprecated__
    """
    return None


# /def


@mpl_decorator(overridefig=True)
def set(**kw):
    r"""A blanck function for accessing any mpl_decorator property
    """
    return None


# /def


def add_axis_limits(ax=None, x=None, y=None, z=None):
    r"""
    """

    ax = ax if ax is not None else _pyplot.gca()

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
    # ax = ax if ax is not None else _pyplot.gca()
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
    ax = ax if ax is not None else _pyplot.gca()

    if x:
        xstep = ax.xaxis.get_majorticklocs()
        xstep = xstep[1] - xstep[0]
        ax.xaxis.set_minor_locator(MultipleLocator(xstep / 5.0))

    if y:
        ystep = ax.yaxis.get_majorticklocs()
        ystep = ystep[1] - ystep[0]
        ax.yaxis.set_minor_locator(MultipleLocator(ystep / 5.0))

    if z:
        try:
            zstep = ax.zaxis.get_majorticklocs()
        except AttributeError:
            pass
        else:
            zstep = zstep[1] - zstep[0]
            ax.yaxis.set_minor_locator(MultipleLocator(zstep / 5.0))


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




# TODO get this from _pyplot.plotting
Matplotlib's Plotting (accessible via ._pyplot):
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
