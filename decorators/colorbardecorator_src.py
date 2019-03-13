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

Colorbar Decorator

"""

#############################################################################
# Imports

# import numpy as np
from warnings import warn
import types

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
from .util import MatplotlibDecoratorBase, _funcdocprefix

from ..docstring import dedent, strthentwoline
from ..util import prepareAxes
from ..util import _stripprefix
from ..util import _cbark

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
                         ColorBar Decorator Arguments
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
    all the other colorbar options
    any method (listed below) will first look for a same-named item.
        failing that, it will draw from the general dict, preferring items
        with keys suffixed by the method's name
        order: 1) 'colorbar'=dict(...)
               2) 'colorbar_dpi', ...   3) 'colorbar', ...
    default: {xkw}
    possible keys:
        'use_gridspec', plt.colorbar kwargs
    used in:
        colorbar[*]
        [*] if options not argument
    ex:  xkw['colorbar'] = **colorbar kwargs
         dict(xkw[o] for o in option_names)
"""

_cbarattrs = (
    # axes
    'ax',
    # colorbar arguments
    'colorbar', 'clabel', 'clim', 'cloc',
    # # modifying arguments
    # 'xkw'
)


#############################################################################
# Decorator

class ColorbarDecorator(MatplotlibDecoratorBase):
    """docstring for ColorbarDecorator

    call signature::
        ColorbarDecorator(func=None, funcdoc=None,
                          ax={ax}
                          # colorbar arguments
                          colorbar={colorbar}, clabel={clabel},
                          clim={clim}, cloc={cloc},
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

    xkw: dict
        all the other colorbar options
        any method (listed below) will first look for a same-named item.
            failing that, it will draw from the general dict, preferring items
            with keys suffixed by the method's name
            order: 1) 'colorbar'=dict(...)
                   2) 'colorbar_dpi', ...   3) 'colorbar', ...
        default: {xkw}
        possible keys:
            'use_gridspec', plt.colorbar kwargs
        used in:
            colorbar[*]
            [*] if options not argument
        ex:  xkw['colorbar'] = **colorbar kwargs
             dict(xkw[o] for o in option_names)
    """

    @classmethod
    def as_decorator(cls, func=None, funcdoc=None,
                     # axes
                     ax=None,
                     # colorbar
                     colorbar=True, clabel=None, clim=None, cloc=None,
                     # modifying arguments
                     xkw={}):
        r"""ColorbarDecorator

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

        xkw: dict
            all the other colorbar options
            any method (listed below) will first look for a same-named item.
                failing that, it will draw from the general dict, preferring items
                with keys suffixed by the method's name
                order: 1) 'colorbar'=dict(...)
                       2) 'colorbar_dpi', ...   3) 'colorbar', ...
            default: empty dict
            possible keys:
                'use_gridspec', plt.colorbar kwargs
            used in:
                colorbar[*]
                [*] if options not argument
            ex:  xkw['colorbar'] = **colorbar kwargs
                 dict(xkw[o] for o in option_names)

        Returns
        -------
        decorator if func = None
        decorated function otherwise
        """
        # making instance from base class
        self = super(ColorbarDecorator, cls).__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            **{k: _locals.get(k).__repr__() for k in set(_cbarattrs)},
            xkw=xkw
        )

        self.__init__(
            funcdoc=funcdoc,
            # axes
            ax=ax,
            # colorbar
            colorbar=colorbar, clabel=clabel, clim=clim, cloc=cloc,
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
                # colorbar
                colorbar=False, clabel=None, clim=None, cloc=None,
                # modifying arguments
                xkw={}, **kw):

        # making instance from base class
        self = super(ColorbarDecorator, cls).__new__(cls)

        # modifying docstring
        _locals = locals()
        self.__doc__ = self.__doc__.format(
            **{k: _locals.get(k).__repr__() for k in set(_cbarattrs)}
        )

        self.__init__(
            funcdoc=funcdoc,
            # axes
            ax=ax,
            # colorbar
            colorbar=colorbar, clabel=clabel, clim=clim, cloc=cloc,
            # modifying arguments
            xkw=xkw, **kw
        )

        return self.as_decorator
    # /def

    # __init__
    def __init__(self, func=None, funcdoc=None,
                 # axes
                 ax=None,
                 # colorbar
                 colorbar=False, clabel=None, clim=None, cloc=None,
                 # modifying arguments
                 xkw={}, **kw
                 ):
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

        # +----------- Colorbar -----------+

        self.ax = ax

        # colorbar
        self.colorbar = colorbar
        self.clabel = clabel
        self.clim = clim
        self.cloc = cloc

        # +----------- Documentation -----------+

        self.attrs += _cbarattrs

        self._doc = _descrargs.format(**{k: getattr(self, k).__repr__()
                                         for k in set(_cbarattrs)})

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
                    # colorbar
                    colorbar=self.colorbar, clabel=self.clabel,
                    clim=self.clim, cloc=self.cloc,
                    # modifying arguments
                    xkw=self.xkw,
                    **func_kwargs):
            r"""
            """

            # PRE

            wkw = self.xkw.copy()
            wkw.update(xkw)

            # +---- figure ----+
            # get current figure
            fig = plt.gcf()

            # ax = self._axes(fig, ax)
            ax = prepareAxes(ax=ax, fig=fig)

            # /PRE
            # CALL

            return_ = wrapped_function(*func_args, **func_kwargs)

            # /CALL
            # POST

            # +---- axes ----+
            # Getting current axis for assigning plot properties
            # ax = plt.gca()

            # +---- colorbar ----+
            if colorbar:

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
                    cbar = fig.colorbar(return_, ax=ax, **ckw)
                elif cloc == 'in':
                    cbar = fig.colorbar(return_, cax=ax, **ckw)
                elif cloc == 'out':
                    cbar = fig.colorbar(return_, ax=ax, **ckw)
                elif isinstance(cloc, mpl.axes.Axes):
                    cbar = fig.colorbar(return_, ax=cloc, **ckw)
                # TODO cax in arbitrary axes
                # elif cloc[0] == 'in & isinstance(cloc[1], mpl.axes.Axes):
                #     cbar = fig.colorbar(return_, cax=cloc[1], **ckw)

                if clim is not None:
                    cbar.set_clim(*clim)
                if clabel is not None:
                    cbar.set_label(clabel)

            # /POST
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

cbar_decorator = ColorbarDecorator.as_decorator

###############################################################################
