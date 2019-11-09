#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""metaclass to inherit docstrings."""

__credits__ = ["astropy"]


##############################################################################
# IMPORTS

# General
import inspect


##############################################################################
# CODE

class InheritDocstrings(type):
    """Docstring inheritance metaclass.

    This metaclass makes methods of a class automatically have their
    docstrings filled in from the methods they override in the base
    class.
    If the class uses multiple inheritance, the docstring will be
    chosen from the first class in the bases list, in the same way as
    methods are normally resolved in Python.  If this results in
    selecting the wrong docstring, the docstring will need to be
    explicitly included on the method.

    For example::
        >>> from astropy.utils.misc import InheritDocstrings
        >>> class A(metaclass=InheritDocstrings):
        ...     def wiggle(self):
        ...         "Wiggle the thingamajig"
        ...         pass
        >>> class B(A):
        ...     def wiggle(self):
        ...         pass
        >>> B.wiggle.__doc__
        u'Wiggle the thingamajig'

    taken from astropy

    """

    def __init__(cls, name, bases, dct):
        """Set up docstring inheritance."""
        def is_public_member(key):
            return (
                (key.startswith('__') and key.endswith('__') and
                 len(key) > 4) or not key.startswith('_'))
        # /def

        for key, val in dct.items():
            if ((inspect.isfunction(val) or inspect.isdatadescriptor(val)) and
                    is_public_member(key) and
                    val.__doc__ is None):

                for base in cls.__mro__[1:]:
                    super_method = getattr(base, key, None)
                    if super_method is not None:
                        val.__doc__ = super_method.__doc__
                        break
                # /for
        # /for

        super().__init__(name, bases, dct)
    # /def
# /class

##############################################################################
# END
