# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 11:34:41 2019

@author: shautala

Python script to draw histogram of selected data column for visualizing data distribution in the data preparation stage.
Data is read from numpy arrays saved in binary format.
"""
import matplotlib.style as mplstyle
mplstyle.use('fast')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def draw_histogram(inputfile,column, noData=""):
    columnForHistogram=column[8:]
    if(noData!=""): #if input contains optional nodata argument
        noData=str(float(noData))
        columnForHistogram=columnForHistogram[(columnForHistogram!=noData)]
    columnForHistogram=columnForHistogram.astype('double')
    columnForHistogram=columnForHistogram[~np.isnan(columnForHistogram)]
    if(len(columnForHistogram)>5000):#if len over threshold: take a smaller sample
        columnForHistogram=np.random.choice(columnForHistogram, 5000)
    sns.set_style('darkgrid')
    plt.style.use('seaborn-darkgrid')
    ax=sns.histplot(columnForHistogram.astype(float),kde=False)
    plt.title(column[7])
    return(ax)