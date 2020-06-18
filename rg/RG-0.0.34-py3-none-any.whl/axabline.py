# Arbitrary line with intercept and slope

# Acts like axhline or axvline
# Works for 2D plots

import matplotlib.pyplot as plt 
import numpy as np    

def axaline(slope, intercept,style=':r',label='name'):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, style, label=label)
