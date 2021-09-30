# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:54:21 2019

@author: Sakari Hautala

Python script to visualize SOM calculation results & original data
"""
#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib as mpl
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    import seaborn as sns
    import sys
    import pandas as pd
    from loadfile import read_lrn_header
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
    import numpy as np; np.random.seed(0)
import os.path

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

som_data = np.genfromtxt(sys.argv[1],skip_header=(1), delimiter=' ')
output_folder=sys.argv[6]
som=pd.read_csv(sys.argv[1], delimiter=' ', header=None)
som_headers=som.iloc[0]                             #this might be quite expensive for just reading the headers. try to work around this.
input_file=sys.argv[5]
interactive_type=sys.argv[7]
if(input_file[-3:].lower()=="lrn"):                 
    header=read_lrn_header(sys.argv[5])  
    actualNumberOfColumns=header['cols']-1          #only thing read lrn header is used for is counting number of columns? replace this with something lighter?
    actualNumberOfColumns=len(som_headers)-3

counter=0

somx=int(sys.argv[2])
somy=int(sys.argv[3])
taulukko=np.zeros((somx,somy))    
som_clusters_table=[]
clusters=int(max(som_data[:,len(som_data[0])-1])+1)
discrete_cmap=sns.cubehelix_palette(n_colors=clusters, start=0, rot=0.4, gamma=1.0, hue=0.8, light=0.85, dark=0.15, reverse=False, as_cmap=False)
discrete_cmap_2=sns.cubehelix_palette(n_colors=clusters, start=0, rot=0.4, gamma=1.0, hue=0.8, light=0.85, dark=0.15, reverse=False, as_cmap=True)
cluster_ticks=[]
if(interactive_type!="Cluster"):
    for i in range (clusters,0,-1):
        cluster_ticks.append(i-1)   
else:
    for i in range (clusters+1,0,-1):
        cluster_ticks.append(i-1)   

geo_data=np.genfromtxt(sys.argv[4], skip_header=(1), delimiter=' ')
geofile = open(sys.argv[4], "r")
header_line = geofile.readline()
geo_headers=['#']
geo_headers = geo_headers +header_line.split(" ")
pivotted=[]
if(os.path.exists(output_folder+"/clickData2.txt")):
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
        for i in range(0, len(geo_data)):
            if(geo_data[i][2]==selected_x and geo_data[i][3]==selected_y):
                geo_data[i][4]=clusters 

if(max(geo_data[:,(4)])>0):     #create dataframe for geospace clusters, if there is more than 1 cluster. 
    x=geo_data[:,0]
    y=geo_data[:,1]
    z=geo_data[:,(4)] 
    df = pd.DataFrame.from_dict(np.array([x,y,z]).T)
    df.columns = ['X_value','Y_value','Z_value']
    df['Z_value'] = pd.to_numeric(df['Z_value'])
    pivotted= df.pivot('Y_value','X_value','Z_value')





############DASH############ 

if(interactive_type=="Cluster"):
    palette=sns.cubehelix_palette(n_colors=clusters, start=0, rot=0.4, gamma=1.0, hue=0.8, light=0.85, dark=0.15, reverse=False, as_cmap=False)
    formatted_palette=[]
else:
    palette=sns.cubehelix_palette(n_colors=clusters, start=0, rot=0.4, gamma=1.0, hue=0.8, light=0.85, dark=0.15, reverse=False, as_cmap=False)
    palette.append([0.00, 0.00, 0.00])
    formatted_palette=[]

for i in palette:
	formatted_value='rgb('
	for j in i:
		formatted_value=formatted_value+str("{:.2f}".format(j*255))+','
	formatted_value=formatted_value[:-1]    #remove last comma. replace this with python equivalent of a conditional operator?
	formatted_value=formatted_value+')' 
	formatted_palette.append(formatted_value)

palette=formatted_palette
clusterColorscale=[]
for i in range (0,clusters):
    clusterColorscale.append([float(float(i)/float(clusters)),palette[i]])
    clusterColorscale.append([float(float(i+1)/clusters),palette[i]])


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
    
if(interactive_type=="Cluster"):    
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
else:
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
        every_nth:_y=1
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
     