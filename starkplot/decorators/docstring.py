#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
r"""

    Docstring Functions

#############################################################################

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

#############################################################################
Planned Features
"""

#############################################################################
# Imports

import inspect

from matplotlib import docstring as _docstring

# decorator module
import decorator

#############################################################################
# Info

__author__ = "Nathaniel Starkman"
__copyright__ = "Copyright 2018, "
__credits__ = ["The Matplotlib Team", "Jo Bovy"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Nathaniel Starkman"
__email__ = "n.starkman@mail.utoronto.ca"
__status__ = "Production"

#############################################################################
# Functions

Substitution = _docstring.Substitution

# class Substitution(object):
#     """
#     A decorator to take a function's docstring and perform string
#     substitution on it.

#     This decorator should be robust even if func.__doc__ is None
#     (for example, if -OO was passed to the interpreter)

#     Usage: construct a docstring.Substitution with a sequence or
#     dictionary suitable for performing substitution; then
#     decorate a suitable function with the constructed object. e.g.

#     sub_author_name = Substitution(author='Jason')

#     @sub_author_name
#     def some_function(x):
#         "%(author)s wrote this function"

#     # note that some_function.__doc__ is now "Jason wrote this function"

#     One can also use positional arguments.

#     sub_first_last_names = Substitution('Edgar Allen', 'Poe')

#     @sub_first_last_names
#     def some_function(x):
#         "%s %s wrote the Raven"
#     """

#     def __init__(self, *args, **kwargs):
#         assert not (len(args) and len(kwargs)), \
#                 "Only positional or keyword args are allowed"
#         self.params = args or kwargs

#     def __call__(self, func):
#         func.__doc__ = func.__doc__ and func.__doc__ % self.params
#         return func

#     def update(self, *args, **kwargs):
#         "Assume self.params is a dict and update it with supplied args"
#         self.params.update(*args, **kwargs)

#     @classmethod
#     def from_params(cls, params):
#         """
#         In the case where the params is a mutable sequence (list or
#         dictionary) and it may change before this class is called, one may
#         explicitly use a reference to the params rather than using *args or
#         **kwargs which will copy the values and not reference them.
#         """
#         result = cls()
#         result.params = params
#         return result


class Appender(object):
    """
    A function decorator that will append an addendum to the docstring
    of the target function.

    This decorator should be robust even if func.__doc__ is None
    (for example, if -OO was passed to the interpreter).

    Usage: construct a docstring.Appender with a string to be joined to
    the original docstring. An optional 'join' parameter may be supplied
    which will be used to join the docstring and addendum. e.g.

    add_copyright = Appender("Copyright (c) 2009", join='\n')

    @add_copyright
    def my_dog(has='fleas'):
        "This docstring will have a copyright below"
        pass

    Modifications
    -------------
    added prededent option
    # TODO make robust if func.__doc__ is None
    """

    def __init__(self, addendum, join="", prededent=False):
        self.addendum = addendum
        self.join = join
        self.prededent = prededent

    def __call__(self, func):
        if self.prededent:
            docitems = [inspect.cleandoc(func.__doc__), self.addendum]
        else:
            docitems = [func.__doc__, self.addendum]

        func.__doc__ = func.__doc__ and self.join.join(docitems)
        return func


def strthentwoline(s):
    if s.endswith("\n\n"):
        return s
    elif s.endswith("\n"):
        return s + "\n"
    else:
        return s + "\n\n"


def strorblank(s):
    """return '' if not already string
    """
    return "" if not isinstance(s, str) else s


def cleandoc(docstring):
    """Dedent a docstring (if present)
    if docstring is None, return ''
    """
    return strorblank(docstring and inspect.cleandoc(docstring))


dedentfunc = inspect.cleandoc


copy = _docstring.copy
# def copy(source):
#     "Copy a docstring from another source function (if present)"
#     def do_copy(target):
#         if source.__doc__:
#             target.__doc__ = source.__doc__
#         return target
#     return do_copy

# create a decorator that will house the various documentation that
#  is reused throughout matplotlib
interpd = Substitution()


copy = _docstring.dedent_interpd
# def dedent_interpd(func):
#     """A special case of the interpd that first performs a dedent on
#     the incoming docstring"""
#     return interpd(dedent(func))


copy_dedent = inspect.cleandoc


def wrap_func_keep_orig_sign(
    func,
    sub_func=None,
    doc_pre=None,
    doc_post=None,
    defaults=None,
    module=None,
    addsource=True,
    **attrs
):
    """helper for decorator.FunctionMaker.create

    takes a function and the main function and makes a
    new wrapped function which has the signature of the sub_function
    doc_pre/post allow the sub_func to have it's prefix pre/appended
    """
    if sub_func is None:
        sub_func = func

    doc = cleandoc(doc_pre) + cleandoc(sub_func.__doc__) + cleandoc(doc_post)

    return decorator.FunctionMaker.create(
        func,
        "return f(%(signature)s)",
        dict(f=sub_func),
        doc=doc,
        __wrapped__=sub_func,
        defaults=defaults,
        module=module,
        addsource=addsource,
        **attrs
    )


# /def
