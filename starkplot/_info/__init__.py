#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _info init
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""

__author__ = "Nathaniel Starkman"


#############################################################################
# Info

_pltypes = (
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
