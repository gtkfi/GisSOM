# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 14:54:21 2019

@author: shautala

Python script to visualize SOM calculation results & original data. Uses dash to create and host a 
html page on localhost. Clicking on the plot will generate a static heatmap,
with only data from the selected cluster/som cell shown.

"""
import seaborn as sns
import math
import matplotlib.pyplot as plt
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import pandas as pd
import flask
from gevent.pywsgi import WSGIServer
import numpy as np
import threading
from plotting_functions import dash_draw_scatter
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
parser.add_argument('--data_type',dest="data_type",nargs='?', help='Type of input data (grid or scatter)')
args=parser.parse_args()

somfile=args.outsomfile  
output_folder=args.dir
somx=int(args.som_x)        
somy=int(args.som_y)       
outgeofile=args.outgeofile
input_file=args.input_file  
outgeofile=args.outgeofile
interactive_folder=args.interactive_dir
output_folder=args.dir                
gridshape=args.grid_type
dataType=args.data_type

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
base_y=-1
firstDraw=True

geo_data=np.genfromtxt(outgeofile, skip_header=(1), delimiter=' ')
geofile = open(outgeofile, "r")
header_line = geofile.readline()
geo_headers = header_line.split(" ")
output_column_names=[]
output_column_names.append({'label': "Cluster", 'value':0})
for i in range(2,len(som_data[0])-3):
    output_column_names.append({'label': geo_headers[int(len(som_data[0])-2+i)], 'value':str(i-1)})

som_array=np.zeros((somx,somy))       
for j in range(2,len(som_data[0])-2):    
    for i in range(0,len(som_data)): 
        som_array[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][j]  
        
if(int(max(som_data[:,len(som_data[0])-2]))>0): #if data has more than 1 cluster: build array for somspace clusters plot.
    for i in range(0,len(som_data)): 
        som_array[int(som_data[i][0])][int(som_data[i][1])]=som_data[i][len(som_data[0])-2]            
xinch=500
yinch=500
cluster_ticks=[]
for j in range (clusters,0,-1):
    cluster_ticks.append(j-0.5)                        
                        



server = flask.Flask(__name__)
app = dash.Dash(server=server)

"""
Create hexa grid plot and web page
"""
def run_hexa():
    global base_y

    xinch=somx*70-somx
    if(somx>somy):
        yinch=((somy*70)-somx*somy)   *(1+max(0.25,(somx+somy)*0.01))
    elif (somx==somy):
        yinch=somy*70-somy
    else:
        yinch=(somy*70)-somx*somy  
    scaleX=550/xinch #scale the resulting plot down
    scale='scale('+str(scaleX)+','+str(scaleX)+')'
    #yHeight=str(20)+'px'
    hexa_size=45#*max_width/xinch
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
            
        html.Div([html.H2(children='Selection Mode'),
                  dcc.RadioItems(
                    id='selection-type-radio',
                    options=[{'label': i, 'value': i} for i in ['Cluster', 'Som Cell']],
                    value='Cluster'
                )],style={'width': '29%','font-family': 'Verdana','position':'absolute','top':'80','left':'80'}),
        html.Div([       
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
                                                    }))
                                ],
                        layout = go.Layout(
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
                            )))      
                ),              
                html.Div(id='output',hidden=True)],style={'display': 'inline-block','transform': scale,'margin-top':'120px','transform-origin':'0 0','vertical-align': 'top','width':'49%','height':'20px'}),                          
        html.Div([
                html.Div([
                        html.H2(children='Select Output',style={ 'display': 'inline','white-space': 'nowrap'}),
                        dcc.Dropdown(
                            id='output-column-dropdown',
                            options=output_column_names,
                            value='0',
                            style={'font-family': 'Verdana','margin-top':'20px'}
                        ),
                html.Div(id='dd-output-container')],style={'width': '30%', 'display': 'inline-block','marginLeft':'80px','font-family': 'Verdana'}),
                html.Div([html.Img(id = 'cur_plot', src = '',style={'width': '100%','height':'10%', 'display': 'inline-block'}),html.Div(
                        dcc.Loading(id="ls-loading-1", children=[html.Div(id="ls-loading-output-1")], type="circle",fullscreen=True,style={'opacity': '0.5'}),                               
                )],style={'width': '100%','height':'100%', 'display': 'inline-block','position': 'relative'})],style={'width': '49%', 'display': 'inline-block','vertical-align': 'top','margin-top':'20px'})                      
    ])
                        
                        
                        
    
    


"""
Create square grid plot and web page
"""                        

def run_square():
    app.layout = html.Div([
            
            html.Div([     
                dcc.Location(id='url', refresh=False),
                html.H2(children='Selection Mode',style={'width': '49%', 'display': 'inline-block','marginLeft':'80px','font-family': 'Verdana'}),
                dcc.RadioItems(
                    id='selection-type-radio',
                    options=[{'label': i, 'value': i} for i in ['Cluster', 'Som Cell']],
                    value='Cluster',
                    style={'width': '49%', 'display': 'inline-block','marginLeft':'80px','font-family': 'Verdana'}
                ),
                dcc.Graph(        
                    id='heatmap',
                    figure=go.Figure(
                            data=[
                                    go.Heatmap(z=som_array.transpose(),
                                        colorscale=clusterColorscale, zmin=0, zmid=clusters/2, zmax=clusters,
                                        colorbar= {
                                            'tick0':1,
                                            'dtick': 1,
                                            'tickvals':cluster_ticks,
                                            'tickmode':"array",
                                            'ticktext':cluster_ticks_text
                                        })
                                 ],
                            layout = go.Layout(
                                    autosize=True,
                                    width=xinch,
                                    height=yinch,
                                    yaxis=dict(
                                        autorange='reversed'
                                        )
                                )
                        )
                
                ),
                html.Div(id='output')],style={'width': '49%', 'display': 'inline-block','vertical-align': 'top'}),                        
            html.Div([
                    html.Div([
                            html.H2(children='Select Output',style={'width': '49%', 'display': 'inline','font-family': 'Verdana'}),                         
                            dcc.Dropdown(
                                id='output-column-dropdown',
                                options=output_column_names,
                                value='0',
                                style={'font-family': 'Verdana','margin-top':'20px'}
                            ),
                    html.Div(id='dd-output-container')],style={'width': '30%', 'display': 'inline-block','marginLeft':'80px','font-family': 'Verdana','margin-top':'10px'}),
            html.Div([html.Img(id = 'cur_plot', src = '',style={'width': '100%','height':'10%', 'display': 'inline-block'}),
                      html.Div(
                                dcc.Loading(id="ls-loading-1", children=[html.Div(id="ls-loading-output-1")], type="circle",fullscreen=True,style={'opacity': '0.5'}),                           
                                                 
                      )],style={'width': '100%','height':'100%', 'display': 'inline-block','position': 'relative'})],style={'width': '49%', 'display': 'inline-block','vertical-align': 'top'})
                
    ])




    

cluster_ticks_text=[]
for i in range (clusters,0,-1):
    cluster_ticks_text.append(i-1)
    

if(gridshape!="hexagonal"):
    run_square()
    
else:
    run_hexa()
    
      

def convert_y_value_to_index(value):
    
    if(gridshape=="hexagonal"):
        return  (int(value/base_y)-1)
    else:
        return int(value)
    
def convert_x_value_to_index(value):
    if(gridshape=="hexagonal"):
        return (int(value)-1)
    else:
        return (int(value))
                  
    
def shutdown_server(): #define shutdown route and function
    http_server.stop()
@server.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'





def create_output_plot(ValueOfX,ValueOfY,ValueOfZ,outputColumn,selectionType):
          
    geo_data_selection=np.copy(geo_data)
    if(selectionType!="Cluster"):
        if(outputColumn==0):  
            for i in range(0, len(geo_data_selection)):
                if(geo_data_selection[i][2]==ValueOfX and geo_data_selection[i][3]==ValueOfY):
                    geo_data_selection[i][4]=clusters 
        else:#if selected column is not cluster col, the process will have to be reversed: in case of data col visualization, we can't really modify the continuous palette, so we'll have to set the non-selected areas to NaN:s and show them as white.
            for i in range(0, len(geo_data_selection)):
                if(geo_data_selection[i][2]!=ValueOfX or geo_data_selection[i][3]!=ValueOfY):
                    geo_data_selection[i][int(len(som_data[0])-1+outputColumn)]=np.NaN
                    
    else: #selectino type is cluster
        if(outputColumn>0): 
            for i in range(0, len(geo_data_selection)):
                if(int(geo_data_selection[i][4])!=ValueOfZ):
                    geo_data_selection[i][int((len(som_data[0])-1+outputColumn))]=np.NaN
        
    x=geo_data_selection[:,0]
    y=geo_data_selection[:,1]
    
    if(outputColumn==0):
        z=geo_data_selection[:,(4)] 
        cmap=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
        
        
        if(selectionType!="Cluster"):
            cmap.append([0.00,0.00,0.00,1]);#change this to appending so that the colorscale stays the same 
        if(selectionType=="Cluster"):
            for i in range(0, len(cmap)):   
                if (str(i)!=ValueOfZ):               
                    cmap[i].append(0.1) #instead of replacing with zero, modify the value to be much closer to zero 
                else:
                    cmap[i].append(1)
        else:
            for i in range(0, len(cmap)): 
                cmap[i].append(0.1)
                #last palette slot to black
        if(selectionType!="Cluster"):
            cmap[len(cmap)-1]=[0.00,0.00,0.00,1] 
    else:
        z=geo_data_selection[:,int(len(som_data[0])-1+outputColumn)]#skip som data values.
        cmap="jet"
    df = pd.DataFrame.from_dict(np.array([x,y,z],dtype=object).T)
    df.columns = ['X_value','Y_value','Z_value']
    df['Z_value'] = pd.to_numeric(df['Z_value'])
    pivotted= df.pivot('Y_value','X_value','Z_value')   
    palette_2=create_palette(selectionType,ValueOfZ)        
        
    if(dataType=="grid"):
        cluster_ticks=[]
        if(selectionType!="Cluster"):
            for i in range (clusters,0,-1):
                cluster_ticks.append(i-1)   
        else:
            for i in range (clusters+1,0,-1):
                cluster_ticks.append(i-1)   
        
        if(outputColumn==0): #if selected output was cluster:
            if(selectionType=="Cluster"):    #if selected input was cluster:
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
            ax.set_title(geo_headers[int(len(som_data[0])-1+outputColumn)])
            
            
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
    else: #if dataType=="scatter"
        cluster_ticks=[]
        cluster_tick_labels=[]
        if(selectionType!="Cluster"):
            for i in range (clusters,0,-1):
                cluster_ticks.append(i-1)   
                cluster_tick_labels.append(str(i-1))
        else:
            for i in range (clusters,0,-1): 
                cluster_ticks.append(i-1)   
                cluster_tick_labels.append(str(i-1))
            
        title=geo_headers[int(len(som_data[0])-1+outputColumn)]
        ax=dash_draw_scatter(geo_data_selection,som_data,palette_2,cluster_ticks,cluster_tick_labels,title,outputColumn,somx,somy,clusters)
    current_cmap = plt.cm.get_cmap()
    current_cmap=current_cmap.copy().set_bad(color='white')   
    plt.yticks(rotation=90)
    plt.yticks(ha='right')
    plt.yticks(va='bottom')
    plt.xticks(rotation=0)
    plt.xticks(ha='left')
    ax.invert_yaxis()
    plt.tight_layout()
    
    import io
    import base64
    s = io.BytesIO()
    ax.figure.savefig(s, format='png', dpi=300)
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,{}".format(s)

    

@app.callback(
    [dash.dependencies.Output('cur_plot', 'src'),dash.dependencies.Output("ls-loading-output-1","children")],
    [dash.dependencies.Input('heatmap', 'clickData'),   
     dash.dependencies.Input('output-column-dropdown','value'),
     dash.dependencies.Input('selection-type-radio','value'),
     dash.dependencies.Input('cur_plot', 'src')
     ])
def update_plot(clickData,outputColumn,selectionType,cur_plot_src):
    global firstDraw #this is not cool, but the only way I got it working
    if (clickData==None and firstDraw==True):
        firstDraw=False
        ValueOfX=0
        ValueOfY=0
        ValueOfZ=-1
    elif(clickData==None and firstDraw==False):
        return cur_plot_src,None
    else:
        ValueOfX=int(clickData["points"][0]['x'])
        ValueOfY=float(clickData["points"][0]['y'])
        ValueOfX=convert_x_value_to_index(ValueOfX)
        ValueOfY=convert_y_value_to_index(ValueOfY)
        ValueOfZ=None    
        if ('z' in clickData["points"][0]):
            ValueOfZ=int(clickData["points"][0]['z'])    
        else:
            ValueOfZ=int(clickData["points"][0]['text'])
    return create_output_plot(ValueOfX,ValueOfY,ValueOfZ,int(outputColumn), selectionType),clickData


def create_palette(selectionType,ValueOfZ):
    #create palette
    palette=sns.cubehelix_palette(n_colors=clusters, start=1,rot=4, gamma=1.0, hue=3, light=0.77, dark=0.15, reverse=False, as_cmap=False)
    #if(selectionType!="Cluster"):
    #    palette.append([0.00,0.00,0.00,1]);#change this to appending so that the colorscale stays the same 
    if(selectionType=="Cluster"):
        for i in range(0, len(palette)):   
            if (i!=ValueOfZ):               
                palette[i].append(0.1) #instead of replacing with zero, modify the value to be much closer to zero 
            else:
                palette[i].append(1)
    else:
        for i in range(0, len(palette)): #does this produce a long enough palette?
            palette[i].append(0.1)
            #last palette slot to black
    if(selectionType!="Cluster"):
        palette.append([0.00,0.00,0.00,1]);
    #if(selectionType!="Cluster"):
     #    palette[len(palette)-1]=[0.00,0.00,0.00,1] 
    
    return palette

timer = threading.Timer(600.0, shutdown_server) #10 min timer for shutdown, so the process doesn't run forever in the background in case there are problems with sending the shutdown message.
timer.start() 
application = app.server    #Launch application. 
if __name__ == '__main__':
   http_server = WSGIServer(("", 8050), application)
   try:
      http_server.serve_forever()
   except:
      print("Server socket is occupied. Close previous plot and try again.")
   