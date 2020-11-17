# -*- coding: utf-8 -*-
"""
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
    from matplotlib.collections import RegularPolyCollection
    import matplotlib as mpl
    import math
    import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

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
som_headers=som.iloc[0]                             
input_file=sys.argv[5]
interactive_type=sys.argv[7]
if(input_file[-3:].lower()=="lrn"):                 
    header=read_lrn_header(sys.argv[5])  
    actualNumberOfColumns=header['cols']-1         
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
    width, height = fig.canvas.get_width_height()
    ypix = height - ypix
    if(ptype=='scatter'): #if the data type is csv with gaps
        apothem=(xpix[1] - xpix[0]) 
        area_inner_circle = abs(apothem) 
        collection_bg = RegularPolyCollection(
            numsides=4,  
            rotation=150,
            sizes=(area_inner_circle,),
            edgecolor="none",
            array= d_matrix,
            cmap = colmap,
            offsets = n_centers,
            transOffset = ax.transData,
        )
    else: #regular hexa plot
        apothem = 1.8 * (xpix[1] - xpix[0]) / math.sqrt(3)
        area_inner_circle = math.pi * (apothem ** 2)
        collection_bg = RegularPolyCollection(
            numsides=6,  
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
    cax = divider.append_axes("right", size="10%", pad=0.05)
    if(colmap=='jet'):
        cbar=plt.colorbar(collection_bg, cax=cax)
        cbar.ax.invert_yaxis()
        cbar.ax.tick_params(axis='y', direction='out', pad=30)
    else:
        colmap2=colmap
        bounds = np.linspace(0, clusters, clusters+1)
        bounds2 = np.linspace(0.5, clusters+0.5, clusters+1.5)
        norm = mpl.colors.BoundaryNorm(bounds, colmap2.N)
        cbar=mpl.colorbar.ColorbarBase(cax, cmap=colmap2, norm=norm,
        spacing='proportional', ticks=bounds2, boundaries=bounds, format='%1i')
        cbar.ax.invert_yaxis()
        cbar.ax.tick_params(axis='y', direction='out', pad=30)
    plt.gca().invert_yaxis()
    return ax


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
	formatted_value=formatted_value[:-1]    #remove last comma.
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
    
centers=[]     
for i in range(0, len(geo_data)):	
    centers.append([geo_data[i][0],geo_data[i][1]])
grid={'centers':np.array(centers), 
      'x':np.array([len(geo_data)]),
      'y':np.array([len(geo_data)])}


x=geo_data[:,0]
y=geo_data[:,1]
z=geo_data[:,(4)]  
sns.set_style("ticks", {"xtick.major.size": 8, "ytick.major.size": 8})
mpl.rcParams.update({'font.size': 30})
ax = plot_hexa(grid, z,title="clusters",colmap=ListedColormap(palette_2), ptype='scatter')   
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







































