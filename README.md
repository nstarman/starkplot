# AstroPHD

Welcome to 	`astroPHD`, a collection of useful python codes. This is a centralized repository for much of the non project-specific code I have written or come across. There are modules for making advanced decorators, interfacing with IPython environments, miscellaneous astronomical functions, data utilities, making fitting libraries inter-operable, improving astropy units and quantity-enabled functions, and much more. Check out the documentation here, on [readthedocs](https://readthedocs.org/projects/astrophd/badge/?version=latest), and at the [wiki](https://github.com/nstarman/astroPHD/wiki) for more detail.


[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)
[![Build Status](https://travis-ci.org/nstarman/astroPHD.svg?branch=master)](https://travis-ci.org/nstarman/astroPHD)
[![Documentation Status](https://readthedocs.org/projects/astrophd/badge/?version=latest)](https://astrophd.readthedocs.io/en/latest/?badge=latest)

## Attribution

Author: **Nathaniel Starkman** - *Graduate Student @ UofT* - [website](http://www.astro.utoronto.ca/~starkman/) -- [github](https://github.com/nstarman)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3545178.svg)](https://doi.org/10.5281/zenodo.3545178)

If you find this code useful in your research, please let me know. If you significantly use astroPHD in a publication, please acknowledge **10.5281/zenodo.3545178**. Please also send me a reference to the paper.



##  Table of Contents
<!-- MarkdownTOC levels="1,2,3" autolink="true" style="unordered" -->

- [Module Highlights](#module-highlights)
    - [astronomy](#astronomy)
    - [data_utils](#data_utils)
    - [decorators](#decorators)
    - [fitting](#fitting)
    - [imports](#imports)
    - [ipython](#ipython)
        - [autoreload](#autoreload)
        - [imports](#imports-1)
        - [notebook](#notebook)
        - [plot](#plot)
        - [printing](#printing)
    - [math](#math)
    - [plot](#plot-1)
    - [units](#units)
    - [util](#util)
        - [config file](#config-file)
- [Templates](#templates)
    - [About Text](#about-text)
    - [Python](#python)
    - [Latex](#latex)

<!-- /MarkdownTOC -->


<br><br>
- - -
- - -
<br><br>

<a id="module-highlights"></a>
# Module Highlights
Most of the modules have too much to reasonably document here. These are some of the most useful highlights. Detailed descriptions of everything in `astroPHD` and more can be found at [readthedocs](https://readthedocs.org/projects/astrophd/badge/?version=latest) and at the [wiki](https://github.com/nstarman/astroPHD/wiki).

<a id="astronomy"></a>
## astronomy
> Import using `from  astroPHD import astronomy`


<a id="data_utils"></a>
## data_utils
> Import using `from  astroPHD import data_utils`


<a id="decorators"></a>
## decorators
> Import using `from  astroPHD import decorators`

<a id="fitting"></a>
## fitting
> Import using `from  astroPHD import fitting`


<a id="imports"></a>
## imports
Most of my notebooks or scripts have at leas 30 lines dedicated to just importing the various modules and functions that will be used later. It's cumbersome, a pain to copy between scripts, and means that the code doesn't start until halfway down the screen. This module provides a variety of files that can be `*`-imported to provide all the basic imports so that you can just get started coding.

The provided quick imports are `base`, `extended`, `astropy`, `matplotlib`, `galpy` and `amuse`.

The files will print an import summary. To prevent this summary, set  `verbose-imports=False` in the `.astroPHCrc` config file in your home or local directory. For details on this config file, see [config file](#config-file). Each of the imports also provides a helper function that will print out  the import summary (for instance [base_imports_help](https://astrophd.readthedocs.io/en/latest/astroPHD.imports.html#astroPHD.imports.base.base_imports_help)).


<a id="ipython"></a>
## ipython
> `from  astroPHD import ipython`

This module contains codes for interacting with IPython environments, like Jupyter Notebooks/Lab.

`ipython` does a few things on import:

1. imports:
    ```
    IPython.display display, Latex, Markdown
           .core.interactiveshell: InteractiveShell
                .debugger: set_trace
    astroPHD.ipython.autoreload: set_autoreload, aimport
                    .imports: run_imports, import_from_file
                    .notebook: add_raw_code_toggle
                    .plot: configure_matplotlib
                    .printing: printmd, printMD, printltx, printLaTeX
    ```
2. makes all non-suppressed lines automatically display
    By setting `IPython.InteractiveShell.ast_node_interactivity='all'`.
    Suppressed lines are lines like `> x = func()` or ending with `;`.
    Displayed lines are just like `x`, where 'x' is an existing variable.

3. configures matplotlib to use the 'inline' & 'retina' backends



<a id="autoreload"></a>
### autoreload
> `from  astroPHD.ipython import autoreload`

This module deals with auto-reloading packages / modules / functions in IPython. With IPython auto-reload, specified (or all) packages will be auto-reloaded to check for code changes. While this slows down code execution, it is enormously useful for real-time code development and testing.

The functions are:

-  `.set_autoreload` to set the auto-reload state for packages

- `.aimport`: import with or without auto-reload


<a id="imports-1"></a>
### imports
> `from  astroPHD.ipython import imports`


<a id="notebook"></a>
### notebook
> `from  astroPHD.ipython import imports`

<a id="plot"></a>
### plot

<a id="printing"></a>
### printing


<a id="math"></a>

<a id="math"></a>
## math
> Import using `from  astroPHD import math`


<a id="plot-1"></a>
## plot
> Import using `from  astroPHD import plot`


<a id="units"></a>
## units
> Import using `from  astroPHD import units`


<a id="util"></a>
## util
> Import using `from  astroPHD import util`

<a id="config-file"></a>
### config file


<br><br>
- - -
- - -
<br><br>

<a id="templates"></a>
# Templates
Templates are useful. Here are some.

<a id="about-text"></a>
## About Text
. [About.txt](templates/ABOUT/ABOUT.txt) : an about text in basic `.txt` format
. [About.md](templates/ABOUT/ABOUT.md) : an about text in Markdown

<a id="python"></a>
## Python

. [\_\_init\_\_](templates/python/__init__.py "initialization file")
. [python.py](templates/python/python.py "standard python file")
. [notebook.ipynb](templates/python/notebook.ipynb "standard Jupter Notebook")

<a id="latex"></a>
## Latex

. [tex file](templates/latex/main.tex)
. [bibtex file](templates/latex/main.bib)

**Stylesheets:**
. [main stylesheet](templates/latex/util/main.cls)
. [astronomy stylesheet](templates/latex/util/astronomy.cls)
. [maths stylesheet](templates/latex/util/maths.cls)
. [base stylesheet](templates/latex/util/base.cls)
