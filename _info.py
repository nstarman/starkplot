#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""starkplot _info

#############################################################################

Copyright (c) 2018 - Nathaniel Starkman
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
"""

#############################################################################
# Imports



#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = [""]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"


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
