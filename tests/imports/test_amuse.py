# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
#
# TITLE   : test_amuse
#
# ----------------------------------------------------------------------------

# Docstring and Metadata
"""test functions for amuse imports."""

__author__ = "Nathaniel Starkman"


##############################################################################
# IMPORTS

# GENERAL
try:
    import amuse
except ImportError:
    _do_amuse_import = False
else:
    _do_amuse_import = True


##############################################################################

def test_import_amuse():
    """Test _inRange."""
    if _do_amuse_import:

        from astroPHD.imports import amuse as imports

        imports.amuse
        imports.lab
        imports.units
        imports.constants
        imports.bridge

    return
# /def


##############################################################################
# END
