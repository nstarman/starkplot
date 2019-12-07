#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : _figure initialization
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""**DOCSTRING**
"""

__author__ = "Nathaniel Starkman"
__credits__ = ["matplotlib"]
# __all__ = ['figure', ]


##############################################################################
### IMPORTS

## General
from ._current_figure import gcf, scf

from ._figure_properties import (
    figure,
    get_figsize,
    set_figsize,
    suptitle,
    supertitle,
    get_suptitle,
    set_suptitle,
    get_supertitle,
    set_supertitle,
    get_dpi,
    set_dpi,
    get_facecolor,
    set_facecolor,
    get_edgecolor,
    set_edgecolor,
    get_frameon,
    set_frameon,
    override_figure,
    tight_layout,
)

from ._info import (  # TODO are these necessary here?
    _newfigk,
    _tightlayoutk,
    _savefigk,
    _suptitlek,
)

from ._save_or_close import (
    savefig,
    save_figure,
    close,
    closefig,
    save_and_close,
)

from .decorators import GetFigArg, SetFigArg
