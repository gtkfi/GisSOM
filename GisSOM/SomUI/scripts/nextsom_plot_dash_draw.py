# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:54:21 2019

@author: Sakari Hautala
Python script to visualize SOM calculation results. Draws only selected cluster/som cell on heatmap, the rest of the data is colorer white/highly transparent. Selecting the cluster or som cell is done in the dash interactive web page (created in nextsomplot_dash script)

DEPRECATED. The whole interactive plot was combined into one dash script in version 1.2.3
"""
#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#import warnings
#with warnings.catch_warnings():
    #warnings.filterwarnings("ignore")
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(0)
import os.path
import argparse
"""
inputs:
1)outSomFile
2)som_x
3)som_y
4)outGeoFile
5)Model.InputFile
6)Model.Output_Folder
7)Interactive selection type (cluster or cell)
8)Selected column (index)
"""

parser = argparse.ArgumentParser(description='Script for drawing resulting plot of interactive selection for csv scatter data')
parser.add_argument('--outsomfile',nargs='?',dest="outsomfile", help='Som calculation somspace output text file')
parser.add_argument('--som_x',nargs='?', dest="som_x", help='som x dimension')
parser.add_argument('--som_y',nargs='?', dest="som_y", help='som y dimension')
parser.add_argument('--outgeofile', dest="outgeofile", default=None, help='#som geospace results txt file')
parser.add_argument('--input_file', dest="input_file", nargs='?', help='Input file(*.lrn)')
parser.add_argument('--dir',nargs='?', dest="dir", help='Output folder')
parser.add_argument('--interactive_type', dest="interactive_type",nargs='?', help='type of interactive selection (som cell or cluster')
parser.add_argument('--selected_column', dest="selected_column",nargs='?', help='Selected data column for plotting')
args=parser.parse_args()

outsomfile=args.outsomfile  
somx=int(args.som_x)       
somy=int(args.som_y)      
input_file=args.input_file  
outgeofile=args.outgeofile
output_folder=args.dir                
interactive_type=args.interactive_type
selected_column=float(args.selected_column)


som_data = np.genfromtxt(outsomfile,skip_header=(1), delimiter=' ')
clusters=int(max(som_data[:,len(som_data[0])-2])+1)
cluster_ticks=[]
if(interactive_type!="Cluster"):
    for i in range (clusters,0,-1):
        cluster_ticks.append(i-1)   
else:
    for i in range (clusters+1,0,-1):
        cluster_ticks.append(i-1)   

geo_data=np.genfromtxt(outgeofile, skip_header=(1), delimiter=' ')
geofile = open(outgeofile, "r")
header_line = geofile.readline()
geo_headers = header_line.split(" ")
pivotted=[]




if(os.path.exists(output_folder+"/clickData2.txt")):
    with open (output_folder+"/clickData2.txt", "r") as clickData:
        selected_x=clickData.readline().replace("\n","")
        selected_y=clickData.readline().replace("\n","")
        selected_z=clickData.readline().replace("\n","")
    if(len(selected_x)==0):
        selected_x="0"
    if(len(selected_y)==0):
        selected_y="0"
    selected_x=float(selected_x)
    selected_y=float(selected_y)
    
    if(interactive_type!="Cluster"):
        if(selected_column==0):  
            for i in range(0, len(geo_data)):
                if(geo_data[i][2]==selected_x and geo_data[i][3]==selected_y):
                    geo_data[i][4]=clusters 
        else:#if selected column is not cluster col, the process will have to be reversed: in case of data col visualization, we can't really modify the continuous palette, so we'll have to set the non-selected areas to NaN:s and show them as white.
            for i in range(0, len(geo_data)):
                if(geo_data[i][2]!=selected_x or geo_data[i][3]!=selected_y):
                    geo_data[i][int(len(som_data[0])-1+selected_column)]=np.NaN
    else:
        if(selected_column>0):  
            for i in range(0, len(geo_data)):
                if(str(int(geo_data[i][4]))!=selected_z):
                    geo_data[i][int((len(som_data[0])-1+selected_column))]=np.NaN
                    
                    
if(max(geo_data[:,(4)])>0): #create dataframe for geospace clusters, if there is more than 1 cluster. 
    x=geo_data[:,0]
    y=geo_data[:,1]
    if(selected_column==0):
        z=geo_data[:,(4)] 
    else:
        z=geo_data[:,int(len(som_data[0])-1+selected_column)]#skip som data values.
    df = pd.DataFrame.from_dict(np.array([x,y,z]).T)
    df.columns = ['X_value','Y_value','Z_value']
    df['Z_value'] = pd.to_numeric(df['Z_value'])
    pivotted= df.pivot('Y_value','X_value','Z_value')





#create palette
palette_2=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
if(interactive_type!="Cluster"):
    palette_2.append([0.00,0.00,0.00,1]);#change this to appending so that the colorscale stays the same 
if(interactive_type=="Cluster"):
    for i in range(0, len(palette_2)):   
        if (str(i)!=selected_z):               
            palette_2[i].append(0.1) #instead of replacing with zero, modify the value to be much closer to zero 
        else:
            palette_2[i].append(1)
else:
    for i in range(0, len(palette_2)): 
        palette_2[i].append(0.1)
        #last palette slot to black
if(interactive_type!="Cluster"):
    palette_2[len(palette_2)-1]=[0.00,0.00,0.00,1] 


        
    
    
if(selected_column==0): #if selected output was cluster:
    if(interactive_type=="Cluster"):    #if selected input was cluster:
        ax=sns.heatmap(pivotted,
                    cmap=palette_2,
                    linewidths=0,
                    vmin=-0.5,
                    vmax=clusters-0.5,
                    square=True,
                    xticklabels="auto",
                    yticklabels="auto",
                    cbar_kws=dict(ticks=cluster_ticks)
        )
    else:  #if selected input was single som cell:
         ax=sns.heatmap(pivotted,
                    cmap=palette_2,
                    linewidths=0,
                    vmin=-0.5,
                    vmax=clusters+0.5,
                    square=True,
                    xticklabels="auto",
                    yticklabels="auto",
                    cbar_kws=dict(ticks=cluster_ticks)
        )
    ax.set_title("Clusters")
else: #if selected output was a data plot:
    palette_2="jet"  
    ax=sns.heatmap(pivotted,
                cmap=palette_2,
                linewidths=0,
                square=True,
                xticklabels="auto",
                yticklabels="auto"
                )
    ax.set_title(geo_headers[int(len(som_data[0])-1+selected_column)])
    
current_cmap = plt.cm.get_cmap()
current_cmap.set_bad(color='white')




fmt = '{:0.0f}'
xticklabels = []
for item in ax.get_xticklabels():
    item.set_text(fmt.format(float(item.get_text())))
    xticklabels += [item]
yticklabels = []
for item in ax.get_yticklabels():
    item.set_text(fmt.format(float(item.get_text())))
    yticklabels += [item]
ax.set_xticklabels(xticklabels)
ax.set_yticklabels(yticklabels)

every_nth = round((len(ax.xaxis.get_ticklabels()))/2)
if(every_nth==0):#temp solution, for data sets with only 1 x coordinate
        every_nth=1
every_nth_y = round((len(ax.yaxis.get_ticklabels()))/2)
if(every_nth_y==0):#temp solution, for data sets with only 1 x coordinate
        every_nth:y=1
for n, label in enumerate(ax.xaxis.get_ticklabels()):
    if n % every_nth != 0:
        label.set_visible(False)
for n, label in enumerate(ax.yaxis.get_ticklabels()):
    if n % every_nth_y != 0:
        label.set_visible(False)

plt.yticks(rotation=90)
plt.yticks(ha='right')
plt.yticks(va='bottom')
plt.xticks(rotation=0)
plt.xticks(ha='left')
ax.invert_yaxis()
plt.tight_layout()
ax.figure.savefig(output_folder+'/somplot_interactive.png', dpi=300)
plt.clf()
plt.close()
     