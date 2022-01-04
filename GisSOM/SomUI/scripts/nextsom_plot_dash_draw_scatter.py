# -*- coding: utf-8 -*-
"""
@author: Sakari Hautala

Python script to visualize SOM calculation results, when input is scatter type. Draws only selected cluster/som cell on heatmap, the rest of the data is colorer white/highly transparent. Selecting the cluster or som cell is done in the dash interactive web page (created in nextsomplot_dash script)

DEPRECATED. The whole interactive plot was combined into one dash script in version 1.2.3
"""

#import warnings
#with warnings.catch_warnings():
    #warnings.filterwarnings("ignore")
import seaborn as sns
import matplotlib.pyplot as plt
#from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import numpy as np#; np.random.seed(0)
#from matplotlib.collections import RegularPolyCollection
import matplotlib as mpl
#import math
#import numpy as np
#from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import ListedColormap
import argparse
from plotting_functions import plot_hexa

"""
inputs:
1)outSomFile
2)som_x
3)som_y
4)outGeoFile
5)Model.InputFile
6)Model.Output_Folder
7)Interactive selection type (cluster or cell)
"""
parser = argparse.ArgumentParser(description='Script for drawing resulting plot of interactive selection for csv scatter data')
parser.add_argument('--outsomfile',nargs='?',dest="outsomfile", help='Som calculation somspace output text file')
parser.add_argument('--som_x',nargs='?', help='som x dimension')
parser.add_argument('--som_y',nargs='?', help='som y dimension')
parser.add_argument('--outgeofile', default=None, dest="outgeofile", help='#som geospace results txt file')
parser.add_argument('--input_file',nargs='?',dest="input_file", help='Input file(*.lrn)')
parser.add_argument('--dir',nargs='?',dest="dir", help='Output folder')
parser.add_argument('--interactive_type',dest="interactive_type",nargs='?', help='type of interactive selection (som cell or cluster')
parser.add_argument('--selected_column',dest="selected_column",nargs='?', help='Selected data column for plotting')
args=parser.parse_args()
#ota ylläolevat sitten käyttöön.

outsomfile=args.outsomfile              #som results txt file
somx=int(args.som_x)                    #som x parameter
somy=int(args.som_y)                    #som y parameter
input_file=args.input_file              #original input file 
outgeofile=args.outgeofile
output_folder=args.dir                  #output directory of GisSOM
interactive_type=args.interactive_type
selected_column=float(args.selected_column)

som_data = np.genfromtxt(outsomfile,skip_header=(1), delimiter=' ')
clusters=int(max(som_data[:,len(som_data[0])-2])+1)
discrete_cmap=sns.cubehelix_palette(n_colors=clusters, start=0, rot=0.4, gamma=1.0, hue=0.8, light=0.85, dark=0.15, reverse=False, as_cmap=False)
discrete_cmap_2=sns.cubehelix_palette(n_colors=clusters, start=0, rot=0.4, gamma=1.0, hue=0.8, light=0.85, dark=0.15, reverse=False, as_cmap=True)
cluster_ticks=[]
cluster_tick_labels=[]
if(interactive_type!="Cluster"):
    for i in range (clusters,0,-1):
        cluster_ticks.append(i-1)   
        cluster_tick_labels.append(str(i-1))
else:
    for i in range (clusters+1,0,-1):
        cluster_ticks.append(i-1)   
        cluster_tick_labels.append(str(i-1))

geo_data=np.genfromtxt(outgeofile, skip_header=(1), delimiter=' ',)
geofile = open(outgeofile, "r")
header_line = geofile.readline()
geo_headers = header_line.split(" ")

with open (output_folder+"/clickData2.txt", "r") as clickData:
    selected_x=clickData.readline()
    selected_y=clickData.readline()
    selected_z=clickData.readline()
selected_x=selected_x.replace("\n","")
selected_y=selected_y.replace("\n","")
selected_z=selected_z.replace("\n","")
if(len(selected_x)==0):
    selected_x="0"
if(len(selected_y)==0):
    selected_y="0"
selected_x=float(selected_x)
selected_y=float(selected_y)
selected_z=selected_z.replace("\n","")


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


palette_2=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
if(interactive_type!="Cluster"):
    palette_2.append([0.00,0.00,0.00,1])#change this to appending so that the colorscale stays the same 
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

centers=[]     
for i in range(0, len(geo_data)):	
    centers.append([geo_data[i][0],geo_data[i][1]])
grid={'centers':np.array(centers), 
      'x':np.array([len(geo_data)]),
      'y':np.array([len(geo_data)])}



if(selected_column==0):
    z=geo_data[:,(4)] 
else:
    z=geo_data[:,int(len(som_data[0])-1+selected_column)]
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
if(clusters>15):
    mpl.rcParams.update({'font.size': 18})  
else:
    mpl.rcParams.update({'font.size': 30})
    
    
if(selected_column==0):
    ax = plot_hexa(somx,somy,clusters+1,grid, z,annot_ticks=cluster_ticks,cluster_tick_labels=cluster_tick_labels,title="Clusters",colmap=ListedColormap(palette_2), ptype='scatter')   
else:
    z = np.ma.array (z, mask=np.isnan(z))
    cmap = mpl.cm.jet
    cmap.set_bad('white',1.)
    ax = plot_hexa(somx,somy,clusters,grid, z,annot_ticks=cluster_ticks,cluster_tick_labels=cluster_tick_labels,title=geo_headers[int(len(som_data[0])-1+selected_column)],colmap="jet", ptype='scatter')   
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
