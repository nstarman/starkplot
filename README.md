# starkplot
Matplotlib and Plotly functions

This code is in active development and parts are quite likely to change significantly.
I find this code useful for quickly prototyping plots.
For long-term stability, it is recommended to make final plots using just matplotlib or plotly.


## Matplotlib Functions

Easy import:
```python
from matplotlib import pyplot as plt
from starkplot import plot as splt
from starkplot.decorators import mpl_decorator
from starkplot.decorators import MatplotlibDecorator
```

`starkplot.plot` is a wrapper around most plotting functions in `matplotlib.pyplot`.
so instead of doing `plt.plot()`, just use `splt.plot()`
The added capabilities of `splt.plot` are detailed in its docstring

The power of *starkplot* is in `mpl_decorator`, which can be used to decorate any plotting function.
For example:

```python
@mpl_decorator(fig='new', title='untitled', xlabel='x', ylabel='y', xkw={'fontsize': 10})  # <- these are defaults
def myplot(x, y, **kw):  # <- alway's need **kw
  im = plt.scatter(x, y)
  plt.plot(2*x, 2*y)
  ...
  return im  # <- for making colorbars and side histograms

# calling
myplot(x, y, title='plot1', savefig='image.png')  # <- options can be passed here & override the defaults
```

new decorators with preset defaults are easy to make
```python
# making new decorator
new_decorator = MatplotlibDecorator(ax=121, invert_axis='xyz', xlim=(0, 10), title='default title')

@new_decorator
def myplot2(x, y, **kw)
  ...
  
@new_decorator(title='new default title')  # <- overriding properties
def myplot3(x, y, **kw)
  ...
 
# calling
myplot2(x, y, title='plot2', savefig='image2.png')  # <- options can be passed here & override the defaults
myplot3(x, y, title='plot3', savefig='image3.png')  # <- options can be passed here & override the defaults
```
