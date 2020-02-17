# Visualisation

import numpy as np
import matplotlib.pyplot as plt
    
def plot(plots):
    #Plots any number of ordered series on the same plot.
    plt.figure(figsize=(10,7.5))
    if type(plots[0]) != list and type(plots[0]) != np.ndarray:
        plots = [plots]
    for x in plots:
        plt.plot(x)
    plt.show()
    
def plotstock(real,smooth,name):
    #Plots a specific stock with it's smoothed curve, plus its name.
    plt.figure(figsize=(10,7.5))
    plt.title(name,fontsize=16, fontweight='bold')
    plt.plot(real,'r-', label = 'Real Values')
    plt.plot(smooth, 'b--', label = 'Smoothed Values')
    plt.xlabel('Time (days)',fontsize=14)
    plt.ylabel('Value (€)',fontsize=14)
    plt.legend(fontsize=14)
    plt.show()
    
    