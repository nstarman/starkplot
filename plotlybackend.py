#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Docstring
"""

# Plotly axis template
axis_tpl = dict(
    showgrid=True,
    zeroline=False,
    showline=False,
)

# Matplotlib-style Plotly axis template
mpl_axis_tpl = dict(
    showgrid=True,
    zeroline=True,
    showline=True,
    mirror='all'
)


# modifies a Plotly axis template
def ply_axis(tpl=axis_tpl, **kw):
    """Modifies a Plotly axis template

    tpl: template
    kw: added terms
    """
    return {**tpl, **kw}
