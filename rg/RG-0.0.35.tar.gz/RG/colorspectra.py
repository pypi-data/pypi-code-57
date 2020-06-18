# Colorspectra: plot X spectra with colorcode defined by y

import numpy as np
import matplotlib.pyplot as plt

def colorspectra(X,y,x_label='wavelength',y_label='intensity',colorbar_label='concentration'):
    '''
    
    Colorspectra: plot X spectra with a colorcode defined by y
    colorspectra(X,y,x_label,y_label,colorbar_label)
    
    INPUT
    X [n x k] <numpy.ndarray>
        spectra
        n samples
        k variables
    Y [n x 1] <numpy.ndarray> 
        spectra
    x_label, y_label, colorbar_label [] <str> 
        optional inputs
        labels of x-axis, y-axis and colorbar
    
    OUTPUT
    none        
    
    '''

    # Plot - color by lines
    [s0,s1]=X.shape
    # Add column listing the original order of y
    order = np.arange(0,s0,1)
    order = (order[np.newaxis]).T
    color = plt.cm.inferno(np.linspace(0,0.9,s0))
    ycolor = np.concatenate((order,y),axis=1)
    # Sort "y" by increasing value
    ycolor=ycolor[np.argsort(ycolor[:,1])]
    # Add colormap
    ycolor = np.concatenate((ycolor,color),axis=1)
    # Sort "order" by increasing value to return to original order
    ycolor=ycolor[np.argsort(ycolor[:,0])]
    # Now the colormap is sorter according to y
    
    # Using contourf to provide my colorbar info, then clearing the figure
    plt.figure()
    mymap = plt.cm.inferno
    Z = [[0,0],[0,0]]
    ymin, ymax = (np.floor(np.min(y)), np.ceil(np.max(y)))
    ymin = int(ymin)
    ymax = int(ymax) 
    levels = np.arange(ymin,ymax,(ymax-ymin)/100)
    CS3 = plt.contourf(Z, levels,cmap=mymap)
    plt.close()
        
    fig = plt.figure()
    for i in range(s0):
        x = X[i,:]
        plt.plot(x.T, color=color[i])
    cbar = plt.colorbar(CS3)
    cbar.set_label(colorbar_label, rotation=270)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel(x_label,fontsize=16)
    plt.ylabel(y_label,fontsize=16)
    plt.show()
    count = int(np.round(1000*np.random.rand(1),0))
    plt.tight_layout()
    #name = 'plot colors'+str(count)+'.png'
    #name = str(name)
    #print(name)
    #fig.savefig('plot colors'+str(count)+'.png',dpi=200)