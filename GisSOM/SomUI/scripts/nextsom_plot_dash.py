# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:54:21 2019

@author: shautala

Python script to visualize SOM calculation results & original data. Uses dash to create and host a 
html page on localhost. Clicking on the plot will write selected cluster number or som cell x and y coordinates to a file.
That file is monitored for changes in the ViewModel, and upon change a new heatmap is drawn
with only data from the selected cluster/som cell .

"""
import seaborn as sns
import math
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import flask
from gevent.pywsgi import WSGIServer
import numpy as np
import threading
import os.path
import argparse
"""
inputs:
1)outSomFile
2)som_x
3)som_y
4)outGeoFile
5)Model.InputFile
6)interactiveFolder
7)Model.Output_folder
8) grid shape
"""
parser = argparse.ArgumentParser(description='Script for drawing reulting plot of interactive selection')
parser.add_argument('--outsomfile',nargs='?',dest="outsomfile", help='Som calculation somspace output text file')
parser.add_argument('--som_x',nargs='?', dest="som_x", help='som x dimension')
parser.add_argument('--som_y',nargs='?',dest="som_y", help='som y dimension')
parser.add_argument('--outgeofile', default=None, dest="outgeofile", help='#som geospace results txt file')
parser.add_argument('--input_file',nargs='?', dest="input_file",help='Input file(*.lrn)')
parser.add_argument('--interactive_dir',dest="interactive_dir",nargs='?', help='Interactive directory folder')
parser.add_argument('--dir',nargs='?',dest="dir", help='Output folder')
parser.add_argument('--grid_type', dest="grid_type",nargs='?', help='grid type (square or hexa)')
args=parser.parse_args()

somfile=args.outsomfile  #som results txt file
output_folder=args.dir
somx=int(args.som_x)        #som x parameter
somy=int(args.som_y)        #som y parameter
outgeofile=args.outgeofile
input_file=args.input_file  #original input file 
outgeofile=args.outgeofile
interactive_folder=args.interactive_dir
output_folder=args.dir                #output directory of GisSOM 
gridshape=args.grid_type



###############################
# initialize common variables #
###############################

som_data = np.genfromtxt(somfile,skip_header=(1), delimiter=' ')


clusters=int(max(som_data[:,len(som_data[0])-2])+1)#number of clusters

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






#################################################
# Initialize dash app, and host it on localhost #
#################################################





"""
Create hexa grid plot and web page
"""
def run_hexa():
    #baseUnit=70
    xinch=somx*70-somx
    if(somx>somy):
        yinch=((somy*70)-somx*somy)   *(1+max(0.25,(somx+somy)*0.01))#(1+((somx/somy)/10)) 1.25 luokkaa pitää olla mutta pitää kasvaa eron kasvaessa. 30 ja 10 rikkoo jo.
    elif (somx==somy):
        yinch=somy*70-somy
    else:
        yinch=(somy*70)-somx*somy 
    #hexa_size=min(somx,somy)*4.5 -min(somx,somy)+10
    
    hexa_size=45
    centers=[]
    base_y=((math.sqrt(3)/2))
    if somx>somy:
        base_y=base_y*(somx/somy)
    centers_x=[]
    centers_y=[]
    for i in range(0, somx):
        for j in range(0, somy):
            if (j%2==0):
                base_x=0
            else:
                base_x=0.50
            centers.append([(i+1)+base_x,(j+1)*base_y])#+1 to convert from index to value
            centers_x.append((i+1)+base_x)
            centers_y.append((j+1)*base_y)

    hits=som_data[:,len(som_data[0])-2]
    
    font_size=1.8*(math.sqrt(somx*somy))
    cluster_ticks=[]
    mystery_extra=0
    if(clusters<8):
        mystery_extra=((7-clusters)**2)/100
    for j in range (clusters,0,-1):
        cluster_ticks.append(j-1+(0.5-(j/clusters))+mystery_extra)#for whatever reason, the numeric scale on the colorbar of plotly's scatterplot differs from the above heatmap's, and seems to follow no reason or logic, so the tick indices must be modified accordingly. The above formula gets it close enough.
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
        colorbar= {
                                'tick0':0,
                                'dtick': 1,
                                'tickvals':cluster_ticks,
                                'tickmode':"array",
                                'ticktext':cluster_ticks_text
                                
                            },
    )
                        )
                     ]
                ,layout = go.Layout(
                        font=dict(
                            size=font_size
                        ),
                        
                        autosize=True,
                        width=xinch,
                        height=yinch,
                        yaxis=dict(
                        autorange='reversed', visible=False, showticklabels=False
                        ),
                        xaxis=dict(
                        visible=False, showticklabels=False
                        )
                    )
                )
    
            ),
        html.Div(id='output',hidden=True)
    ])
                        
                        
                        
                        
                        
                        
                        
"""
Create square grid plot and web page
"""                        
def run_square():
    taulukko=np.zeros((somx,somy))       
    for j in range(2,len(som_data[0])-2):    
        for i in range(0,len(som_data)): 
            taulukko[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][j]  
            
    if(int(max(som_data[:,len(som_data[0])-2]))>0): #if data has more than 1 cluster: build array for somspace clusters plot.
        for i in range(0,len(som_data)): 
            taulukko[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][len(som_data[0])-2]            
    xinch=500#xinch/2
    yinch=500#yinch/2
    cluster_ticks=[]
    for j in range (clusters,0,-1):
        cluster_ticks.append(j-0.5)
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
                            autosize=True,
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






server = flask.Flask(__name__)
cluster_ticks_text=[]
for i in range (clusters,0,-1):
    cluster_ticks_text.append(i-1)
    
app = dash.Dash(server=server)
if(gridshape!="hexagonal"):
    run_square()
    
else:
    run_hexa()
    
                        

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
        ValueOfX=clickData["points"][0]['x']
        ValueOfY=clickData["points"][0]['y']
        ValueOfZ=clickData["points"][0]['z']          
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
    
timer = threading.Timer(600.0, shutdown_server) #10 min timer for shutdown, so the process doesn't run forever in the background in case there are problems with sending the shutdown message.
timer.start() 
application = app.server    #Launch application. 
if __name__ == '__main__':
   http_server = WSGIServer(("", 8050), application)
   try:
      #test=requests.post('https://localhost:8050/shutdown')
      http_server.serve_forever()
   except:
      print("Server socket is occupied. Close previous plot and try again.")
   

