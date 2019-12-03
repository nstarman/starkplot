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
Planned Features:

"""

#############################################################################
# Imports

from .._figure import _newfigk, _savefigk, _suptitlek
from .._util import _titlek, _xlabelk, _ylabelk, _zlabelk
from .._util import _cbark


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
# Classes


class MatplotlibDecoratorBase(object):
    """docstring for MatplotlibDecoratorBase
    """

    def __init__(self):
        super().__init__()

        self.attrs = []

        # Keys are just the keys and don't provide a defualt value
        # these are provided by pyplot
        # keys & defaults can be used to override the defualt pyplot values
        # not providing a key is a good wa

        # +------------------- Figure -------------------+

        # keys for a new figure, defaults provided by pyplot
        self._newfigk = _newfigk

        # keys for savefig
        self._savefigk = _savefigk

        # keys for suptitles
        self._suptitlek = _suptitlek

        # +------------------- Axes -------------------+
        self._titlek = _titlek
        self._xlabelk = _xlabelk
        self._ylabelk = _ylabelk
        self._zlabelk = _zlabelk


#############################################################################
# Strings

_funcdocprefix = "\n\n{0}\n{1}Wrapped Function's Documentation\n{0}\n\n".format(
    "=" * 78, " " * 22
)


#############################################################################
# Functions
