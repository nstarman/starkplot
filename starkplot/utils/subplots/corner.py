#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : functions for shaped subplots grids
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
r"""functions for corner plots

adapted from code provided by James Lane

TODO
make this work more closely with the corner package
make a function which returns the axis grid and necessary info to make the plot
make this work with bovy_plot scatterplot
"""

__author__ = "Nathaniel Starkman"

##############################################################################
### IMPORTS

## General
import numpy as np
from scipy import stats
from itertools import product as iter_product

from matplotlib import pyplot

## Project-Specific
from ...decorators import mpl_decorator


##############################################################################


def _type_of_plot(orientation, n_var, i, j):
    """internal helper function for determining plot type in a corner plot

    Parameters
    ----------
    orientation : str
        the orientation
        options: 'lower left', 'lower right', 'upper left', 'upper right'
    i, j : int
        the row, column index

    Returns
    -------
    plot type : str
        'remove' : do not show this plot
        'same' : the axes are the same
        'compare' : compare the two different axes
    """
    if orientation == "lower left":
        if j > i:
            return i, j, "remove"
        elif j == i:
            return i, j, "same"
        else:  # j < i
            return i, j, "compare"

    elif orientation == "lower right":
        raise ValueError("not yet supported orientation")
        # if i + j < n_var - 1:
        #     return i, j, 'remove'
        # elif i + j == n_var - 1:
        #     return i, j, 'same'
        # else:  # j < i
        #     return i, j, 'compare'

    elif orientation == "upper left":
        raise ValueError("not yet supported orientation")
        # if i + j < n_var - 1:
        #     return i, j, 'compare'
        # elif i + j == n_var - 1:
        #     return i, j, 'same'
        # else:  # j < i
        #     return i, j, 'remove'

    elif orientation == "upper right":
        raise ValueError("not yet supported orientation")
        # if j < i:
        #     return i, j, 'remove'
        # elif j == i:
        #     return i, j, 'same'
        # else:  # j < i
        #     return i, j, 'compare'
    else:
        raise ValueError("not supported orientation")


# /def


# Staircase plotting function
def corner_plot(
    data,
    data_labels=None,
    orientation="lower left",
    draw_contours=False,
    fig=None,
    axs=None,
    savefig=False,
    **kw
):
    """corner_plot

    Take in N variables in M samples and plot their correlations.

    Parameters
    ----------
    data : (mxn) array
        The input data. The first axis should be the sample
        number and the second axis should be the variable
    data_labels : (length n array)
        the variable labels
    orientation : str
        the orientation about which this is `centered'
        options: 'lower left', 'lower right', 'upper left', 'upper right'
    fig : matplotlib Figure, optional
        The input figure to plot on.
        If None then make one
    axs : matplotlib axes ndarray, optional
        The input axis to plot on.
        If None then make one
    **kw : passed to correlation plots

    Returns
    -------
    fig : Figure
        matplotlib figure
    axs : Axes array
        array of matplotlib axes
    """

    # Figure out the number of variables
    n_var = len(data[0, :])

    if data_labels is None:
        data_labels = ["q " + i + 1 for i in range(n_var)]

    # Check if the figure was provided
    if fig is None:
        fig = pyplot.figure(figsize=(int(n_var + 3), int(n_var + 3)))
    # /if
    if axs is None:
        axs = fig.subplots(nrows=n_var, ncols=n_var)
    # /if

    # loop over the number of variables
    # i = index along columns (down)
    # j = index along rows (across)
    for i, j in iter_product(range(n_var), range(n_var)):

        i, j, plot_type = _type_of_plot(orientation, n_var, i, j)

        # Maxima and minima
        xmin = np.min(data[:, j])
        xmax = np.max(data[:, j])
        ymin = np.min(data[:, i])
        ymax = np.max(data[:, i])

        # If this is an upper-right plot it is a duplicate, remove it
        if plot_type == "remove":
            axs[i, j].set_axis_off()
            continue

        # If the two indices are equal just make a histogram of the data
        elif plot_type == "same":

            # Make and plot the kernel
            kernel = stats.gaussian_kde(data[:, i])
            kernel_grid = np.linspace(
                np.min(data[:, i]), np.max(data[:, i]), 1000
            )
            kernel_evaluate = kernel.evaluate(kernel_grid)
            axs[i, j].plot(kernel_grid, kernel_evaluate, color="Black")

            # Decorate
            axs[i, j].set_xlim(np.min(data[:, i]), np.max(data[:, i]))
            axs[i, j].tick_params(labelleft=False, labelright=True)
            axs[i, j].set_ylabel("KDE")
            axs[i, j].yaxis.set_label_position("right")

        # If the two indices are not equal make a scatter plot
        elif plot_type == "compare":

            if draw_contours:

                # Make the 2D gaussian KDE
                xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
                positions = np.vstack([xx.ravel(), yy.ravel()])
                values = np.vstack([data[:, j], data[:, i]])
                kernel = stats.gaussian_kde(values)
                kernel_evaluate = np.reshape(kernel(positions).T, xx.shape)

                # Make contours out of the KDE
                cfset = axs[i, j].contourf(
                    xx, yy, kernel_evaluate, cmap="Blues"
                )
                cset = axs[i, j].contour(
                    xx, yy, kernel_evaluate, colors="Black"
                )

                # Decorate
                axs[i, j].set_xlim(xmin, xmax)
                axs[i, j].set_ylim(ymin, ymax)

            else:  # no contours

                axs[i, j].scatter(data[:, j], data[:, i], **kw)
            # /if
        # /if

        # Make X axis
        if i == n_var - 1:
            axs[i, j].set_xlabel(data_labels[j])
        else:
            axs[i, j].tick_params(labelbottom=False)
        # /if

        # Make Y axis
        if (j == 0) and (i != 0):
            axs[i, j].set_ylabel(data_labels[i])
        else:
            axs[i, j].tick_params(labelleft=False)
        # /if
    # /for

    # TODO replace by proper starkplot functions
    if isinstance(savefig, str):
        fig.savefig(savefig)

    return fig, axs


# /def


# --------------------------------------------------------------------------


def staircase_plot(
    data,
    data_labels=None,
    draw_contours=False,
    fig=None,
    axs=None,
    savefig=False,
    **kw
):
    """staircase_plot

    Take in N variables in M samples and plot their correlations.

    Parameters
    ----------
    data : (mxn) array
        The input data. The first axis should be the sample
        number and the second axis should be the variable
    data_labels : (length n array)
        the variable labels
    fig : matplotlib Figure, optional
        The input figure to plot on.
        If None then make one
    axs : matplotlib axes ndarray, optional
        The input axis to plot on.
        If None then make one

    Returns
    -------
    fig : Figure
        matplotlib figure
    axs : Axes array
        array of matplotlib axes
    """
    return corner_plot(
        data,
        data_labels=data_labels,
        draw_contours=draw_contours,
        fig=fig,
        axs=axs,
        savefig=savefig,
        orientation="lower left",
        **kw
    )


##############################################################################
# End
