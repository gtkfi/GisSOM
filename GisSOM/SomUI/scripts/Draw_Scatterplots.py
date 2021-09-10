# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 10:40:32 2020

Draw scatterplots from selected columns of som result data.

@author: shautala
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import seaborn as sns
import pickle
import pandas as pd



"""
Load input parameters & do basic setup
Inputs:
1) Model.Output_file_somspace
2) Model.Som_x 
3) Model.Som_y 
4) Model.InputFile 
5) Model.Output_Folder
6) draw_list 

"""

parser = argparse.ArgumentParser(description='Script for generating self organizing maps')
parser.add_argument('--outsomfile',nargs='?',dest="outsomfile", help='Som calculation somspace output text file')
parser.add_argument('--som_x',nargs='?', help='som x dimension')
parser.add_argument('--som_y',nargs='?', help='som y dimension')
parser.add_argument('--input_file',nargs='?', help='Input file(*.lrn)')
parser.add_argument('--dir',nargs='?', help='Input file(*.lrn)')
parser.add_argument('--draw_list', default="", dest="draw_list")
args=parser.parse_args()

outsomfile=args.outsomfile  #som results txt file
somx=int(args.som_x)        #som x parameter
somy=int(args.som_y)        #som y parameter
input_file=args.input_file  #original input file. not necessary for scatterplots?
dir=args.dir                #output directory of GisSOM
draw_list=args.draw_list    #list of columns to use in scatterplots

draw_list=draw_list.split(",")


"""
Declare and initialize variables
"""


with open(dir+"/som.dictionary", 'rb') as som_dictionary_file:
     som_dict = pickle.load(som_dictionary_file)
som_data= np.genfromtxt(outsomfile,skip_header=(1), delimiter=' ')
working_dir=dir#+"/somresults"
dataPrepDir=dir+"/DataPreparation"
dataPrepDir2=dir+"/DataForOriginalPlots/DataPreparation"

som=pd.read_csv(outsomfile, delimiter=' ', header=None)
som_headers=som.iloc[0] 

clusters=int(max(som_data[:,len(som_data[0])-2])+1)
discrete_cmap=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)





"""
Plot scatterplots using som data.
"""

    
print("")
mpl.rcParams.update({'font.size': 12})  
cluster_col=[]

for i in range(0,len(som_data)): 
    cluster_col.append(som_data[i][len(som_data[0])-2]);
cluster_nparray=np.asarray(cluster_col)   
clusters_unique=np.unique(cluster_nparray)
for k in range(len(discrete_cmap)-1,-1,-1):
    if(k not in clusters_unique):
        discrete_cmap.pop(k)
counter=0
for i in range(len(som_data[0])-4,1,-1): 
    if(draw_list[i-2]=="0"):
        som_data=np.delete(som_data,i,1)
        som_headers=som_headers.drop(i)
som_headers=som_headers.reset_index(drop=True)
for i in range(2,len(som_data[0]-1)): 
    
    for k in range(i, len(som_data[0])-4):   
        counter=counter+1   
        ax=sns.scatterplot(x=som_data[:,i].astype(float), y=som_data[:,k+1].astype(float), hue=cluster_nparray.astype(float), palette=discrete_cmap,legend="full")
        ax.set_xlabel(som_headers[i])
        ax.set_ylabel(som_headers[k+1])    
        lgd=ax.legend(bbox_to_anchor=(1, 1),loc=0,fontsize=8 ,borderaxespad=0.8)
        ax.figure.savefig(working_dir+'/Scatterplot/scatterplot_' +str(counter)+'.png', bbox_extra_artists=(lgd,), bbox_inches='tight')    
        plt.clf()
        plt.cla()
        plt.close()
        

print("Scatterplots finished")