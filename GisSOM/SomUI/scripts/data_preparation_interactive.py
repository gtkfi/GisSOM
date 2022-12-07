# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 12:38:19 2022

@author: shautala
"""


import dash
from dash import dcc
from dash import html
import flask
from gevent.pywsgi import WSGIServer
import dash_bootstrap_components as dbc
import io
import base64
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output, State
from split_to_columns_interactive import readInputData
from edit_column_interactive import edit_column
from draw_histogram_interactive import draw_histogram
from combine_to_lrn_file_interactive import combine_to_lrn_file
import copy
import argparse
import threading
#import base64

parser = argparse.ArgumentParser(description='Script for drawing reulting plot of interactive selection')
parser.add_argument('--input_file',nargs='?',dest="inputFile", help='input file used for som calculation')
parser.add_argument('--output_folder',nargs='?', dest="outputFolder", help='output folder')
parser.add_argument('--data_shape',nargs='?',dest="dataShape", help='grid or scatter data')
args=parser.parse_args()

input_file=args.inputFile
output_folder=args.outputFolder
dataShape=args.dataShape
input_type=input_file[-3:].lower()
selected_column='0'
firstLoad=True#don't look at me i'm hideous
firstLoad2=True

data=readInputData(input_file,input_type)
data_original=copy.copy(data["data"])
headers=data["data"][7,:]
column_names=[]
for i in range(0,len(headers)):
    column_names.append({'label': str(headers[i]), 'value':str(i)})


server = flask.Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],server=server)
def generate_column_checklist_row(column_name,column_index):
    return dbc.Row([
        html.Div([html.Span(str(column_name),id=(str("btn_t_"+column_name+"_"+str(column_index))), style={'display': 'inline-block','width':'40%'}),dcc.RadioItems((str("rd_"+str(column_index))),[
            {'label':' x','value':'data'},#
            {'label':' x','value':'x'},
            {'label':' x','value':'y'},
            {'label':' x','value':'label'},
            {'label':' x','value':'exclude'}],'data', style={'display': 'inline-block','color':'white'})])#,style={'width': '10%'})])#,inline=True,),
             ])#,style=dict(display='flex'))
    
def generate_column_selections(column_name,column_index):
    return html.Option([html.Div([dcc.RadioItems(id=(str("rd_"+column_name)),options=['data','x','y','label','exclude'])],style={'width': '40%'})])


    


def run():
    app.layout = dbc.Container(
        [
            dbc.Row(children=[
                dbc.Col(html.H1("Data preparation"),md=4),dbc.Col(html.H6(["Before proceeding: ",html.Br(),"1. Check that the spatial parameters are correctly defined (Easting, Northing) ",html.Br(),"2. Optionally exclude the parameters that should not be used in clustering"] ),md=8)]),
            #html.H1("Data preparation"),
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(children=[
                        dbc.Row(
                            dbc.Col(children=[  
                                dcc.Checklist(id="spatialCheckList",
                                              options=[{"label":"Spatial data","value":"spatial"}],
                                              value=[]),
                                html.Div([dcc.Input(id='na_value',type="text",value=data['noDataValue'],style={'width': '20%', 'height': 30,'marginBottom':5,'marginRight':10}),dash.html.Label("NoData value")],style=dict(display='flex',marginTop=5))
                                #,html.Table(children=[generate_column_table_row(headers[i],i) for i in range(0,len(headers))])
                                ])),
                        dbc.Row([
                           html.Div([html.Span("",id=(str("span_dummy")), style={'display': 'inline-block','width':'40%'}),
                                     html.Span("data",id=(str("column_type_headers_data")),style= {'writing-mode': 'vertical-rl','text-orientation': 'mixed'}),
                                     html.Span("x",id=(str("column_type_headers_x")),style= {'writing-mode': 'vertical-rl','text-orientation': 'mixed'}),
                                     html.Span("y",id=(str("column_type_headers_y")),style= {'writing-mode': 'vertical-rl','text-orientation': 'mixed'}),
                                     html.Span("label",id=(str("column_type_headers_label")),style= {'writing-mode': 'vertical-rl','text-orientation': 'mixed'}),
                                     html.Span("exclude",id=(str("column_type_headers_ex")),style= {'writing-mode': 'vertical-rl','text-orientation': 'mixed'})
                                     ])
                                
                                 ]),
                        dbc.Row(
                            dbc.Col(children=[generate_column_checklist_row(headers[i],i) for i in range(0,len(headers))],id='column_type_host'))],md=3)
                    ,
                    dbc.Col(html.Div([
                        dcc.Dropdown(
                            id='column-dropdown',
                            options=column_names,#replace this with a list of column names.
                            value='1',
                            style={'font-family': 'Verdana','margin-top':'20px'}),
                        html.Div(id='column_dummy', style={'display': 'none'}),
                        html.Div(id='plot_trigger', style={'display': 'none'}),
                        html.Img(id = 'cur_plot', src = '',style={'width': '100%','height':'10%', 'display': 'inline-block'}),
                        html.Div(dcc.Loading(id="ls-loading-1", children=[html.Div(id="ls-loading-output-1")], type="circle",fullscreen=True,style={'opacity': '0.5'}))
                        ]),md=6),

                    dbc.Col(html.Div([
                        dcc.Checklist(id="LogWinChecklist",
                            options=[{"label":"Log Transform", "value":"log"}, {"label":"Winsorize (original values)", "value":"winsorize"}],
                            value=[],
                            labelStyle={'display': 'block'},
                        ),
                        html.Div([dcc.Input(id='minWin',type="number",value=0,style={'width': '20%', 'height': 30,'marginLeft':25,'marginBottom':5,'marginRight':10}),dash.html.Label("Min limiting value")],style=dict(display='flex',marginTop=5)),
                        html.Div([dcc.Input(id='maxWin',type="number",value=0,style={'width': '20%', 'height': 30,'marginLeft':25,'marginBottom':5,'marginRight':10}),dash.html.Label("Max limiting value")],style=dict(display='flex',marginBottom=10)),
                        html.Button('Save edits', id='save_col',n_clicks=0),
                        
                        dcc.Checklist(id="ScaleChecklist",
                            options=[{"label":"Scale data","value":"scale"}],
                            value=["scale"],
                            style={'marginTop':80}
                        ),
                        html.Div([dcc.Input(id='scalemin',type="number",value=0,style={'width': '20%', 'height': 30,'marginLeft':25,'marginBottom':5,'marginRight':10}),dash.html.Label("Scaling Min value")],style=dict(display='flex',marginTop=5)),
                        html.Div([dcc.Input(id='scalemax',type="number",value=1,style={'width': '20%', 'height': 30,'marginLeft':25,'marginBottom':5,'marginRight':10}),dash.html.Label("Scaling max value")],style=dict(display='flex',marginBottom=10)),
                        html.Div(id='dummy', style={'display': 'none'}),
                        html.Button('Next', id='submit-val')]),md=3),
                        html.Div(dcc.Loading(id="ls-loading-2", children=[html.Div(id="ls-loading-output-2")], type="circle",fullscreen=True,style={'opacity': '0.5'}))
                        
                      
                ],
                align="start",
            ),
        ],
        fluid=True,
    )


run()

def shutdown_server(): 
    http_server.stop()
@server.route('/shutdown', methods=['POST'])
def shutdown():
    global health_check_timer
    if health_check_timer is not None:
        health_check_timer.cancel()
    shutdown_server()
    return 'Server shutting down...'
"""
@server.route('/loadfile/<filepath>', methods=['POST'])#filepath should be base64 encoded
def loadfile(filepath):

    path=base64.b64decode(filepath)
    load_data(path)
    return 'Loading input data...'
"""

@server.route('/deadman', methods=['POST'])
def deadman():
    global health_check_timer
    health_check_timer.cancel()
    health_check_timer = threading.Timer(35.0, shutdown_server)
    health_check_timer.start()
    return 'OK'   
    

@app.callback(
    [Output('cur_plot', 'src'),
     Output("ls-loading-output-1","children"),
     Output("column_dummy","children")
     ],
    [Input(component_id='column-dropdown',component_property='value'),
     Input(component_id='cur_plot', component_property='src'),
     Input(component_id='plot_trigger',component_property='children'
     )
     ],
    State("na_value","value"))
def update_histogram(value,src,dummy_trigger,noData):
    column_to_draw=data["data"][:,int(value)]
    histogram=draw_histogram(input_file,column_to_draw, noData) 
    s = io.BytesIO()
    histogram.figure.savefig(s, format='png', dpi=300)
    plt.close()
    s = base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return "data:image/png;base64,{}".format(s),"",value



@app.callback(
    #Output('cur_plot', 'src'),
     [Output("LogWinChecklist","value"),
     Output("minWin","value"),
     Output("maxWin","value"),
     Output("scalemin","value"),
     Output("scalemax","value")],   
    [Input(component_id='column_dummy', component_property='children')])  
def load_edits(column):
    
    selected_column=data["data"][:,int(column)]
    is_winsorized=selected_column[0]
    win_min=selected_column[1]
    win_max=selected_column[2]
    is_log_transformed=selected_column[3]
    #exclusion=selected_column[4]
    scale_min=selected_column[5]
    scale_max=selected_column[6]
    log_win_value=[]
    if(is_log_transformed=='true'):
        log_win_value.append("log")
    if(is_winsorized=='true'):
        log_win_value.append("winsorize")#Why are these grouped in one variable?
    
    return log_win_value,win_min,win_max,scale_min,scale_max


@app.callback(
    [Output("plot_trigger","children")],        
    [Input('save_col','n_clicks')],
    [State('LogWinChecklist','value'),
           State('minWin', 'value'),
           State('maxWin', 'value'),
           State('column_dummy', 'children'),
           State('scalemin','value'),
           State('scalemax','value')]
    )
def save_edits(n_clicks,LogWin,minWin,maxWin,column,scalemin,scalemax):
    global firstLoad2 #this is not cool, but the only way I got it working. I couldn't find any decent way to prevent dash buttons from firing their event on page load.
    if(firstLoad2==False):
        log_transformed='false'
        winsorized='false'
        if "log" in LogWin:
            log_transformed='true'
        if "winsorize" in LogWin:
            winsorized='true'
        original_values=copy.copy(data_original[:,int(column)])
        edited_column=edit_column(original_values,winsorized,minWin,maxWin,log_transformed,0,scalemin,scalemax,noData=None)
        data["data"][:,int(column)]=edited_column
    else:
        firstLoad2=False;
    return [""]




@app.callback([Output("dummy","children"),
              Output("ls-loading-output-2","children")],
              Input("submit-val","n_clicks"),
              State("column_type_host","children"),
              State("na_value","value"),
              State("ScaleChecklist","value"),
              State("spatialCheckList","value"))
def create_lrn(n_clicks,column_type_host,na_value,scaled,spatial):
    global firstLoad #this is not cool, but the only way I got it working
    if(firstLoad==False):
        column_types=[]
        is_scaled=False
        is_spatial=False
        if("spatial" in spatial):
            is_spatial=True
        if "scale" in scaled:
            is_scaled=True
        for i in range(0,len(headers)):       
            column_types.append(column_type_host[i]['props']['children'][0]['props']['children'][1]['props']['value'])
        try:
            combine_to_lrn_file(input_file,output_folder,data["data"],column_types,is_scaled,is_spatial,na_value)
            #print("Saved to .lrn file")
        except ValueError as err:
            print('Error:', err)
        
        
    else:
        firstLoad=False;
    return [""],n_clicks

"""
def load_data(input_file):
    data=readInputData(input_file,inputType)
    data_original=copy.copy(data["data"])
    headers=data["data"][7,:]
    #headers=data["data"][7,:].compute()
    column_names=[]
    for i in range(0,len(headers)):
        column_names.append({'label': str(headers[i]), 'value':str(i)})
    return #column names ja data. mietippä sit miten noita ajetaan, onko global muuttujaa (hyi) vai joku elementti, en tiä onko se sit sen parempi
"""    

health_check_timer = threading.Timer(999.0, shutdown_server) #default timer for shutdown, if no message from UI is received
health_check_timer.start() 
print("Data preaparation page ready")
application = app.server    #Launch application. 
if __name__ == '__main__':
   http_server = WSGIServer(("", 8051), application)
   try:
      http_server.serve_forever()
   except:
      print("Server socket is occupied. Close previous plot and try again.")

