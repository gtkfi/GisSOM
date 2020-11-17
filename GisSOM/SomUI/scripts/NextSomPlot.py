# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:54:21 2019

@author: Sakari Hautala, Joonas Haikonen

Python script to visualize SOM calculation results & original data

inputs:
1)outSomFile
2)som_x
3)som_y
4)outGeoFile
5)Model.InputFile
6)Model.EastingColumnIndex
7)Model.NorthingColumnIndex
8)Model.Working_Folder
"""
#import warnings
#with warnings.catch_warnings():
#    warnings.filterwarnings("ignore")
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import seaborn as sns
import sys
import pickle
from sklearn.model_selection import train_test_split
import pandas as pd
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, HPacker, VPacker
from matplotlib.ticker import FormatStrFormatter
from loadfile import read_lrn_header
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import math
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.collections import RegularPolyCollection
#print("Start plotting")
#start_time2 = time.time()


"""
Load input parameters & do basic setup
Inputs:
1) Model.Output_file_somspace
2) Model.Som_x 
3) Model.Som_y 
4) Model.Output_file_geospace
5) Model.InputFile 
6) Model.EastingColumnIndex 
7) Model.NorthingColumnIndex
8) Model.LabelColumnIndex
8) Model.Output_Folder
9) Model.GridType
10) Redraw (boolean) - whether to calculate all plots or only those that deal with clustering 
"""

parser = argparse.ArgumentParser(description='Script for generating self organizing maps')
parser.add_argument('--outsomfile',nargs='?',dest="outsomfile", help='Som calculation somspace output text file')
parser.add_argument('--som_x',nargs='?', help='som x dimension')
parser.add_argument('--som_y',nargs='?', help='som y dimension')
parser.add_argument('--input_file',nargs='?', help='Input file(*.lrn)')
parser.add_argument('--dir',nargs='?', help='Input file(*.lrn)')
parser.add_argument('--original_data_dir', default=None, dest="original_data_dir", help='location of input columns with original data')
parser.add_argument('--grid_type',nargs='?', help='grid type (square or hexa)')
parser.add_argument('--redraw',nargs='?', help=' #whether to draw all plots, or only those required for clustering (true: draw all. false:draw only for clustering).')
parser.add_argument('--outgeofile', default=None, dest="outgeofile", help='#som geospace results txt file')
parser.add_argument('--eastingIndex', default=None, dest="eastingIndex", help='index of easting column')
parser.add_argument('--northingIndex', default=None, dest="northingIndex", help='index of northing column')
parser.add_argument('--labelIndex', default=None, dest="labelIndex", help='index of label column')
parser.add_argument('--dataType', default=None, dest="dataType", help='index of label column')
args=parser.parse_args()

outsomfile=args.outsomfile  #som results txt file
original_data_dir=args.original_data_dir
somx=int(args.som_x)        #som x parameter
somy=int(args.som_y)        #som y parameter
input_file=args.input_file  #original input file 
dir=args.dir                #output directory of GisSOM
grid_type=args.grid_type    #grid type 
redraw=args.redraw          #whether to draw all plots, or only those required for clustering (true: draw all. false:draw only for clustering)
dataType=args.dataType
outgeofile=None
eastingIndex=None
northingIndex=None
if args.outgeofile is not None:
    outgeofile=args.outgeofile        #som geospace results txt file
if args.eastingIndex is not None:
    eastingIndex=args.eastingIndex    #index of easting column
if args.northingIndex is not None:
    northingIndex=args.northingIndex  #index of northing column
if args.labelIndex is not None:
    labelIndex=args.labelIndex

    





"""Declare and initialize variables"""

with open(dir+"/som.dictionary", 'rb') as som_dictionary_file:#Draw Boxplots:
     som_dict = pickle.load(som_dictionary_file)
som_data= np.genfromtxt(outsomfile,skip_header=(1), delimiter=' ')
working_dir=dir#+"/somresults"
dataPrepDir=dir+"/DataPreparation"
dataPrepDir2=dir+"/DataForOriginalPlots/DataPreparation"

som=pd.read_csv(outsomfile, delimiter=' ', header=None)
som_headers=som.iloc[0] 
if outgeofile is not None:
    geo_data=np.genfromtxt(outgeofile, skip_header=(1), delimiter=' ')
som_table=np.zeros((somx,somy))#empty somx*somy sized table for som plots
if outgeofile is not None: #if spatial, draw geo plots
    geofile = open(outgeofile, "r")
    header_line = geofile.readline()
    geo_headers=['#']
    geo_headers = geo_headers +header_line.split(" ")

columns=[]    
firstFileName=""
index=0

if(input_file[-3:].lower()=="lrn"):     #if input is lrn file
    header=read_lrn_header(input_file)  
    actualNumberOfColumns=header['cols']-1         
else:
    actualNumberOfColumns=len(som_headers)-3#this is really not the actual number of columns...should be renamed.

#Generate colormaps and ticks for clustering
clusters=int(max(som_data[:,len(som_data[0])-1])+1)
discrete_cmap=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
discrete_cmap_2=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=True)
cluster_ticks=[]
for i in range (clusters,0,-1):
    cluster_ticks.append(i-1)   
palette=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
formatted_palette=[]

#format color values to format rgb(x,y,x), where x y and z are values between 0 and 255. values before conversion are in format a,b,c where a b and c are values between 0 and 1
for i in palette:
	formatted_value='rgb('
	for j in i:
		formatted_value=formatted_value+str("{:.2f}".format(j*255))+','
	formatted_value=formatted_value[:-1] #remove last comma. replace this with some one liner equivalent of a conditional operator?  
	formatted_value=formatted_value+')' 
	formatted_palette.append(formatted_value)
palette=formatted_palette

#Format palette into colorscale. for example 10 clusters: (0,0.1,rgb_val), (0.1,0.2 rgb_val_2),...... ,(0.9,1,rgb_val_x) ((not always distance of 0.1)) so each cluster is assigned a specific color.
clusterColorscale=[]
for i in range (0,clusters):
    clusterColorscale.append([float(float(i)/float(clusters)),palette[i]])
    clusterColorscale.append([float(float(i+1)/clusters),palette[i]])


if(grid_type.lower()!="rectangular"):
    x=somx
    y=somy
    centers=[]
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

# Puts labels into array for cluster graph.

if (labelIndex!="-2"):
    annot_strings={}
    annot_data=[]
    filename="outfile" + str(labelIndex) + "label.npy"
    outfile=np.load(dataPrepDir+"/"+filename,allow_pickle=True)[4:]
    annot_ticks=np.empty([somx, somy], dtype="<U32")
    bmus=som_dict["bmus"]
    counter=1
    for i in range(2,len(outfile)):  
        tick=annot_ticks[bmus[i-2][0]][bmus[i-2][1]]
        if(outfile[i]!='' and outfile[i]!= "nan" and outfile[i]!='0'):
            if (tick==''): # Checks if there are other labels.
                annot_ticks[bmus[i-2][0]][bmus[i-2][1]]=str(counter)            
                annot_strings[str(counter)]=str(counter) + ": " + outfile[i]
                annot_data.append([(str(counter) + ": " + outfile[i]),(str(bmus[i-2][0]) + str(bmus[i-2][1])),(str(geo_data[i-2][0]) + ", " + str(geo_data[i-2][1]))])             
                counter=counter+1
            else:
                annot_strings[tick]=annot_strings[tick] + ", " + outfile[i]
                annot_data.append([(str(tick) + ": " + outfile[i]),(str(bmus[i-2][0]) + str(bmus[i-2][1])),(str(geo_data[i-2][0]) + ", " + str(geo_data[i-2][1]))])
else:
    annot_ticks=np.empty([somx, somy], dtype='<U')
    annot_ticks.fill("")


#print("End of data preparation: --- %s seconds ---" % (time.time() - start_time2))




"""Function Definitions:"""

"""
Function for plotting hexagonal heatmaps.
Based on an excellent stackoverflow post by Fernando Ferreira 
https://stackoverflow.com/questions/23726564/matplotlib-regularpolygon-collection-location-on-the-canvas/23811383#23811383
"""
def plot_hexa(grid,
             d_matrix,
             w=1080,
            dpi=72.,
            title='SOM Hit map',
            colmap='jet',
            ptype='scatter'):
    n_centers = grid['centers']
    x, y = grid['x'], grid['y']
    if(somx<somy):
        xinch = (x * w / y) / dpi
    else:
        xinch=(y * w / y) / dpi
    yinch = (y * w / x) / dpi

    fig = plt.figure(figsize=(xinch, yinch), dpi=dpi)
    ax = fig.add_subplot(111, aspect='equal')
    xpoints = n_centers[:, 0]
    ypoints = n_centers[:, 1]
    ax.scatter(xpoints, ypoints, s=0.0, marker='s')
    ax.axis([min(xpoints)-1., max(xpoints)+1.,
             max(ypoints)+1., min(ypoints)-1.])
    xy_pixels = ax.transData.transform(np.vstack([xpoints, ypoints]).T)
    xpix, ypix = xy_pixels.T
    
    # In matplotlib, 0,0 is the lower left corner, whereas it's usually the
    # upper right for most image software, so we'll flip the y-coords
    width, height = fig.canvas.get_width_height()
    ypix = height - ypix
    
    # discover radius and hexagon
    #apothem = 1.8 * (xpix[1] - xpix[0]) / math.sqrt(3)#.9 
    if(ptype=='scatter'): #if the data type is csv with gaps
        apothem=(xpix[1] - xpix[0]) 
        area_inner_circle = abs(apothem) 
        collection_bg = RegularPolyCollection(
            numsides=4,  
            rotation=150,
            sizes=(area_inner_circle,),
            edgecolor="none",
            #edgecolors = (0, 0, 0, 1),
            array= d_matrix,
            cmap = colmap,
            offsets = n_centers,
            transOffset = ax.transData,
        )
    else: #regular hexa plot
        apothem = 1.8 * (xpix[1] - xpix[0]) / math.sqrt(3)#.9 oli
        area_inner_circle = math.pi * (apothem ** 2)
        collection_bg = RegularPolyCollection(
            numsides=6,  # a hexagon
            rotation=0,
            sizes=(area_inner_circle,),
            edgecolors = (0, 0, 0, 1),
            array= d_matrix,
            cmap = colmap,
            offsets = n_centers,
            transOffset = ax.transData,
        )
    ax.add_collection(collection_bg, autolim=True)
    
    ax.axis('off')
    ax.autoscale_view()
    ax.set_title(title)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    #plt.colorbar(collection_bg, cax=cax)#cm.ScalarMappable(norm=norm, cmap=cmap)
    if(colmap=='jet'):
        cbar=plt.colorbar(collection_bg, cax=cax,ticklocation='right', aspect=10)
        cbar.ax.invert_yaxis()
        cbar.ax.tick_params(axis='y', direction='out', pad=30)
    else:
        colmap2=colmap
        bounds = np.linspace(0, clusters, clusters+1)
        bounds2 = np.linspace(0.5, clusters+0.5, clusters+1.5)
        norm = mpl.colors.BoundaryNorm(bounds, colmap2.N)
        cbar=mpl.colorbar.ColorbarBase(cax, cmap=colmap2, norm=norm,
        spacing='proportional',ticklocation='right', ticks=bounds2, boundaries=bounds, format='%1i')
        cbar.ax.invert_yaxis()
        cbar.ax.tick_params(axis='y', direction='out', pad=30)
    plt.gca().invert_yaxis()
    return ax



"""
Plot geospace plots & q-error if type is grid
"""
def plot_geospace_results_grid():
    global geo_data
    global geo_headers
    global som_data
    for i in range(0, len(som_data[0])-3): 
        x=geo_data[:,0]
        y=geo_data[:,1]
        z=geo_data[:,(len(som_data[0])+1+i)]
        df = pd.DataFrame.from_dict(np.array([x,y,z]).T)
        df.columns = ['X_value','Y_value','Z_value']
        df['Z_value'] = pd.to_numeric(df['Z_value'])
        pivotted= df.pivot('Y_value','X_value','Z_value')
        #pivotted=pivotted.fillna(value='nan')
        sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
        ax=sns.heatmap(pivotted,cmap='jet', square=True, linewidths=0, xticklabels="auto", yticklabels="auto")
        scalebar = AnchoredSizeBar(ax.transData, 3.4, str(geo_data[4][0] - geo_data[0][0]), 1, pad=0.4,
                                    sep=5, borderpad=0.1,
                                    size_vertical=0.2)
        #ax.add_artist(scalebar)
        # Set tick labels to integers:
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
            every_nth_y=1
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        for n, label in enumerate(ax.yaxis.get_ticklabels()):
            if n % every_nth_y != 0:
                label.set_visible(False)
        ax.xaxis.get_ticklabels()[-1].set_visible(True)
        ax.yaxis.get_ticklabels()[-1].set_visible(True)
        plt.yticks(rotation=90)
        plt.yticks(ha='right')
        plt.yticks(va='bottom')
        plt.xticks(rotation=0)
        plt.xticks(ha='left')
        ax.invert_yaxis()
        ax.set_title(geo_headers[len(som_data[0])+i+2])
        plt.tight_layout()
        ax.figure.savefig(working_dir+'/Geo/geoplot_'+str(i+2)+'.png', dpi=300)
        plt.clf()
        plt.cla()
        plt.close()

"""
Plot geospace plots & q-error if type is scatter
"""
def plot_geospace_results_scatter():
    global geo_data
    global geo_headers
    global som_data
    #x=max(geo_data[:,0])-min(geo_data[:,0])
    #y=max(geo_data[:,1])-min(geo_data[:,1])

    centers=[]     
    for i in range(0, len(geo_data)):	
        centers.append([geo_data[i][0],geo_data[i][1]])
    grid={'centers':np.array(centers), 
          'x':np.array([len(geo_data)]),
          'y':np.array([len(geo_data)])}

    for i in range(0, len(som_data[0])-3): 
        x=geo_data[:,0]
        y=geo_data[:,1]
        z=geo_data[:,(len(som_data[0])+1+i)]
        sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
        mpl.rcParams.update({'font.size': 30})
        ax = plot_hexa(grid, z,title=som_headers[i], ptype='scatter')   
        
        #scalebar = AnchoredSizeBar(ax.transData, 3.4, str(geo_data[4][0] - geo_data[0][0]), 1, pad=0.4,
        #                            sep=5, borderpad=0.1,
        #                            size_vertical=0.2)
        #ax.add_artist(scalebar)
        # Set tick labels to integers:
        """
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
            every_nth_y=1
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        for n, label in enumerate(ax.yaxis.get_ticklabels()):
            if n % every_nth_y != 0:
                label.set_visible(False)
        ax.xaxis.get_ticklabels()[-1].set_visible(True)
        ax.yaxis.get_ticklabels()[-1].set_visible(True)
        """
        plt.yticks(rotation=90)
        plt.yticks(ha='right')
        plt.yticks(va='bottom')
        plt.xticks(rotation=0)
        plt.xticks(ha='left')
        ax.invert_yaxis()
        ax.set_title(geo_headers[len(som_data[0])+i+2])
        plt.tight_layout()
        ax.figure.savefig(working_dir+'/Geo/geoplot_'+str(i+2)+'.png', dpi=300)
        plt.clf()
        plt.cla()
        plt.close()
        mpl.rcParams.update({'font.size': 12})  


"""
Draw Som result plots
"""
def draw_som_results():
    global som_data
    global som_table
    global grid
    global hits
    global som_headers
    for j in range(2,len(som_data[0])-1):
        if(grid_type.lower()=="rectangular"):
            for i in range(0,len(som_data)): 
                som_table[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][j] #som_table: somx*somy size
            ax = sns.heatmap(som_table.transpose(), cmap="jet", linewidth=0)   
            ax.set_title(som_headers[j])    
        else:
            hits=som_data[:,j]
            mpl.rcParams.update({'font.size': 30})
            ax = plot_hexa(grid, hits,title=som_headers[j+1], ptype='grid')   
            mpl.rcParams.update({'font.size': 12})
            ax.set_title(som_headers[j]) 
        ax.figure.savefig(working_dir+'/Som/somplot_' +str(j-1)+'.png')#Creating the folder is done in C# side of things.    
        plt.clf()
        plt.cla()
        plt.close()  


"""
Draw Som Cluster plot
"""
def draw_som_clusters():
    global som_data
    global som_table
    global annot_ticks
    global som_headers
    if(grid_type.lower()=="rectangular"):
        for i in range(0,len(som_data)): 
            som_table[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][len(som_data[0])-1]
        ax = sns.heatmap(som_table.transpose(), cmap=discrete_cmap, linewidth=0, vmin=-0.5, vmax=clusters-0.5, center=clusters/2-0.5, cbar_kws=dict(ticks=cluster_ticks), annot=annot_ticks.transpose(), fmt = '')
    else:
        hits=som_data[:,len(som_data[0])-1]
        mpl.rcParams.update({'font.size': 30})
        ax = plot_hexa(grid, hits,colmap=discrete_cmap_2, ptype='grid')
    ax.set_title(som_headers[len(som_headers)-1])
    ax.figure.savefig(working_dir+'/Som/somplot_' + str(len(som_data[0])-2) + '.png')
    plt.clf()
    plt.cla()
    plt.close()
    mpl.rcParams.update({'font.size': 12})  
    if(labelIndex!="-2"):
        fig = plt.figure()
        ax1 = fig.add_subplot(211) # Creates another plot image and turns visibility of the axes off
        ax1.axis('off')
        children=[]
        for text in annot_strings:
            children.append(TextArea(annot_strings[text], textprops=dict(color="red")))
            #print(annot_strings[text])
        box = VPacker(children=children, align="left", pad=5, sep=5)

        # anchored_box creates the text box outside of the plot
        anchored_box = AnchoredOffsetbox(loc=3,
                                            child=box, pad=0.,
                                            frameon=True,
                                            bbox_to_anchor=(0.01, 0.01),
                                            bbox_transform=ax.transAxes,
                                            borderpad=0.,
                                            )
        ax1.add_artist(anchored_box)
        ax1.figure.savefig(working_dir+'/Som/somplot_' + str(len(som_data[0])-1) + '.png')
        plt.clf()
        plt.cla()
        plt.close()
        df = pd.DataFrame(annot_data)
        headers = ["label", "som", "datapoint"]
        df.to_csv(working_dir+'/labels.csv', index=False, header=headers)




"""
Plot geospace clusters, if there is more than 1 cluster
"""
def plot_geospace_clusters_grid():
    global geo_data
    x=geo_data[:,0]
    y=geo_data[:,1]
    z=geo_data[:,(4)]    
    df = pd.DataFrame.from_dict(np.array([x,y,z]).T)
    df.columns = ['X_value','Y_value','Z_value']
    df['Z_value'] = pd.to_numeric(df['Z_value'])
    pivotted= df.pivot('Y_value','X_value','Z_value')
    ax=sns.heatmap(pivotted,cmap=discrete_cmap, vmin = -0.5, vmax = clusters - 0.5, square=True, linewidths=0, xticklabels="auto", yticklabels="auto", cbar_kws=dict(ticks=cluster_ticks))
    #scalebar = AnchoredSizeBar(ax.transData, 3.4, str(my_data2[4][0] - my_data2[0][0]), 1, pad=0.4,
    #                           sep=5, borderpad=0.1,
    #                           size_vertical=0.2)
    #ax.add_artist(scalebar)
    #every_nth =4#4 #this should be dynamic, not constant? 

    # Set tick labels to integers:
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
    if(every_nth_y==0):#temp solution, for data sets with only 1 y coordinate
        every_nth_y=1
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    for n, label in enumerate(ax.yaxis.get_ticklabels()):
        if n % every_nth_y != 0:
            label.set_visible(False)
    ax.xaxis.get_ticklabels()[-1].set_visible(True)
    ax.yaxis.get_ticklabels()[-1].set_visible(True)
    #ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%5.0d'))
    #ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    plt.yticks(rotation=90)
    plt.yticks(ha='right')
    plt.yticks(va='bottom')
    plt.xticks(rotation=0)
    plt.xticks(ha='left')
    ax.invert_yaxis()
    ax.set_title('cluster')
    plt.tight_layout()
    ax.figure.savefig(working_dir+'/Geo/geoplot_'+str(1)+'.png', dpi=300)
    plt.clf()
    plt.cla()
    plt.close()       
    
    
def plot_geospace_clusters_scatter():
    global geo_data
    x=geo_data[:,0]
    y=geo_data[:,1]
    z=geo_data[:,(4)]  
    
    centers=[]     
    for i in range(0, len(geo_data)):	
        centers.append([geo_data[i][0],geo_data[i][1]])
    grid={'centers':np.array(centers), 
          'x':np.array([len(geo_data)]),
          'y':np.array([len(geo_data)])}    
    mpl.rcParams.update({'font.size': 30})
    ax = plot_hexa(grid, z,title="clusters",colmap=discrete_cmap_2, ptype='scatter')   
    # Set tick labels to integers:
    """
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
    if(every_nth_y==0):#temp solution, for data sets with only 1 y coordinate
        every_nth_y=1
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    for n, label in enumerate(ax.yaxis.get_ticklabels()):
        if n % every_nth_y != 0:
            label.set_visible(False)
    ax.xaxis.get_ticklabels()[-1].set_visible(True)
    ax.yaxis.get_ticklabels()[-1].set_visible(True)
    """
    
    #ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%5.0d'))
    #ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    plt.yticks(rotation=90)
    plt.yticks(ha='right')
    plt.yticks(va='bottom')
    plt.xticks(rotation=0)
    plt.xticks(ha='left')
    ax.invert_yaxis()
    ax.set_title('cluster')
    plt.tight_layout()
    ax.figure.savefig(working_dir+'/Geo/geoplot_'+str(1)+'.png', dpi=300)
    plt.clf()
    plt.cla()
    plt.close()   
    mpl.rcParams.update({'font.size': 12})  

"""
Plot boxplots using som data.
"""

def draw_box_andscatterplots():
    
    global som_dict
    global geo_data #som_data
    counter=0
    mpl.rcParams.update({'font.size': 12})  
    #sampleSize=4000
    #clusters_2d=som_dict['clusters']
    #bmus=som_dict['bmus']
    cluster_col=[]

    for i in range(0,len(som_data)): 
        cluster_col.append(som_data[i][len(som_data[0])-1]);
    cluster_nparray=np.asarray(cluster_col)   
    clusters_unique=np.unique(cluster_nparray)
    for k in range(len(discrete_cmap)-1,-1,-1):
        if(k not in clusters_unique):
            discrete_cmap.pop(k)  
    for i in range(3,len(som_data[0])-1):#3 to skip x y and cluster col            
        z=som_data[:,i]      
        ax=sns.boxplot(x=cluster_nparray.astype(float), y=z.astype(float), hue=cluster_nparray.astype(float) ,dodge=False, palette=discrete_cmap)       
        ax.set_title(som_headers[i-1])
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f')) 
        ax.legend(bbox_to_anchor=(1.05, 1),loc=0,handlelength=2,fontsize=8 ,borderaxespad=0.)   
        plt.tight_layout()           
        ax.figure.savefig(working_dir+'/Boxplot/boxplot_' +str(i)+'.png')   
        plt.clf()
        plt.cla()
        plt.close()        
        

"""
Draw number of hits
"""
def draw_number_of_hits():
    mpl.rcParams.update({'font.size': 12})
    if outgeofile is not None:
        hits=np.zeros((somx,somy))   
        for i in range(0, len(geo_data)):
            x=geo_data[:,2]
            y=geo_data[:,3]
            hits[int(x[i])][int(y[i])]+=1
        hits=np.transpose(hits)
        if(grid_type=='rectangular'):
            ax = sns.heatmap(hits, cmap="binary", linewidth=0)   
        else: #if grid type is hexagonal
            mpl.rcParams.update({'font.size': 30})
            ax = plot_hexa(grid, hits.flatten(order='F'), ptype='grid')    
        ax.set_title("Number of hits per SOM cell")    
        ax.figure.savefig(working_dir+'/Som/somplot_' +str(len(som_data[0])+1)+'.png')
        mpl.rcParams.update({'font.size': 12})
        plt.clf()
        plt.cla()
        plt.close()







"""
Script "Base". 
"""
           

#start_time_0 = time.time()
if outgeofile is not None: #if spatial, draw geo plots
    if(dataType=='scatter'):
        if(max(geo_data[:,(4)])>0):#if clusters
            plot_geospace_clusters_scatter()
        if(redraw!="false"):
            plot_geospace_results_scatter()
        print("GeoSpace plots finished")
    else:
        if(max(geo_data[:,(4)])>0):#if clusters
            plot_geospace_clusters_grid()
        if(redraw!="false"):
            plot_geospace_results_grid()
        print("GeoSpace plots finished")
if(int(max(som_data[:,len(som_data[0])-1]))>0): #draw som cluster plot if there is more than 1 cluster
    draw_som_clusters()

#in case the function was called for redrawing after selecting a different clustering result. so that we can skip stuff we don't have to redraw to speed things up
if(redraw!="false"):
    draw_som_results()
draw_number_of_hits()
print("SomSpace plots finshed")
#start_time = time.time()

if(som_dict['clusters'] is not None):
    draw_box_andscatterplots()
print("Boxplots finished")
#print("Scatterplot: --- %s seconds ---" % (time.time() - start_time))


#print("--- %s seconds ---" % (time.time() - start_time))
#print("finished with data preparation")
#print("Everything:: --- %s seconds ---" % (time.time() - start_time2))
#print("All plotting took: --- %s seconds ---" % (time.time() - start_time_0))