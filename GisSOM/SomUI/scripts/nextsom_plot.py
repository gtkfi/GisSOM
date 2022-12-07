# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:54:21 2019

@author: Sakari Hautala, Joonas Haikonen

Python script to visualize SOM calculation results & original data. Draws heatmaps based on som and geospace results, and boxplots of data distribution per cluster 

Inputs:
1) Somspace results file
2) Som x dimension
3) Som y dimension
4) Geospace results file
5) Input file used for som calculation 
6) Index of easting column 
7) Index of northing column
8) Index of label column
8) Output folder
9) Grid type (rectangular or hexagonal)
10) Redraw (boolean) - whether to calculate all plots or only those that deal with clustering 
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import seaborn as sns
import pickle
import pandas as pd
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea, VPacker # HPacker,
from matplotlib.ticker import FormatStrFormatter
import math
from matplotlib.lines import Line2D
from plotting_functions import plot_hexa

"""
Load input parameters & do basic setup

"""

parser = argparse.ArgumentParser(description='Script for drawing plots from self organizing maps')
parser.add_argument('--outsomfile',nargs='?',dest="outsomfile", help='Som calculation somspace output text file')
parser.add_argument('--som_x',nargs='?', help='som x dimension')
parser.add_argument('--som_y',nargs='?', help='som y dimension')
parser.add_argument('--input_file',nargs='?', help='Input file(*.lrn)')
parser.add_argument('--dir',nargs='?', help='Input file(*.lrn)')
parser.add_argument('--grid_type',nargs='?', help='grid type (square or hexa)')
parser.add_argument('--redraw',nargs='?', help=' #whether to draw all plots, or only those required for clustering (true: draw all. false:draw only for clustering).')
parser.add_argument('--outgeofile', default=None, dest="outgeofile", help='#som geospace results txt file')
parser.add_argument('--dataType', default=None, dest="dataType", help='Data type (scatter or grid)')
parser.add_argument('--noDataValue', default='NA', dest="noDataValue", help='noData value')
args=parser.parse_args()

outsomfile=args.outsomfile  #somspace results txt file
somx=int(args.som_x)        
somy=int(args.som_y)        
input_file=args.input_file  #original input file 
dir=args.dir               
grid_type=args.grid_type   
redraw=args.redraw          #whether to draw all plots, or only those required for clustering (true: draw all. false:draw only for clustering)
dataType=args.dataType
outgeofile=None
eastingIndex=None
northingIndex=None
if args.outgeofile is not None:
    outgeofile=args.outgeofile      
labelIndex="-2" #TODO: Now that labelIndex is no longer a parameter, this system should be removed.
    


"""Initialize variables"""

with open(dir+"/som.dictionary", 'rb') as som_dictionary_file:
     som_dict = pickle.load(som_dictionary_file)
som_data= np.genfromtxt(outsomfile,skip_header=(1), delimiter=' ')
working_dir=dir#+"/somresults"

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


#Generate colormaps and ticks for clustering
clusters=int(max(som_data[:,len(som_data[0])-2])+1)
discrete_cmap=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
discrete_cmap_2=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=True)
cluster_ticks=[]
cluster_tick_labels=[]
cluster_hit_count=[]


#labeling clusters in colorbar with format "cluster number:  number of data points in this cluster".
if(clusters>1):
    for i in range (clusters,0,-1):
        cluster_array=som_dict['clusters'].transpose()#TODO: figure out if this a problem elsewhere.
        cluster_ticks.append(i-1)   
        count=0
        for bmu in som_dict['bmus']:
            if (cluster_array[bmu[0]][bmu[1]])+1==i:
                count+=1
        cluster_tick_labels.append(str(i-1)+ "   " +str(count)) 
        
palette=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
formatted_palette=[]

#format color values to format rgb(x,y,x), where x y and z are values between 0 and 255. values before conversion are in format a,b,c where a b and c are values between 0 and 1
for i in palette:
	formatted_value='rgb('
	for j in i:
		formatted_value=formatted_value+str("{:.2f}".format(j*255))+','
	formatted_value=formatted_value[:-1] #remove last comma 
	formatted_value=formatted_value+')' 
	formatted_palette.append(formatted_value)
palette=formatted_palette

#Format palette into colorscale. for example 10 clusters: (0,0.1,rgb_val), (0.1,0.2 rgb_val_2),...... ,(0.9,1,rgb_val_x) ((not always distance of 0.1)) so each cluster is assigned a specific color.
clusterColorscale=[]
for i in range (0,clusters):
    clusterColorscale.append([float(float(i)/float(clusters)),palette[i]])
    clusterColorscale.append([float(float(i+1)/clusters),palette[i]])


if(grid_type.lower()=="hexagonal"): #if grid shape is hexagonal, initialize corresponding variables for hexa plots
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
else:
    grid=None
    
    
header_line=""#check if file has label column in it
with open(input_file,encoding='utf-8-sig') as fh:
    fh.readline() #skip first 3 rows
    fh.readline() #skip first 3 rows
    fh.readline() #skip first 3 rows
    header_line = fh.readline()
colnames=header_line.split("\t")
if('label' in colnames):
    labelIndex=colnames.index('label')
#if (labelIndex!="-2"):#eli tän checkin sijaan pitäs kattoa onko input filessä 'label' nimistä columnia hedereissä.
    annot_strings={}
    annot_strings_for_dict={}
    annot_data=[]
    data = np.loadtxt(
            input_file, 
            dtype='str',
            delimiter='\t',
            skiprows=3
            )
    outfile=[]
    
    #So. the current label format is the one that should be written to file, as it preserves all data. But for the plots, the new labeling system
    #should be changed so, that differences in count are not taken into account, i.e. A A B = A B B, both are reduced to A B. should clean up the legend by
    #quite a bit
    
    for i in range(0,len(data[0])):
        if(data[0][i].replace("\"","")=='label'):
            outfile=data[1:,i]
    annot_ticks=np.empty([somx, somy], dtype="<U32")
    bmus=som_dict["bmus"]
    counter=1
    for i in range(0,len(outfile)):   #AA. eli jos nonspatial: -2 sekoittaa. luultavasti ainakin tän takia. veikkaanpa että spatiaalilla on ton takia 2:n ekan skippi.      # ticks are added to list. annot_strings_for_dict stores them in a list, so that they can be sorted and reliably checked for duplicates including ones that are in different order.
        tick=annot_ticks[bmus[i][0]][bmus[i][1]]
        if(outfile[i]!='' and outfile[i]!= "nan" and outfile[i]!='NA' and outfile[i]!='NULL' and outfile[i]!='Null' and outfile[i]!='NoData' and outfile[i]!=args.noDataValue):#tähän jonon jatkoksi vielä noDataValue
            if (tick==''): 
                annot_ticks[bmus[i][0]][bmus[i][1]]=str(counter)    
                annot_strings[str(counter)]=[outfile[i]]
                annot_strings_for_dict[str(counter)]=[outfile[i]]
                if outgeofile is not None:
                    annot_data.append([(str(counter) + ": " + outfile[i]),(str(bmus[i][0]) + str(bmus[i][1])),(str(geo_data[i][0]) + ", " + str(geo_data[i][1]))]) 
                else:
                    annot_data.append([(str(counter) + ": " + outfile[i]),(str(bmus[i][0]) + str(bmus[i][1]))])          
                counter=counter+1
            else:   
                annot_strings[tick].append(outfile[i])
                annot_strings_for_dict[tick].append(outfile[i])
                if outgeofile is not None:
                    annot_data.append([(str(tick) + ": " + outfile[i]),(str(bmus[i][0]) + str(bmus[i][1])),(str(geo_data[i][0]) + ", " + str(geo_data[i][1]))])
                else:
                    annot_data.append([(str(tick) + ": " + outfile[i]),(str(bmus[i][0]) + str(bmus[i][1]))])
     
    for i in range(1, len(annot_strings_for_dict)+1): 
        annot_strings_for_dict[str(i)].sort()
    
    #add a step: merge duplicates within a labeling group. BUT the below result must also be kept...
    #eli joku unique filtteri vaan vetää eka tähän, sit jatko saa mennä aivan samaan tapaan.
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

                
else:
    annot_ticks=np.empty([somx, somy], dtype='<U')
    annot_ticks.fill("")









"""
Plot geospace plots & q-error if type is grid
"""
def plot_geospace_results_grid(geo_data, geo_headers, som_data):
    mpl.rcParams.update({'font.size': 14})

    for i in range(0, len(som_data[0])-4): 
        x=geo_data[:,0]
        y=geo_data[:,1]
        z=geo_data[:,(5+i)]
        df = pd.DataFrame.from_dict(np.array([x,y,z]).T)
        df.columns = ['X_value','Y_value','Z_value']
        df['Z_value'] = pd.to_numeric(df['Z_value'])
        pivotted= df.pivot('Y_value','X_value','Z_value')
        sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
        ax=sns.heatmap(pivotted,cmap='jet', square=True, linewidths=0, xticklabels="auto", yticklabels="auto")

        # Set tick labels
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
        if(every_nth==0):#for data sets with only 1 x coordinate
            every_nth=1
        every_nth_y = round((len(ax.yaxis.get_ticklabels()))/2)
        if(every_nth_y==0):#for data sets with only 1 x coordinate
            every_nth_y=1
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        for n, label in enumerate(ax.yaxis.get_ticklabels()):
            if n % every_nth_y != 0:
                label.set_visible(False)
        ax.xaxis.get_ticklabels()[-1].set_visible(True)
        ax.yaxis.get_ticklabels()[-1].set_visible(True)
        plt.yticks(rotation=90,ha='right',va='bottom')
        plt.xticks(rotation=0,ha='left')
        ax.invert_yaxis()
        ax.set_title(geo_headers[5+i+1])
        plt.tight_layout()
        ax.figure.savefig(working_dir+'/Geo/geoplot_'+str(i+2)+'.png', dpi=300)
        plt.clf()
        plt.cla()
        plt.close()
        
        
    #q_error:
    x=geo_data[:,0]
    y=geo_data[:,1]
    z=geo_data[:,(len(som_data[0])-5)*2 +5] 
    df = pd.DataFrame.from_dict(np.array([x,y,z]).T)
    df.columns = ['X_value','Y_value','Z_value']
    df['Z_value'] = pd.to_numeric(df['Z_value'])
    pivotted= df.pivot('Y_value','X_value','Z_value')
    sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
    ax=sns.heatmap(pivotted,cmap='jet', square=True, linewidths=0, xticklabels="auto", yticklabels="auto")
    
    # Set tick labels
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
    if(every_nth==0):#for data sets with only 1 x coordinate
        every_nth=1
    every_nth_y = round((len(ax.yaxis.get_ticklabels()))/2)
    if(every_nth_y==0):#for data sets with only 1 x coordinate
        every_nth_y=1
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    for n, label in enumerate(ax.yaxis.get_ticklabels()):
        if n % every_nth_y != 0:
            label.set_visible(False)
    ax.xaxis.get_ticklabels()[-1].set_visible(True)
    ax.yaxis.get_ticklabels()[-1].set_visible(True)
    plt.yticks(rotation=90, ha='right',va='bottom')
    plt.xticks(rotation=0, ha='left')
    ax.invert_yaxis()
    ax.set_title(geo_headers[(len(som_data[0])-5)*2 +6])#(geo_headers[len(som_data[0])+i+1])#tähän sama 5     
    plt.tight_layout()
    ax.figure.savefig(working_dir+'/Geo/geoplot_'+str(i+2)+'.png', dpi=300)
    plt.clf()
    plt.cla()
    plt.close()
    
    

"""
Plot geospace plots & q-error if type is scatter
"""
def plot_geospace_results_scatter(geo_data, geo_headers, som_data):

    centers=[]     
    for i in range(0, len(geo_data)):	
        centers.append([geo_data[i][0],geo_data[i][1]])
    grid={'centers':np.array(centers), 
          'x':np.array([len(geo_data)]),
          'y':np.array([len(geo_data)])}

    for i in range(0, len(som_data[0])-4):  
        z=geo_data[:,(5+i)]   
        sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
        mpl.rcParams.update({'font.size': 30})
        ax = plot_hexa(somx,somy,clusters,grid,z,cluster_tick_labels=cluster_tick_labels, title=geo_headers[5+i+1], ptype='scatter')           
        plt.yticks(rotation=90, ha='right', va='bottom')
        plt.xticks(rotation=0, ha='left')
        ax.invert_yaxis()
        plt.tight_layout()
        ax.figure.savefig(working_dir+'/Geo/geoplot_'+str(i+2)+'.png', dpi=300)
        plt.clf()
        plt.cla()
        plt.close()
        mpl.rcParams.update({'font.size': 12})  
       
        
    #draw q_error:
    z=geo_data[:,(len(som_data[0])-5)*2 +5]   
    sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
    mpl.rcParams.update({'font.size': 30})
    ax = plot_hexa(somx,somy,clusters,grid,z,cluster_tick_labels=cluster_tick_labels, title=geo_headers[(len(som_data[0])-5)*2 +6], ptype='scatter')           
    plt.yticks(rotation=90, ha='right', va='bottom')
    plt.xticks(rotation=0, ha='left')
    ax.invert_yaxis()
    plt.tight_layout()
    ax.figure.savefig(working_dir+'/Geo/geoplot_'+str(len(som_data[0])-2)+'.png', dpi=300)
    plt.clf()
    plt.cla()
    plt.close()
    mpl.rcParams.update({'font.size': 12})
    






"""
Draw Som result plots
"""
def draw_som_results(som_data, som_table,grid, annot_ticks, som_headers):
    for j in range(2,len(som_data[0])-3):
        if(grid_type.lower()=="rectangular"):
            for i in range(0,len(som_data)): 
                som_table[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][j] #som_table: somx*somy size
            ax = sns.heatmap(som_table.transpose(), cmap="jet", linewidth=0)   
            ax.set_title(som_headers[j])    
        else:#grid type=="hexagonal":
            hits=som_data[:,j]
            mpl.rcParams.update({'font.size': 30})
            ax = plot_hexa(somx,somy,clusters,grid, hits, annot_ticks,cluster_tick_labels,title=som_headers[j+1], ptype='grid')   
            mpl.rcParams.update({'font.size': 32})           
            ax.set_title(som_headers[j]) 
            mpl.rcParams.update({'font.size': 32})  
        ax.figure.savefig(working_dir+'/Som/somplot_' +str(j-1)+'.png',bbox_inches='tight')#Creating the folder is done in C# side of things.    
        plt.clf()
        plt.cla()
        plt.close()  
        mpl.rcParams.update({'font.size': 12})
        
        
"""
Draw U-matrix plot
"""
def draw_umatrix(som_data, som_table,grid, annot_ticks, som_headers):
    for j in range(len(som_data[0])-3,len(som_data[0])-2):
        if(grid_type.lower()=="rectangular"):
            for i in range(0,len(som_data)): 
                som_table[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][j] #som_table: somx*somy size
            ax = sns.heatmap(som_table.transpose(), cmap="jet", linewidth=0)   
            ax.set_title(som_headers[j])    
        else:#grid type=="hexagonal":
            hits=som_data[:,j]
            mpl.rcParams.update({'font.size': 30})
            ax = plot_hexa(somx,somy,clusters,grid, hits, annot_ticks,cluster_tick_labels,title=som_headers[j+1], ptype='grid')   #j+1 to 
            mpl.rcParams.update({'font.size': 32})           
            ax.set_title(som_headers[j]) 
            mpl.rcParams.update({'font.size': 32})  
        ax.figure.savefig(working_dir+'/Som/somplot_' +str(j-1)+'.png',bbox_inches='tight')#Creating the folder is done in C# side of things.    
        plt.clf()
        plt.cla()
        plt.close()  
        mpl.rcParams.update({'font.size': 12})

"""
Draw Som Cluster plot
"""
def draw_som_clusters(som_data, som_table, annot_ticks, som_headers):    
    if(grid_type.lower()=="rectangular"):
        mpl.rcParams.update({'font.size': 14})  
        for i in range(0,len(som_data)): 
            som_table[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][len(som_data[0])-2]          
        ax = sns.heatmap(som_table.transpose(), cmap=discrete_cmap, linewidth=0, vmin=-0.5, vmax=clusters-0.5, center=clusters/2-0.5, cbar_kws=dict(ticks=cluster_ticks), annot=annot_ticks.transpose(), fmt = '')
        colorbar = ax.collections[0].colorbar
        colorbar.set_ticklabels(cluster_tick_labels)
        ax.set_title(som_headers[len(som_headers)-2])
    else:#grid type=="hexagonal":
        hits=som_data[:,len(som_data[0])-2]   
        mpl.rcParams.update({'font.size': 30})  
        ax = plot_hexa(somx,somy,clusters,grid,hits,annot_ticks,cluster_tick_labels,colmap=discrete_cmap_2, ptype='grid',labelIndex=labelIndex)
        mpl.rcParams.update({'font.size': 32})  
        ax.set_title(som_headers[len(som_headers)-2])
        mpl.rcParams.update({'font.size': 30})  
    ax.figure.savefig(working_dir+'/Som/somplot_' + str(len(som_data[0])-3) + '.png',bbox_inches='tight')
    plt.clf()
    plt.cla()
    plt.close()
    if(labelIndex!="-2"):
        mpl.rcParams.update({'font.size': 12})  
        fig = plt.figure(figsize= [6.4, 4.8])
        ax1 = fig.add_subplot(211) # Creates another plot image and turns visibility of the axes off
        ax1.axis('off')
        children=[]
        for text in annot_strings:
            children.append(TextArea(annot_strings[text], textprops=dict(color="red")))
        box = VPacker(children=children, align="left", pad=5, sep=5)

        # anchored_box creates the text box outside of the plot
        if(grid_type.lower()=="rectangular"):
            location=3
            anchored_box = AnchoredOffsetbox(loc=location,
                                            child=box, pad=0.,
                                            frameon=True,
                                            bbox_to_anchor=(0.01, 0.01),
                                            bbox_transform=ax.transAxes,
                                            borderpad=0.,                                       
                                            )
        else:
            location=3
            anchored_box = AnchoredOffsetbox(loc=location,
                                            child=box,
                                            borderpad=0.
                                            )
        
        ax1.add_artist(anchored_box)
        ax1.figure.savefig(working_dir+'/Som/somplot_' + str(len(som_data[0])-1) + '.png',bbox_inches='tight')
        plt.clf()
        plt.cla()
        plt.close()
        df = pd.DataFrame(annot_data)
        if outgeofile is not None: 
            headers = ["label", "som", "datapoint"]
        else:
            headers = ["label", "som"]
        df.to_csv(working_dir+'/labels_flat.csv', index=False, header=headers)   #so in addition to this there should be a list thats written out in the format of current label legend?
        #list_grouped=list(annot_strings.items())
        array_grouped=np.array(list(annot_strings.items()))#dict to list and list to np array
        for i in range(0,len(array_grouped)):
            array_grouped[i][1]= array_grouped[i][1][(array_grouped[i][1].find(":")+1):len(array_grouped[i][1])]      #  ": "+ ','.join(annot_strings[str(i)])
        np.savetxt(working_dir+'/labels_grouped.csv', array_grouped, delimiter=',', fmt='%s')
        #df_grouped.to_csv(working_dir+'/labels_grouped.csv', index=False, header=headers)

"""
Plot geospace clusters, if there is more than 1 cluster and input type is grid
"""
def plot_geospace_clusters_grid(geo_data):
    #global geo_data
    x=geo_data[:,0]
    y=geo_data[:,1]
    z=geo_data[:,(4)]    
    df = pd.DataFrame.from_dict(np.array([x,y,z]).T)
    df.columns = ['X_value','Y_value','Z_value']
    df['Z_value'] = pd.to_numeric(df['Z_value'])
    pivotted= df.pivot('Y_value','X_value','Z_value')
    mpl.rcParams.update({'font.size': 14})
    ax=sns.heatmap(pivotted,cmap=discrete_cmap, vmin = -0.5, vmax = clusters - 0.5, square=True, linewidths=0, xticklabels="auto", yticklabels="auto", cbar_kws=dict(ticks=cluster_ticks))

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
    if(every_nth==0):# for data sets with only 1 x coordinate
        every_nth=1
    every_nth_y = round((len(ax.yaxis.get_ticklabels()))/2)
    if(every_nth_y==0):#for data sets with only 1 y coordinate
        every_nth_y=1
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)
    for n, label in enumerate(ax.yaxis.get_ticklabels()):
        if n % every_nth_y != 0:
            label.set_visible(False)
    ax.xaxis.get_ticklabels()[-1].set_visible(True)
    ax.yaxis.get_ticklabels()[-1].set_visible(True)
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticklabels(cluster_tick_labels)
    plt.yticks(rotation=90)#, ha='right', va='bottom')
    #plt.yticks(ha='right')
    #plt.yticks(va='bottom')
    plt.xticks(rotation=0)
    plt.xticks(ha='left')
    ax.invert_yaxis()
    ax.set_title('cluster')
    plt.tight_layout()
    ax.figure.savefig(working_dir+'/Geo/geoplot_'+str(1)+'.png', dpi=300)
    plt.clf()
    plt.cla()
    plt.close()       
    
    
"""
Plot geospace clusters if input type is scatter
"""
def plot_geospace_clusters_scatter(geo_data):
    #global geo_data
    z=geo_data[:,(4)]      
    centers=[]     
    for i in range(0, len(geo_data)):	
        centers.append([geo_data[i][0],geo_data[i][1]])
    grid={'centers':np.array(centers), 
          'x':np.array([len(geo_data)]),
          'y':np.array([len(geo_data)])}    
    mpl.rcParams.update({'font.size': 30})
    ax = plot_hexa(somx,somy,clusters,grid,z,cluster_tick_labels=cluster_tick_labels, title="clusters",colmap=discrete_cmap_2, ptype='scatter')       
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

def draw_boxplots(som_dict,som_data):
    
    mpl.rcParams.update({'font.size': 12})  
    cluster_col=[]
    
    for i in range(0,len(som_data)): 
        cluster_col.append(som_data[i][len(som_data[0])-2])
    cluster_nparray=np.asarray(cluster_col)   
    clusters_unique=np.unique(cluster_nparray)
    for k in range(len(discrete_cmap)-1,-1,-1):
        if(k not in clusters_unique):
            discrete_cmap.pop(k)  
    for i in range(2,len(som_data[0])-3): 
        z=som_data[:,i]      
        ax=sns.boxplot(x=cluster_nparray.astype(float), y=z.astype(float), hue=cluster_nparray.astype(float) ,dodge=False, palette=discrete_cmap)       
        ax.set_title(som_headers[i])
        ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f')) 
        custom_lines=[]#dummy handle
        for j in range(0,len(cluster_tick_labels)):
            custom_lines.append(Line2D([0], [0], color='blue', lw=4))#only working way I found to make legened properly without handles, was to pass custom width 0 handles. 
        ax.legend(custom_lines,cluster_tick_labels,bbox_to_anchor=(1.05, 1),loc=0,handlelength=0,fontsize=8,handletextpad=0 ,borderaxespad=0.)   
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
    hits=np.zeros((somx,somy))   
    for i in range(0, len(som_dict['bmus'])):
        x=int(som_dict['bmus'][i][0])
        y=int(som_dict['bmus'][i][1])
        hits[x][y]+=1
    hits=np.transpose(hits)
    if(grid_type=='rectangular'):
        ax = sns.heatmap(hits, cmap="binary", linewidth=0)   
        ax.set_title("Number of hits per SOM cell")
    else: #if grid type is hexagonal
        mpl.rcParams.update({'font.size': 30})
        ax = plot_hexa(somx,somy,clusters,grid,hits.flatten(order='F'),annot_ticks,cluster_tick_labels,  colmap="binary", ptype='grid')    
        mpl.rcParams.update({'font.size': 32})  
        if(somy/somx>1.5):
            mpl.rcParams.update({'font.size': int(48/(somy/somx))})  #scale header font down if plot is narrow (i.e. x<y). This was a problem only in this, because the title is so long compared to the others
        #ax.set_title("Number of hits per SOM cell")
 
        mpl.rcParams.update({'font.size': 30})  
    #ax.figure.savefig(working_dir+'/Som/somplot_' +str(len(som_data[0])-2)+'.png',bbox_inches='tight')
    mpl.rcParams.update({'font.size': 12})
    plt.clf()
    plt.cla()
    plt.close()
    

"""
Run plotting scripts
"""          

if outgeofile is not None: #if spatial, draw geo plots
    if(dataType=='scatter'):
        if(max(geo_data[:,(4)])>0):#if clusters
            plot_geospace_clusters_scatter(geo_data)
        if(redraw!="false"):
            plot_geospace_results_scatter(geo_data, geo_headers, som_data)
        print("GeoSpace plots finished")
    else:
        if(max(geo_data[:,(4)])>0):#if clusters
            plot_geospace_clusters_grid(geo_data)
        if(redraw!="false"):
            plot_geospace_results_grid(geo_data, geo_headers, som_data)
        print("GeoSpace plots finished")
if(clusters>1): #draw som cluster plot if there is more than 1 cluster
    draw_som_clusters(som_data, som_table, annot_ticks, som_headers)

draw_umatrix(som_data, som_table,grid, annot_ticks, som_headers)
draw_number_of_hits()
#in case the function was called for redrawing after selecting a different clustering result. so that we can skip stuff we don't have to redraw to speed things up. CURRENTLY NOT IN USE, ALWAYS TRUE.
#if(redraw!="false"):
draw_som_results(som_data, som_table,grid, annot_ticks, som_headers)

print("SomSpace plots finshed")

if(som_dict['clusters'] is not None):
    draw_boxplots(som_dict,som_data)
print("Boxplots finished")

