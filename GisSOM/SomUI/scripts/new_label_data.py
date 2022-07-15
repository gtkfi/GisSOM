# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 10:41:12 2021

Python script used to add new label data to existing dataset, and draw a 
@author: shautala
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import seaborn as sns
import pandas as pd
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, VPacker 
from loadfile import read_header
import math
from plotting_functions import plot_hexa

parser = argparse.ArgumentParser(description='Script for drawing plots from self organizing maps')
parser.add_argument('--outsomfile',nargs='?',dest="outsomfile", help='Som calculation somspace output text file')
parser.add_argument('--som_x',nargs='?', help='som x dimension')
parser.add_argument('--som_y',nargs='?', help='som y dimension')
parser.add_argument('--input_file',nargs='?', help='Input file(*.lrn)')
parser.add_argument('--dir',nargs='?', help='Input file(*.lrn)')
parser.add_argument('--original_data_dir', default=None, dest="original_data_dir", help='location of input columns with original data')
parser.add_argument('--grid_type',nargs='?', help='grid type (square or hexa)')
parser.add_argument('--outgeofile', default=None, dest="outgeofile", help='#som geospace results txt file')
parser.add_argument('--labelIndex', default=None, dest="labelIndex", help='index of label column')
parser.add_argument('--newLabelData', default=None, dest="newLabelData", help='index of label column')
args=parser.parse_args()

outsomfile=args.outsomfile 
outgeofile=args.outgeofile
somx=int(args.som_x)        
somy=int(args.som_y)        
input_file=args.input_file  
working_dir=args.dir                
grid_type=args.grid_type    
newLabelData=args.newLabelData 




"""Declare and initialize variables"""


som_data= np.genfromtxt(outsomfile,skip_header=(1), delimiter=' ')

som=pd.read_csv(outsomfile, delimiter=' ', header=None)
som_headers=som.iloc[0] 
if outgeofile is not None:
    geo_data=np.genfromtxt(outgeofile, skip_header=(1), delimiter=' ')
som_table=np.zeros((somx,somy))



if(input_file[-3:].lower()=="lrn"):     
    header=read_header(input_file)  
    actualNumberOfColumns=header['cols']-1         
else:
    actualNumberOfColumns=len(som_headers)-3

#Generate colormaps and ticks for clustering
clusters=int(max(som_data[:,len(som_data[0])-2])+1)
discrete_cmap=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
discrete_cmap_2=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=True)
cluster_ticks=[]
cluster_tick_labels=[]
cluster_hit_count=[]
for i in range (clusters,0,-1):
    cluster_ticks.append(i-1)   
    
    if outgeofile is not None:
        cluster_tick_labels.append(str(i-1)+ "   " +str(geo_data[:,(4)].tolist().count(i-1))) 
        cluster_hit_count.append(geo_data[:,(4)].tolist().count(i-1))
    else: 
        cluster_tick_labels.append(str(i-1)+ "   " +str(som_data[:,len(som_data[0])-2].tolist().count(i))) 
                      

#generate grid for hexagonal input
grid={}
centers=[]
if(grid_type.lower()=="hexagonal"):
    x=somx
    y=somy
    base_y=math.sqrt(3)/2

    for i in range(0, x):	
        for j in range(0, y):
            if (j%2==0):
                base_x=0
                
            else:
                base_x=0.5
            centers.append([(i+1)+base_x,(j+1)*base_y])#+1 to convert from index to value

    grid={'centers':np.array(centers), 
          'x':np.array([float(x)]),
          'y':np.array([float(y)])}



"""
Calculate best matching som cell for new data, using euclidian distance of data values to existing data points
"""
def create_annotations():
    global annot_strings
    global annot_strings_for_dict
    global data 
    global outfile

    #bmus=som_dict["bmus"]
    counter=1
    euclid_dist_of_single_row=[]
    min_val=-1
    som_x=0
    som_y=0
    #calculate euclid distance
    for k in range(1,len(data)):
        for j in range(0,len(geo_data)):
            for l in range(0, len(som_data[0])-5):        
                euclid_dist_of_single_row.append((float(data[k][l+5])-float(geo_data[j][(len(som_data[0])+l)]))**2) 
            euclid_dist_of_single_row_sum=math.sqrt(sum(euclid_dist_of_single_row))  
            if(min_val<0):
                min_val=euclid_dist_of_single_row_sum
                #min_index=i
                som_x=geo_data[j][2]
                som_y=geo_data[j][3]
            else:
                if(euclid_dist_of_single_row_sum<min_val):
                    min_val=euclid_dist_of_single_row_sum
                    #min_index=i
                    som_x=geo_data[j][2]
                    som_y=geo_data[j][3]
            euclid_dist_of_single_row.clear()   
        min_val=-1
    
        tick=annot_ticks[int(som_x)][int(som_y)]       
        if (tick==''):  # Checks if there are other labels. if tick label is empty:
            annot_ticks[int(som_x)][int(som_y)]=str(counter)    
            annot_strings[str(counter)]=[outfile[k-1]]
            annot_strings_for_dict[str(counter)]=[outfile[k-1]]
            counter=counter+1
        else:   #tick label already contains stuff
            annot_strings[tick].append(outfile[k-1])
            annot_strings_for_dict[tick].append(outfile[k-1])
    
                    
    for i in range(1, len(annot_strings_for_dict)+1): 
        annot_strings_for_dict[str(i)].sort()
        
    #merge duplicates:         
    for i in range(1, len(annot_strings_for_dict)+1):
        for j in range(1, len(annot_strings_for_dict)+1):
            if ((i!=j) and annot_strings_for_dict[str(i)]==annot_strings_for_dict[str(j)]):	
                if(str(i) in annot_strings):
                    annot_strings.pop(str(j))
                for a in range(0,len(annot_ticks)):
                    for b in range(0,len(annot_ticks[a])):
                        if(annot_ticks[a][b]==str(i)):
                            annot_ticks[a][b]=str(j)	     
                            
    #remove gaps in index numbers:                        
    counter=0
    for i in range (1, len(annot_strings_for_dict)+1): 
        if str(i) in annot_strings:
            counter=counter+1
            annot_strings[str(counter)] = annot_strings.pop(str(i)) 
            for a in range(0,len(annot_ticks)):
                for b in range(0,len(annot_ticks[a])):
                    if(annot_ticks[a][b]==str(i)):
                        annot_ticks[a][b]=counter	
    #format ticks:
    for i in range(1,len(annot_strings)+1):
        annot_strings[str(i)]=str(i)+": "+ ','.join(annot_strings[str(i)])



"""
Draw Som Cluster plot
"""
def draw_som_clusters():
    global som_data
    global som_table
    global annot_ticks
    global som_headers
    global grid
    global centers
    if(grid_type.lower()=="rectangular"):
        mpl.rcParams.update({'font.size': 14})  
        for i in range(0,len(som_data)): 
            som_table[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][len(som_data[0])-2]
        ax = sns.heatmap(som_table.transpose(), cmap=discrete_cmap, linewidth=0, vmin=-0.5, vmax=clusters-0.5, center=clusters/2-0.5, cbar_kws=dict(ticks=cluster_ticks), annot=annot_ticks.transpose(), fmt = '')
        colorbar = ax.collections[0].colorbar
        colorbar.set_ticklabels(cluster_tick_labels)
        ax.set_title(som_headers[len(som_headers)-1])
    else:
        hits=som_data[:,len(som_data[0])-2]   
        mpl.rcParams.update({'font.size': 30})  
        ax = plot_hexa(somx,somy,clusters,grid, hits,annot_ticks,cluster_tick_labels,colmap=discrete_cmap_2, ptype='grid')
        mpl.rcParams.update({'font.size': 32})  
        ax.set_title(som_headers[len(som_headers)-1])
        mpl.rcParams.update({'font.size': 30})  
    #ax.set_title(som_headers[len(som_headers)-1])
    #plt.tight_layout()
    ax.figure.savefig(working_dir+'/Som/cluster_new.png',bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()
    
    mpl.rcParams.update({'font.size': 12})  
    #fig = plt.figure()
    fig = plt.figure(figsize= [6.4, 4.8])
    ax1 = fig.add_subplot(211) # Creates another plot image and turns visibility of the axes off
    ax1.axis('off')
    children=[]
    for text in annot_strings:
        children.append(TextArea(annot_strings[text], textprops=dict(color="red")))
        #print(annot_strings[text])
    box = VPacker(children=children, align="left", pad=5, sep=5)

    # anchored_box creates the text box outside of the plot
    if(grid_type.lower()=="rectangular"):
        anchored_box = AnchoredOffsetbox(loc=3,
                                        child=box, pad=0.,
                                        frameon=True,
                                        bbox_to_anchor=(0.01, 0.01),
                                        bbox_transform=ax.transAxes,
                                        borderpad=0.,
                                        )
    else:
        anchored_box = AnchoredOffsetbox(loc=3,
                                        child=box, pad=0.,
                                        frameon=True
                                        )
    
    ax1.add_artist(anchored_box)
    ax1.figure.savefig(working_dir+'/Som/labels_new.png',bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()





#initialize variables
annot_strings={}
annot_strings_for_dict={}
data = np.loadtxt(
        newLabelData, 
        dtype='str',
        delimiter=',',
        skiprows=0
        )
outfile=[]
for i in range(0,len(data[0])):
    if(data[0][i]=='label'):
        outfile=data[1:,i]
#run functions
annot_ticks=np.empty([somx, somy], dtype="<U32")
create_annotations()
draw_som_clusters()