# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:54:21 2019

@author: shautala

Python script to visualize SOM calculation results & original data. Uses dash to create and host a 
html page on localhost. Clicking on the plot will write selected cluster number to a file,
that file is monitored for changes in the ViewModel, and upon change a new heatmap is drawn
with only the selected cluster.

"""
import matplotlib as mpl
import seaborn as sns
import sys
import pandas as pd
import math
import json
import matplotlib.pyplot as plt
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import flask
from gevent.pywsgi import WSGIServer
from loadfile import read_lrn_header
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.collections import RegularPolyCollection
import threading
import os.path
"""
inputs:
1)outSomFile
2)som_x
3)som_y
4)outGeoFile
5)Model.InputFile
6)interactiveFolder
7)Model.Output_folder
8) grid shape?
"""

somfile=sys.argv[1]
somx=int(sys.argv[2])
somy=int(sys.argv[3]) 
input_file=sys.argv[5]
interactive_folder=sys.argv[6]
output_folder=sys.argv[7]
gridshape=sys.argv[8]

som_data = np.genfromtxt(sys.argv[1],skip_header=(1), delimiter=' ')
som=pd.read_csv(somfile, delimiter=' ', header=None)
som_headers=som.iloc[0] 
if(input_file[-3:].lower()=="lrn"):
    header=read_lrn_header(input_file)    
    actualNumberOfColumns=header['cols']-1          
else:
    actualNumberOfColumns=len(som_headers)-3


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
            colmap='jet'):
   
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
    

    apothem = 1.8 * (xpix[1] - xpix[0]) / math.sqrt(3)#.9
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
    else:
        colmap2=colmap
        bounds = np.linspace(0, clusters, clusters+1)
        bounds2 = np.linspace(0.5, clusters+0.5, clusters+1.5)
        norm = mpl.colors.BoundaryNorm(bounds, colmap2.N)
        cbar=mpl.colorbar.ColorbarBase(cax, cmap=colmap2, norm=norm,
        spacing='proportional', ticks=bounds2, boundaries=bounds, format='%1i')
        cbar.ax.invert_yaxis()
    plt.gca().invert_yaxis()
    return ax

x=somx
y=somy
centers=[]
x2=[];
y2=[];
base_y=((math.sqrt(3)/2))
if somx>somy:
    base_y=base_y*(somx/somy)
centers_x=[]
centers_y=[]
for i in range(0, x):
    for j in range(0, y):
        if (j%2==0):
            base_x=0
        else:
            base_x=0.50
        centers.append([(i+1)+base_x,(j+1)*base_y])#+1 to convert from index to value
        centers_x.append((i+1)+base_x)
        centers_y.append((j+1)*base_y)
        x2.append((i+1)+base_x)
        y2.append((j+1)*base_y)

grid={'centers':np.array(centers), 
      'x':np.array([float(x)]),
      'y':np.array([float(y)]),
      }
hits=som_data[:,len(som_data[0])-1]

som_d = {'x': centers_x, 'y': centers_y}
som_df = pd.DataFrame(data=som_d)
taulukko=np.zeros((somx,somy))    

for j in range(2,len(som_data[0])-1):    
    for i in range(0,len(som_data)): 
        taulukko[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][j]  

clusters=int(max(som_data[:,len(som_data[0])-1])+1)#number of clusters

if(int(max(som_data[:,len(som_data[0])-1]))>0): #if data has more than 1 cluster: build array for somspace clusters plot.
    for i in range(0,len(som_data)): 
        taulukko[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][len(som_data[0])-1]

palette=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
formatted_palette=[]
discrete_cmap_2=sns.cubehelix_palette(n_colors=clusters, start=0, rot=0.4, gamma=1.0, hue=0.8, light=0.85, dark=0.15, reverse=False, as_cmap=True)
for i in palette:   #format color values to format rgb(x,y,x), where x y and z are values between 0 and 255. values before conversion are in format a,b,c where a b and c are values between 0 and 1
	formatted_value='rgb('
	for j in i:
		formatted_value=formatted_value+str("{:.2f}".format(j*255))+','
	formatted_value=formatted_value[:-1] #remove last comma
	formatted_value=formatted_value+')' 
	formatted_palette.append(formatted_value)

palette=formatted_palette   #Format palette in to colorscale. for example 10 clusters: (0,0.1,rgb_val), (0.1,0.2 rgb_val_2),...... ,(0.9,1,rgb_val_x)
clusterColorscale=[]        #so each cluster is assigned a specific color.
for i in range (0,clusters):
    clusterColorscale.append([float(float(i)/float(clusters)),palette[i]])
    clusterColorscale.append([float(float(i+1)/clusters),palette[i]])
ValueOfZ_2="0"

baseUnit=70
xinch=somx*70-somx
if(somx>somy):
    yinch=((somy*70)-somx*somy)*(somx/somy)
else:
    yinch=(somy*70)-somx*somy
hexa_size=min(somx,somy)*4.5



##########################DASH##########################

server = flask.Flask(__name__)
cluster_ticks_text=[]
for i in range (clusters,0,-1):
    cluster_ticks_text.append(i-1)

cluster_ticks=[]
for j in range (clusters,0,-1):
    cluster_ticks.append(j-0.5)
app = dash.Dash(server=server)
if(gridshape!="hexagonal"):
    app.layout = html.Div([     
        dcc.Location(id='url', refresh=False),
        dcc.Graph(        
            id='heatmap',
            figure=go.Figure(
                    data=[
                            go.Heatmap(z=taulukko.transpose(),
                            colorscale=clusterColorscale, zmin=0, zmid=clusters/2, zmax=clusters,
                            colorbar= {
                                'tick0':1,
                                'dtick': 1,
                                'tickvals':cluster_ticks,
                                'tickmode':"array",
                                'ticktext':cluster_ticks_text
                            })
                         ]
                    ,layout = go.Layout(
                        yaxis=dict(
                            autorange='reversed'
                            )
                        )
                    )
        
                ),
            html.Div(id='output')
        ])

else:
    app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Graph(        
        id='heatmap',
        figure=go.Figure(
                data=[
                        go.Scatter(
                                x=centers_x, y = centers_y, text=hits,hovertext=hits,
    mode='markers',
    marker=dict(
        size=hexa_size,
        symbol='hexagon',
        color=hits, #set color equal to a variable
        colorscale=clusterColorscale, 
        showscale=True
    )
                        )
                     ]
                ,layout = go.Layout(
                        
                        autosize=False,
                        width=xinch,
                        height=yinch,
                        yaxis=dict(
                        autorange='reversed'
                        )
                    )
                )
    
            ),
        html.Div(id='output')
    ])

def shutdown_server(): #define shutdown route and function
    http_server.stop()
@server.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.callback( #defining callback functions: these provide the interactivity
    Output('output', 'children'),
    [Input('heatmap', 'hoverData'),
     Input('heatmap', 'clickData'),
     dash.dependencies.Input('url', 'pathname')])
def display_hoverdata(hoverData, clickData,pathname):
    if pathname =='/shutdown':
        shutdown()
    if(clickData is not None):
        with open(output_folder+'/clickData.txt', 'w') as f:
            for item in clickData["points"]:
                f.write("%s\n" % item)    
    if(os.path.isfile(output_folder+'/clickData.txt')):
        with open (output_folder+"/clickData.txt", "r") as myfile:
            data=myfile.readline()
            dataDict=eval(data)
            dataDict.pop('pointIndex',None)
            data=str(dataDict)
            indexOfX=data.find('x')
            stringFromX=data[indexOfX:]
            endOfX=stringFromX.find(',')        
            if(gridshape!='hexagonal'):
                ValueOfX=data[indexOfX+4:indexOfX+endOfX]
            else:
                ValueOfX=math.floor(float(data[indexOfX+4:indexOfX+endOfX]))
            indexOfY=data.find('y')
            stringFromY=data[indexOfY:]
            endOfY=stringFromY.find(',')        
            if(gridshape!='hexagonal'):
                ValueOfY=data[indexOfY+4:indexOfY+endOfY]
            else:
                ValueOfY=math.floor(float(data[indexOfY+4:indexOfY+endOfY])*((math.sqrt(3)/2)))
            indexOfZ=data.find('z')
            if(indexOfZ>-1):
                stringFromZ=data[indexOfZ:]
                endOfZ=stringFromZ.find('}')
                ValueOfZ=data[indexOfZ+4:indexOfZ+endOfZ]
            else:
                if(clickData is not None):              
                    points=clickData["points"]
                    ValueOfZ=points[0]["text"]
        if(os.path.isfile(output_folder+'/clickData2.txt')):
            with open (output_folder+"/clickData2.txt", "r") as clickData2:
                x=clickData2.readline()
                x=x.replace("\n","")
                y=clickData2.readline()
                y=y.replace("\n","")
                z=clickData2.readline()
                z=z.replace("\n","")
                if(z!=ValueOfZ or x!=ValueOfX or y!=ValueOfY):
                    with open(output_folder+'/clickData2.txt', 'w') as f:
                        f.write("%s\n" % ValueOfX)
                        f.write("%s\n" % ValueOfY)
                        f.write("%s\n" % ValueOfZ)
                    with open(interactive_folder+'/clickData2.txt', 'w') as f:
                        f.write("%s\n" % ValueOfX)
                        f.write("%s\n" % ValueOfY)
                        f.write("%s\n" % ValueOfZ)                                                     
    return [
        json.dumps(hoverData, indent=2),
        html.Br(),
        json.dumps(clickData, indent=2)        
    ]
timer = threading.Timer(3600.0, shutdown_server) #One hour timer for shutdown, so the process doesn't run forever in the background in case there are problems with sending the shutdown message.
timer.start() 
application = app.server    #Launch application. Will serve until shut down. 
if __name__ == '__main__':
   http_server = WSGIServer(("", 8050), application)
   http_server.serve_forever()

