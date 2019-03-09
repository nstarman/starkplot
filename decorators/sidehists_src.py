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

xlim and ylim from kw if available to the AxesDecorator

just use {_descrargs} in the SideHists docstring and get right indentation level

make xkw be in the docstring depending on whether toplevel or not

"""

#############################################################################
# Imports

import numpy as np
from warnings import warn
import types

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# 3rd Party Imports

try:
    from astropy.utils.decorators import wraps
except ImportError as e:
    print("could not import wraps from astropy. using functools' instead")
    from functools import wraps

# Custom Imports

from ..util import axisLabels, axisScales, axisLimits, invertAxis
# from ..util import _stripprefix, _parseoptsdict, _latexstr, _parselatexstrandopts, _parsestrandopts

from ..docstring import dedent, strthentwoline

from .util import MatplotlibDecoratorBase, _funcdocprefix

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
# Docstring

_descrhead = """
===============================================================================
                         SideHists Decorator Arguments
===============================================================================
these are available as kwargs for {func}(x, y, *args, **kwargs)
"""

_descrargs = """
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
"""

xkwargs = """
xkw: dict
    all the other figure options
    any method (listed below) will first look for a same-named item.
        failing that, it will draw from the general dict, preferring items
        with keys suffixed by the method's name
        order: 1) 'fig'=dict(...)
               2) 'fig_dpi', ...   3) 'dpi', ...
    default: {xkw}
    possible keys:
        # full keys
        # general keys
    used in:
        [*] if options not in argument
    ex:  xkw['_'] = **_ kwargs
         dict(xkw[o] for o in option_names)
"""

_sidehistattrs = (
    # sidehist arguments
    'sidehists',
    'shtype', 'shbins', 'shcolor', 'shfc', 'shec',
    'shxdensity', 'shydensity', 'shxweights', 'shyweights',
    # # modifying arguments
    # 'xkw'
)


#############################################################################
# Decorator

class SideHists(MatplotlibDecoratorBase):
    r"""docstring for SideHists

    call signature::
        SideHists(func=None, funcdoc=None,
                  # sidehist arguments
                  sidehists={sidehists}, shbins={shbins}, shtype={shtype},
                  shcolor={shcolor}, shfc={shfc}, shec={shec}, shxdensity={shxdensity}, shydensity={shydensity}, shxweights={shxweights}, shyweights={shyweights},
                  # modifying arguments
                  xkw={xkw}, kwargs)

    Methods
    -------
    .as_decorator

    Arguments
    ---------
    func:

    funcdoc:

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
        all the other figure options
        any method (listed below) will first look for a same-named item.
            failing that, it will draw from the general dict, preferring items
            with keys suffixed by the method's name
            order: 1) 'fig'=dict(...)
                   2) 'fig_dpi', ...   3) 'dpi', ...
        default: {xkw}
        possible keys:
            # full keys
            # general keys
        used in:
            [*] if options not in argument
        ex:  xkw['_'] = **_ kwargs
             dict(xkw[o] for o in option_names)
    """

    @classmethod
    def as_decorator(cls, func=None, funcdoc=None,
                     # sidehists
                     sidehists=True, shtype='stepfilled',
                     shbins=None, shcolor='k',
                     shfc=None, shec='k',
                     shxdensity=True, shydensity=True,
                     shxweights=None, shyweights=None,
                     # modifying arguments
                     xkw={}):
        r"""SideHists

        Arguments  # TODO fill out text
        ---------
        func:

        funcdoc:

        sidehists: bool
            whether to use sidehists
            default: True
        shtype: str
            ax.hist histtype
            default: 'stepfilled'
        shbins: None, int, array
            ax.hist bins
            default: None
            None uses function args if arg is ndarray, list, or tuple, else shbins=30
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
            all the other figure options
            any method (listed below) will first look for a same-named item.
                failing that, it will draw from the general dict, preferring items
                with keys suffixed by the method's name
                order: 1) 'fig'=dict(...)
                       2) 'fig_dpi', ...   3) 'dpi', ...
            default: empty dict
            possible keys:
                # full keys
                # general keys
            used in:
                [*] if options not in argument
            ex:  xkw['_'] = **_ kwargs
                 dict(xkw[o] for o in option_names)

        Returns
        -------
        decorator if func = None
        decorated function otherwise
        """
        # making instance from base class
        self = super(SideHists, cls).__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            **{k: _locals.get(k).__repr__() for k in set(_sidehistattrs)},
            xkw=xkw
        )

        # init
        self.__init__(
            funcdoc=funcdoc,
            # sidehists
            sidehists=sidehists, shbins=shbins,
            shtype=shtype, shcolor=shcolor,
            shfc=shfc, shec=shec,
            shxdensity=shxdensity, shydensity=shydensity,
            shxweights=shxweights, shyweights=shyweights,
            # modifying arguments
            xkw=xkw
        )
        if func is not None:
            if isinstance(func, type(plt.scatter)):  # scatter doesn't work
                # raise TypeError('plt.scatter does not work')
                pass
            return self(func)
        else:
            return self
    # /def

    def __new__(cls, func=None, funcdoc=None,
                # sidehists
                sidehists=False, shbins=None,
                shtype='stepfilled', shcolor='k',
                shfc=None, shec='k',
                shxdensity=True, shydensity=True,
                shxweights=None, shyweights=None,
                # modifying arguments
                xkw={}, **kw):
        r"""
        important that sidehists defaults to True for combining wrappers
        """
        # making instance from base class
        self = super(SideHists, cls).__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            **{k: _locals.get(k).__repr__() for k in set(_sidehistattrs)}
        )

        # init
        self.__init__(
            funcdoc=funcdoc,
            # sidehists
            sidehists=sidehists, shbins=shbins,
            shtype=shtype, shcolor=shcolor,
            shfc=shfc, shec=shec,
            shxdensity=shxdensity, shydensity=shydensity,
            shxweights=shxweights, shyweights=shyweights,
            # modifying arguments
            xkw={}, **kw
        )

        return self
    # /def

    def __init__(self, func=None, funcdoc=None,
                 # sidehists
                 sidehists=False, shtype='stepfilled', shbins=None,
                 shcolor='k', shfc=None, shec='k',
                 shxdensity=True, shydensity=True,
                 shxweights=None, shyweights=None,
                 # modifying arguments
                 xkw={}, **kw):
        r"""
        """

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

        self.attrs += _sidehistattrs

        self._doc = _descrargs.format(**{k: getattr(self, k).__repr__()
                                         for k in set(self.attrs)})

        if kw.get('_topdecorator', True):
            self._doc += xkwargs.format(xkw=getattr(self, 'xkw').__repr__())

        return
    # /def

    # __call__
    def __call__(self, wrapped_function):

        @wraps(wrapped_function)
        def wrapped(*func_args,
                    # sidehists
                    sidehists=self.sidehists,
                    shtype=self.shtype, shbins=self.shbins,
                    shcolor=self.shcolor, shfc=self.shfc,
                    shec=self.shec,
                    shxdensity=self.shxdensity,
                    shydensity=self.shydensity,
                    shxweights=self.shxweights,
                    shyweights=self.shyweights,
                    # modifying arguments
                    xkw=self.xkw,
                    **func_kwargs):
            # PRE

            # combining dictionaries
            wkw = self.xkw.copy()
            wkw.update(xkw)

            # /PRE
            # CALL

            _res = wrapped_function(*func_args, **func_kwargs)

            # /CALL
            # POST

            # +---- axes ----+
            # Getting current axis for assigning plot properties
            ax = plt.gca()

            # +---- sidehists ----+
            if sidehists:

                ax.set_aspect(1.)  # so same size sidehists

                # create new axes on the right and on the top of the current axes
                # The first argument of the new_vertical(new_horizontal) method is
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

            # Old Method

            # if sidehists:
            #     nullfmt = NullFormatter()         # no labels
            #     # definitions for the axes
            #     # this is directly from bovy_plot
            #     left, width = 0.1, 0.65
            #     bottom, height = 0.1, 0.65
            #     bottom_h = left_h = left + width
            #     rect_scatter = [left, bottom, width, height]
            #     rect_histx = [left, bottom_h, width, 0.2]
            #     rect_histy = [left_h, bottom, 0.2, height]

            #     ax.set_position(rect_scatter)
            #     axHistx = plt.axes(rect_histx)
            #     axHisty = plt.axes(rect_histy)

            #     # no labels
            #     axHistx.xaxis.set_major_formatter(nullfmt)
            #     axHistx.yaxis.set_major_formatter(nullfmt)
            #     axHisty.xaxis.set_major_formatter(nullfmt)
            #     axHisty.yaxis.set_major_formatter(nullfmt)

            # ax.set_autoscale_on(False)

            # # Limits
            # if xlim is None:
            #     arg0 = np.array(func_args[0])
            #     xlim = (arg0.min(), arg0.max())
            # if ylim is None:
            #     arg1 = np.array(func_args[1])
            #     ylim = (arg1.min(), arg1.max())

            # if clim is None:
            #     c = func_kwargs.get('c', None)
            #     if isinstance(c, (list, tuple, np.ndarray)):
            #         clim = (min(c), max(c))
            #     else:
            #         clim = None

            # _res = wrapped_function(*func_args, **func_kwargs)

            # axisLabels(x=xlabel, y=ylabel, units=unit_labels)
            # axisLimits(x=xlim, y=ylim)

            # #Add colorbar
            # if colorbar:
            #     cbar = plt.colorbar(_res, ax=ax)
            #     if clim is not None:
            #         cbar.set_clim(*clim)
            #     if clabel is not None:
            #         cbar.set_label(clabel)

            # # Add onedhists
            # if sidehists:
            #     histx, edges, patches = axHistx.hist(
            #         func_args[0], bins=shbins, density=shxdensity,
            #         weights=shxweights, histtype=shtype,
            #         range=sorted(xlim), color=shcolor, fc=shfc, ec=shec)
            #     histy, edges, patches = axHisty.hist(
            #         func_args[1], bins=shbins, orientation='horizontal',
            #         weights=shyweights, density=shydensity, histtype=shtype,
            #         range=sorted(ylim), color=shcolor, fc=shfc, ec=shec)
            #     axHistx.set_xlim(ax.get_xlim())
            #     axHisty.set_ylim(ax.get_ylim())
            #     axHistx.set_ylim(0, 1.2 * np.amax(histx))
            #     axHisty.set_xlim(0, 1.2 * np.amax(histy))

            return _res
            # /def

        # print('funcdoc:', self.funcdoc)
        # print('descrhead:', _descrhead.format(func=wrapped_function.__name__))
        # print('_doc:', self._doc)

        # modifying wrapped_function docstring
        _doc = (self.funcdoc +
                _descrhead.format(func=wrapped_function.__name__) +
                self._doc)
        wrapped.__doc__ = dedent(wrapped.__doc__) + _doc

        return wrapped
    # /def


###############################################################################

sidehist_decorator = SideHists.as_decorator

###############################################################################
