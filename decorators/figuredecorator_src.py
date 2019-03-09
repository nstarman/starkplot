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

# import numpy as np
from warnings import warn
import types

# from functools import partialmethod

import matplotlib.pyplot as plt

# 3rd Party Imports

try:
    from astropy.utils.decorators import wraps
except ImportError as e:
    print("could not import wraps from astropy. using functools' instead")
    from functools import wraps

# Custom Imports

from ..util import prepareFigure, saveFigure, overrideFigure, setSuptitle, tightLayout

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
                         Figure Decorator Arguments
===============================================================================
these are available as kwargs for {func}()
"""

_descrargs = """
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
        fig, savefig, suptitle
        # general keys
        num, dpi, facecolor, edgecolor, frameon, FigureClass,
        clear, subplotpars, constrained_layout, line_width,
        pad, h_pad, w_pad, rect,
        orientation, portrait, papertype, format, transparent,
        bbox_inches, pad_inches, metadata,
        fontsize, fontweight,
    used in:
        fig, overridefig, suptitle[*], savefig[*], tight_layout[*], savefig[*]
        [*] if options not in argument
        # TODO add more
    ex:  xkw['savefig'] = **savefig kwargs
         dict(xkw[o] for o in option_names)
"""

_figureattrs = (
    # figure
    'fig', 'rtcf',
    'figsize', 'overridefig', 'savefig', 'closefig',
    'suptitle',
    # style
    'stylesheet', 'tight_layout',
    # # modifying arguments
    # 'xkw',
)


#############################################################################
# Decorator

class FigureDecorator(MatplotlibDecoratorBase):
    """docstring for FigureDecorator

    call signature::
        FigureDecorator(func=None, funcdoc=None,
                        fig={fig}, rtcf={rtcf},
                        figsize={figsize}, overridefig={overridefig},
                        savefig={savefig},
                        suptitle={suptitle},
                        # style
                        stylesheet={stylesheet},
                        tight_layout={tight_layout},
                        # modifying arguments
                        xkw={xkw}, **kwargs)

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
            fig, savefig, suptitle
            # general keys
            num, dpi, facecolor, edgecolor, frameon, FigureClass,
            clear, subplotpars, constrained_layout, line_width,
            pad, h_pad, w_pad, rect,
            orientation, portrait, papertype, format, transparent,
            bbox_inches, pad_inches, metadata,
            fontsize, fontweight,
        used in:
            fig, overridefig, suptitle[*], savefig[*], tight_layout[*], savefig[*]
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
                     # style
                     stylesheet=None,
                     tight_layout=False,
                     # modifying arguments
                     xkw={}):
        r"""FigureDecorator

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

        xkw: dict
            all the other figure, axes options
            any method (listed below) will first look for a same-named item.
                failing that, it will draw from the general dict, preferring items
                with keys suffixed by the method's name
                order: 1) 'fig'=dict(...)
                       2) 'fig_dpi', ...   3) 'dpi', ...
            default: empty dict()
            possible keys:
                # full keys
                savefig, suptitle, tight_layout
                # general keys
                num, dpi, facecolor, edgecolor, frameon, FigureClass,
                clear, subplotpars, constrained_layout, line_width,
                pad, h_pad, w_pad, rect,
                orientation, portrait, papertype, format, transparent,
                bbox_inches, pad_inches, metadata,
                fontsize, fontweight,
            used in:
                fig, overridefig, suptitle[*], savefig[*], tight_layout[*], savefig[*]
                [*] if options not in argument
                # TODO add more
            ex:  xkw['savefig'] = **savefig kwargs
                 dict(xkw[o] for o in option_names)

        Returns
        -------
        decorator if func = None
        decorated function otherwise

        TODO
        ----
        get vs pop
        """

        # making instance from base class
        self = super(FigureDecorator, cls).__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            **{k: _locals.get(k).__repr__() for k in set(_figureattrs)},
            xkw=xkw
        )

        # init
        self.__init__(
            funcdoc=funcdoc,
            # figure
            fig=fig, rtcf=rtcf,
            figsize=figsize, overridefig=overridefig,
            savefig=savefig, closefig=closefig,
            suptitle=suptitle,
            # style
            stylesheet=stylesheet,
            tight_layout=tight_layout,
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
                # figure
                fig=None, rtcf=None,
                figsize=None, overridefig=False,
                savefig=False, closefig=False,
                suptitle=None,
                stylesheet=None, tight_layout=True,
                # modifying arguments
                xkw={}, **kw):

        print('called fig __new__')
        # making instance from base class
        self = super(FigureDecorator, cls).__new__(cls)
        print('\t in fig __new__')

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            **{k: _locals.get(k).__repr__() for k in set(_figureattrs)}
        )

        # newfunc = lambda x: func(func=x, **kw) if func is not None else None
        # print('newfunc.__doc__' if newfunc is not None else None)
        # newfunc = lambda *args, **kw: func(*args, **kw)

        # init
        self.__init__(
            # func=newfunc,
            # func=func,
            # funcdoc=newfunc.__doc__ if newfunc is not None else None,
            # figure
            fig=fig, rtcf=rtcf,
            figsize=figsize, overridefig=overridefig,
            savefig=savefig, closefig=closefig,
            suptitle=suptitle,
            # style
            stylesheet=stylesheet,
            tight_layout=tight_layout,
            # modifying arguments
            xkw=xkw, **kw
        )

        print('\t in fig __new__')

        # if func is not None:
        #     return self(lambda *args, **kw: func(*args, **kw))
        return self
    # /def

    # __init__
    def __init__(self, func=None, funcdoc=None,
                 # figure
                 fig=None, rtcf=None,
                 figsize=None, overridefig=False,
                 savefig=False, closefig=False,
                 suptitle=None,
                 # style
                 stylesheet=None, tight_layout=False,
                 # modifying arguments
                 xkw={}, **kw):
        r""""""
        print('called fig __init__')

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

        # +----------- Documentation -----------+

        self.attrs += _figureattrs

        self._doc = _descrargs.format(**{k: getattr(self, k).__repr__()
                                         for k in set(_figureattrs)})

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

            overridefig = True if fig == 'new' else overridefig
            fig, oldfig = prepareFigure(fig=fig, rtcf=rtcf,
                                        figsize=figsize, **wkw)

            # override currrent figure properties
            if overridefig:
                overrideFigure(fig, figsize=figsize, **wkw)

            # set supertitle
            if suptitle is not None:
                setSuptitle(suptitle, fig=fig, **wkw)

            # /PRE
            # CALL

            if stylesheet is not None:
                with plt.style.context(stylesheet):
                    _res = wrapped_function(*func_args, xkw=xkw, **func_kwargs)
            else:
                _res = wrapped_function(*func_args, **func_kwargs)

            # /CALL
            # POST

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

fig_decorator = FigureDecorator.as_decorator

###############################################################################
