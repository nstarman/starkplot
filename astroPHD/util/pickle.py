#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : pickle
#
# ----------------------------------------------------------------------------

### Docstring and Metadata
"""functions for making basic pickling easier
"""

__author__ = "Nathaniel Starkman"

#############################################################################
### IMPORTS

import pickle

## Custom
from . import LogPrint

#############################################################################
### PARAMETERS

_LOGFILE = LogPrint(header=False)


#############################################################################
### CODE

def dump(obj, fname, protocol=None, *, fopt='b', fix_imports=True,
         logger=_LOGFILE, verbose=None):
    """wrapper for pickle.dump

    *fname* replaces *file* and is a string for the filename
    this file is auto opened and closed

    pickle.dump documenation
    ------------------------

    Write a pickled representation of obj to the open file object file.

    This is equivalent to ``Pickler(file, protocol).dump(obj)``, but may
    be more efficient.

    The optional *protocol* argument tells the pickler to use the given
    protocol supported protocols are 0, 1, 2, 3 and 4.  The default
    protocol is 3; a backward-incompatible protocol designed for Python 3.

    Specifying a negative protocol version selects the highest protocol
    version supported.  The higher the protocol used, the more recent the
    version of Python needed to read the pickle produced.

    The *file* argument must have a write() method that accepts a single
    bytes argument.  It can thus be a file object opened for binary
    writing, an io.BytesIO instance, or any other custom object that meets
    this interface.

    If *fix_imports* is True and protocol is less than 3, pickle will try
    to map the new Python 3 names to the old module names used in Python
    2, so that the pickle data stream is readable with Python 2.

    """
    logger.verbort(f"dumping obj at {fname}",
                   (f"dumping obj at {fname} with fopt='{'w' + fopt}, "
                    f"protocol=protocol, fix_imports={fix_imports}'"),
                   verbose=verbose)

    with open(fname, 'w' + fopt) as file:
        pickle.dump(obj, file, protocol=protocol, fix_imports=fix_imports)
    return
# /def


# --------------------------------------------------------------------------

def load(fname, *, fopt='b', fix_imports=True, encoding='ASCII',
         errors='strict',
         logger=_LOGFILE, verbose=None):
    """wrapper for pickle.load

    *fname* replaces *file* and is a string for the filename
    this file is auto opened and closed

    pickle.load documenation
    ------------------------

    Read and return an object from the pickle data stored in a file.

    This is equivalent to ``Unpickler(file).load()``, but may be more
    efficient.

    The protocol version of the pickle is detected automatically, so no
    protocol argument is needed.  Bytes past the pickled object's
    representation are ignored.

    The argument *file* must have two methods, a read() method that takes
    an integer argument, and a readline() method that requires no
    arguments.  Both methods should return bytes.  Thus *file* can be a
    binary file object opened for reading, an io.BytesIO object, or any
    other custom object that meets this interface.

    Optional keyword arguments are *fix_imports*, *encoding* and *errors*,
    which are used to control compatibility support for pickle stream
    generated by Python 2.  If *fix_imports* is True, pickle will try to
    map the old Python 2 names to the new names used in Python 3.  The
    *encoding* and *errors* tell pickle how to decode 8-bit string
    instances pickled by Python 2; these default to 'ASCII' and 'strict',
    respectively.  The *encoding* can be 'bytes' to read these 8-bit
    string instances as bytes objects.
    """
    logger.verbort(f"loading obj at {fname}",
                   (f"loading obj at {fname} with fopt='{'r' + fopt}, "
                    f"fix_imports={fix_imports}', encoding={encoding}, "
                    f"errors={errors}"),
                   verbose=verbose)

    with open(fname, 'r' + fopt) as file:
        res = pickle.load(file, fix_imports=fix_imports,
                          encoding=encoding, errors=errors)
    return res
# /def