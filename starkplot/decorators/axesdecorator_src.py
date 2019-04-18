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

# 3rd Party Imports

try:
    from astropy.utils.decorators import wraps
except ImportError as e:
    print("could not import wraps from astropy. using functools' instead")
    from functools import wraps

# Custom Imports
from .util import MatplotlibDecoratorBase, _funcdocprefix

from ..docstring import dedent, strthentwoline
from ..util import prepareAxes, axisLabels, axisLimits, invertAxis, axisScales
from ..util import set_title
from ..util import _parseoptsdict  #, _stripprefix, _latexstr, _parselatexstrandopts, _parsestrandopts



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
                            Axes Decorator Arguments
===============================================================================
these are available as kwargs for {func}()
"""

_descrargs = """
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
stylesheet: None, str
    temporary stylesheet
    default: {stylesheet}
"""

xkwargs = """
xkw: dict
    all the other figure options
    any method (listed below) will first look for a same-named item.
        failing that, it will draw from the general dict, preferring items
        with keys suffixed by the method's name
        order: 1) 'title'=dict(...)
               2) 'title_dpi', ...   3) 'title', ...
    default: {xkw}
    possible keys:
        'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
    used in:
        title[*], xlabel[*], ylabel[*], zlabel[*], xlim, ylim, zlim,
        invert_xaxis, invert_yaxis, invert_zaxis,
        xscale[*], yscale[*], zscale[*],
        [*] if options not in argument
    ex:  xkw['title'] = **title kwargs
         dict(xkw[o] for o in option_names)
"""

_axesattrs = (
    # axes
    'ax',
    'title', 'xlabel', 'ylabel', 'zlabel', 'unit_labels',
    'xlim', 'ylim', 'zlim', 'invert_axis',
    'xscale', 'yscale', 'zscale', 'aspect',
    'legend',
    # style
    'stylesheet',
    # # modifying arguments
    # 'xkw',
)


#############################################################################
# Decorator

class AxesDecorator(MatplotlibDecoratorBase):
    """docstring for AxesDecorator

    call signature::
        AxesDecorator(func=None, funcdoc=None,
                      ax={ax},
                      title={title},
                      xlabel={xlabel}, ylabel={ylabel}, zlabel={zlabel}, unit_labels={unit_labels},
                      xlim={xlim}, ylim={ylim}, zlim={zlim},
                      invert_axis={invert_axis},
                      xscale={xscale}, yscale={yscale}, zscale={zscale},
                      aspect={aspect},
                      legend={legend},
                      # style
                      stylesheet={stylesheet},
                      # modifying arguments
                      xkw={xkw}, **kwargs)

    Methods
    -------
    .as_decorator

    Arguments  # TODO fill out text
    ---------
    func:

    funcdoc:

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
    stylesheet: None, str
        temporary stylesheet
        default: {stylesheet}

    xkw: dict
        all the other axes options
        any method (listed below) will first look for a same-named item.
            failing that, it will draw from the general dict, preferring items
            with keys suffixed by the method's name
            order: 1) 'title'=dict(...)
                   2) 'title_dpi', ...   3) 'title', ...
        default: {xkw}
        possible keys:
            'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
        used in:
            title[*], xlabel[*], ylabel[*], zlabel[*], xlim, ylim, zlim,
            invert_xaxis, invert_yaxis, invert_zaxis,
            xscale[*], yscale[*], zscale[*],
            [*] if options not in argument
        ex:  xkw['title'] = **title kwargs
             dict(xkw[o] for o in option_names)
    """

    __name__ = 'AxesDecorator'

    @classmethod
    def as_decorator(cls, func=None, funcdoc=None,
                     # axes
                     ax=None,
                     title=None,
                     xlabel=None, ylabel=None, zlabel=None, unit_labels=False,
                     xlim=None, ylim=None, zlim=None,
                     invert_axis=None,
                     xscale='linear', yscale='linear', zscale='linear',
                     aspect='auto',
                     legend={},
                     # style
                     stylesheet=None,
                     # modifying arguments
                     xkw={}):
        r"""AxesDecorator

        Arguments  # TODO fill out text
        ---------
        func:

        funcdoc:

        ax: Axes Artist, None, int, False,
            default: None
            uses Axes, gets current axes (if None), makes/gets subplot (at int),
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
        stylesheet: None, str
            temporary stylesheet
            default: None

        xkw: dict
            all the other figure options
            any method (listed below) will first look for a same-named item.
                failing that, it will draw from the general dict, preferring items
                with keys suffixed by the method's name
                order: 1) 'title'=dict(...)
                       2) 'title_dpi', ...   3) 'title', ...
            default: empty dict
            possible keys:
                'fontdict', 'loc', 'pad', anything in matplotlib.text.Text
            used in:
                title[*], xlabel[*], ylabel[*], zlabel[*], xlim, ylim, zlim,
                invert_xaxis, invert_yaxis, invert_zaxis,
                xscale[*], yscale[*], zscale[*],
                [*] if options not in argument
            ex:  xkw['title'] = **title kwargs
                 dict(xkw[o] for o in option_names)

        Returns
        -------
        decorator if func = None
        decorated function otherwise
        """
        # making instance from base class
        self = super(AxesDecorator, cls).__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            **{k: _locals.get(k).__repr__() for k in set(_axesattrs)},
            xkw=xkw
        )

        # init
        self.__init__(
            funcdoc=funcdoc,
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
            # style
            stylesheet=stylesheet,
            # modifying arguments
            xkw=xkw
        )
        if func is not None:
            return self(func)
        else:
            return self
    # /def

    # __new__
    def __new__(cls, func=None, funcdoc=None,
                # axes
                ax=None,
                title=None,
                xlabel=None, ylabel=None, zlabel=None, unit_labels=False,
                xlim=None, ylim=None, zlim=None,
                invert_axis=None,
                xscale='linear', yscale='linear', zscale='linear',
                aspect='auto',
                legend={},
                # style
                stylesheet=None,
                # modifying arguments
                xkw={}, **kw):

        print('called ax __new__')
        # making instance from base class
        self = super(AxesDecorator, cls).__new__(cls)
        print('\t in ax __new__')

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            **{k: _locals.get(k).__repr__() for k in set(_axesattrs)}
        )

        # newfunc = lambda x: func(x, **kw) if func is not None else None

        # init
        self.__init__(
            # func=newfunc,
            funcdoc=funcdoc,
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
            # style
            stylesheet=stylesheet,
            # modifying arguments
            xkw=xkw, **kw
        )
        print('\t in ax __new__')

        # if func is not None:
        #     return self(lambda *args, **kw: func(*args, **kw))
        return self.as_decorator
    # /def

    # __init__
    def __init__(self, func=None, funcdoc=None,
                 # axes
                 ax=None,
                 title=None,
                 xlabel=None, ylabel=None, zlabel=None, unit_labels=False,
                 xlim=None, ylim=None, zlim=None,
                 invert_axis=None,
                 xscale='linear', yscale='linear', zscale='linear',
                 aspect='auto',
                 legend={},
                 # style
                 stylesheet=None,
                 # modifying arguments
                 xkw={}, **kw):

        print('called ax __init__')

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

        # +----------- Documentation -----------+

        self.attrs += _axesattrs

        self._doc = _descrargs.format(**{k: getattr(self, k).__repr__()
                                         for k in set(_axesattrs)})

        if kw.get('_topdecorator', True):
            self._doc += xkwargs.format(xkw=getattr(self, 'xkw').__repr__())

        return
    # /def

    # __call__
    def __call__(self, wrapped_function):

        @wraps(wrapped_function)
        def wrapped(*func_args,
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
                    # styles
                    stylesheet=self.stylesheet,
                    # modifying arguments
                    xkw=self.xkw,
                    **func_kwargs):
            # PRE

            # combining dictionaries
            wkw = self.xkw.copy()
            wkw.update(xkw)

            # +---- figure ----+
            # get current figure
            fig = plt.gcf()

            # +---- axes ----+
            if np.isscalar(ax):

                ax = prepareAxes(ax=ax, fig=fig)

                # /PRE
                # CALL

                func_kwargs['label'] = str(func_kwargs.get('label', ''))  # TODO set in

                if stylesheet is not None:
                    with plt.style.context(stylesheet):
                        return_ = wrapped_function(*func_args, **func_kwargs)
                else:
                    return_ = wrapped_function(*func_args, **func_kwargs)

            else:  # it's a list of axes
                pass
                # for a in ax:
                #     a = prepareAxes(ax=a, fig=fig)
                #
                #     # /PRE
                #     # CALL
                #
                #     if stylesheet is not None:
                #         with plt.style.context(stylesheet):
                #             return_ = wrapped_function(*func_args, **func_kwargs)
                #     else:
                #         return_ = wrapped_function(*func_args, **func_kwargs)

            # /CALL
            # POST

            # +---- axes ----+
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
            if ax is not None:
                if np.isscalar(ax):

                    ax = plt.gca()

                    # set title
                    if title is not None:
                        set_title(title, ax=ax, **wkw)

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

                else:
                    pass
                    # for a in ax:
                    #
                    #     # set title
                    #     if title is not None:
                    #         set_title(title, ax=ax, **wkw)
                    #
                    #     ax.set_aspect(aspect)
                    #
                    #     # setting axisLabels/limits/scales
                    #     axisLabels(ax, x=xlabel, y=ylabel, z=zlabel,
                    #                units=unit_labels, **wkw)
                    #     axisLimits(ax, x=xlim, y=ylim, z=zlim)
                    #
                    #     if invert_axis is not None:
                    #         invertAxis(ax, x='x' in invert_axis, y='y' in invert_axis,
                    #                    z='z' in invert_axis)
                    #
                    #     axisScales(ax, x=xscale, y=yscale, z=zscale, **wkw)
                    #
                    #     # Legend
                    #     handles, labels = ax.get_legend_handles_labels()
                    #     if labels:
                    #         legend = _parseoptsdict(legend)
                    #         ax.legend(handles=handles, labels=labels, **legend)
                    #
                    # plt.sca(ax[0])


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


###############################################################################
# as_decorator

ax_decorator = AxesDecorator.as_decorator

###############################################################################
