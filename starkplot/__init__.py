# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : starkplot initialization file
# AUTHOR  : Nathaniel Starkman
# PROJECT : starkplot
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""Starkplot.

----------------------------------------------------------------------------

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

"""

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = ["matplotlib"]
__license__ = "GPL3"
__version__ = "0.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"

##############################################################################
# IMPORTS

# GENERAL
from matplotlib.pyplot import *
from matplotlib import pyplot

# astropy
from astropy.visualization import quantity_support
from astropy.visualization import astropy_mpl_style

# PROJECT-SPECIFIC

# importing folders
from . import decorators, utils

# Now overwriting
from ._plot import *
from .decorators import mpl_decorator, MatplotlibDecorator

# explicitly import here
from ._figure import (
    figure,
    gcf,
    scf,
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
    savefig,
    save_figure,
    close,
    closefig,
    save_and_close,
)


from ._axes import (
    gca,
    sca,
    get_title,
    set_title,
    get_xlabel,
    set_xlabel,
    get_ylabel,
    set_ylabel,
    get_xlim,
    set_xlim,
    get_ylim,
    set_ylim,
    invert_xaxis,
    invert_yaxis,
    get_xscale,
    set_xscale,
    get_yscale,
    set_yscale,
)


#############################################################################
# CODE

quantity_support()
style.use(astropy_mpl_style)  # using *style* from ._plot

#############################################################################
# END
