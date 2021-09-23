# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:03:49 2019

@author: shautala

Script for combining individual data columns back to a .lrn file. This lrn file is used as input for som calculation.
For CSV files it is possible to use non-spatial data, in this case this script will output a lrn file 
with x- and y- cols filled with zeroes, for internal use. Final program output will not contain these dummy columns.
"""

import argparse
#from loadfile import load_input_file,  read_header
from nextsomcore.loadfile import load_input_file,  read_header
import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import pandas as pd
import os
import ast
"""
inputs:
 1) Model.InputFile 
 2) Model.EastingColumnIndex 
 3) Model.NorthingColumnIndex 
 4) Model.Output_Folder 
 5) Model.NoDataValue 
"""
parser = argparse.ArgumentParser(description='Script for generating self organizing maps')

parser.add_argument('--input_file',nargs='?', help=' #input file path, only reads headers and notes from this')
parser.add_argument('--eastingIndex', default=None, dest="eastingIndex", help='#index of easting column, if data is spatial')
parser.add_argument('--northingIndex', default=None, dest="northingIndex", help='#index of northing column, if data is spatial')
parser.add_argument('--output_folder',nargs='?', help=' #output folder path, also reads the columns used to build the result file form this directory.')
parser.add_argument('--na_value', default="", dest="na_value", help='#NA/null value to remove if data contains them')
parser.add_argument('--normalized', default=None, dest="normalized", help='#if data should be normalized')
parser.add_argument('--min_N', default=None, dest="min_N",help="minimum value used for normalization scale")
parser.add_argument('--max_N' , default=None,dest="max_N",help="maximum value used for normalization scale")
parser.add_argument('--exclude_list',default=None, dest="exclude_list", help="List of booleans, whether columns are included or excluded") 
parser.add_argument('--scale_min_list',default=None, dest="scale_min_list", help="List of floats for scaling minimum values") 
parser.add_argument('--scale_max_list',default=None, dest="scale_max_list", help="List of floats for scaling maximum values") 
parser.add_argument('--log_transform_list',default=None, dest="log_transform_list", help="List of booleans, whether columns are log transformed or not")
parser.add_argument('--winsor_list',default=None, dest="winsor_list", help="List of booleans, whether columns are winsorized or not")
parser.add_argument('--winsor_min_list',default=None, dest="winsor_min_list", help="List of floats for winsor min value")
parser.add_argument('--winsor_max_list',default=None, dest="winsor_max_list", help="List of floats for winsor max values")
parser.add_argument('--label_index',default=None, dest="label_index", help="Index of label column")


args=parser.parse_args()    
eastingIndex=None
northingIndex=None

exclude_list=None
scale_min_list=None
scale_max_list=None
log_transform_list=None
winsor_list=None
winsor_min_list=None
winsor_max_list=None

exclude_list_sorted=[]
scale_min_list_included=[]
scale_max_list_included=[]
log_transform_list_included=[]
winsor_list_included=[]
winsor_min_list_included=[]
winsor_max_list_included=[]
columns=[]
columns_sorted=[] 
columns_excluded=[]
columns_included=[]  

inputFile=args.input_file
fileType=inputFile[-3:].lower()

if(args.eastingIndex is not None):
    eastingIndex=args.eastingIndex    
if(args.northingIndex is not None):
    northingIndex=args.northingIndex   
output_folder=args.output_folder
na_value=""
if(len(args.na_value)>0):
    na_value=args.na_value    

if(args.max_N is not None):
    maxN=float(args.max_N)
else:
    maxN=0.0

if(args.min_N is not None):
    minN=float(args.min_N)
else:
    minN=1.0
if args.label_index is not None:
    label_index=args.label_index
if(args.exclude_list is not None):
    exclude_list=ast.literal_eval(args.exclude_list)
if(args.scale_min_list is not None):
    scale_min_list=ast.literal_eval(args.scale_min_list)
if(args.scale_max_list is not None):
    scale_max_list=ast.literal_eval(args.scale_max_list)
if(args.log_transform_list is not None):
    log_transform_list=ast.literal_eval(args.log_transform_list)
if(args.winsor_list is not None):
    winsor_list=ast.literal_eval(args.winsor_list)
if(args.winsor_min_list is not None):
    winsor_min_list=ast.literal_eval(args.winsor_min_list)
if(args.winsor_max_list is not None):
    winsor_max_list=ast.literal_eval(args.winsor_max_list)



"""
Write lrn file from csv input. Diverges into write_spatial_from_csv and write_nonspatal_from_csv, depending on input type.
"""
def write_from_csv_input():
    global unformattedRows
    global actualNumberOfColumns
    global header
    global df_ex
    global df_in
    header=read_header(inputFile)    
    actualNumberOfColumns=header['cols']
    header=load_input_file(inputFile)    
    unformattedRows=header['rows']
    header['rows']="%"+str(header['rows'])
    header['cols']="%"+str(header['cols'])  
    header['colnames'] = [s.replace('\"', '') for s in header['colnames']]
    header['colnames'] = [s.replace('%', '') for s in header['colnames']]
    header['colnames'] = [s.replace(" ", "") for s in header['colnames']]
    coltypes=[]    
    for i in range(0, (len(header['colnames'])+2)):
        if i<2:
            coltypes.append(0)
        else:
            coltypes.append(1)
    coltypes=np.append("%9",coltypes)
    if eastingIndex is not None:
        write_spatial_from_csv()
    else: #if easting index is none                    
        write_nonspatial_from_csv()
        
    
    
"""
Write lrn file from csv input, when input is nonspatial
"""
def write_nonspatial_from_csv():
    global exclude_list
    global na_value
    global actualNumberOfColumns
    global unformattedRows
    global header
    global df_ex
    global df_in
    global columns_ex
    global columns_in
    global columns
    dummy_coordinates=createDummyCoordinates()                  #x and y columns filled with zeroes are used in place of actual coordinates
    columns=loadColumns(actualNumberOfColumns,dummy_coordinates)

    exclude_list=(True, True)+exclude_list

    for i in range(0, len(columns)) :     
        if(exclude_list[i]==True):
            columns[i][0][0]=0
        else:
            columns[i][0][0]=1
    for i in range(0,  actualNumberOfColumns+2):#+2 because two dummy coordinate columns are added to beginning (this is to keep the shape of the lrn file the same for reading the edited input data in som calculation.)
        columns_sorted.append(columns[i])
        exclude_list_sorted.append(exclude_list[i])
    column_names_sorted=[]
    column_names_sorted.append('x')
    column_names_sorted.append('y')


    for i in range(0,  actualNumberOfColumns):
        if(int(label_index)==i):
                column_names_sorted.append('label')
        else:
            column_names_sorted.append(header['colnames'][i])
    for i in range(0, actualNumberOfColumns):
        if(i>1):
            columns_sorted[i][1][0]=column_names_sorted[i]   
            
    populateCsvDataFrames(-2)        
    writeXmlTreeFromCsv(df_in,columns_included)
    
    if(args.normalized is not None):
        for i in range(0,len(columns_included)):
            data_min= min(columns_included[i][2:].astype(float))
            data_max= max(columns_included[i][2:].astype(float))
            for j in range(2, len(columns_included[i])):
                if(columns_included[i][j]!=na_value):
                    columns_included[i][j]=(scale_max_list_included[i]-scale_min_list_included[i])*(columns_included[i][j].astype(float)-data_min)/(data_max-data_min)+scale_min_list_included[i]
    
    df_in=pd.DataFrame(np.squeeze(np.stack(columns_included, axis=1)))  
    columns_in=df_in.values        
    combineCsvColumns()
    
    for i in range(0, len(columns[1])): 
        if (columns[1][i]== "label\n"):    #remove linebreaker.
            columns[1][i]="label"
    np.savetxt(output_folder+"/DataPreparation/EditedData.lrn", columns, delimiter="\t",header=(header['rows']+"\n"+str(header['cols'])), fmt="%s",comments='')   
    print("Saved to .lrn File")
    
    
"""
Write lrn file from csv input, when input is spatial
"""    
def write_spatial_from_csv():
    
    global exclude_list
    global na_value
    global df_ex
    global df_in
    global columns_ex
    global columns_in
    global columns
    columns=loadColumns(actualNumberOfColumns)  
    
    for i in range(0, len(columns)) :             
        if(exclude_list[i]==True):
            columns[i][0][0]=0
        else:
            columns[i][0][0]=1
    columns_sorted.append(columns[int(eastingIndex)])
    columns_sorted.append(columns[int(northingIndex)])
    exclude_list_sorted.append(exclude_list[int(eastingIndex)])
    exclude_list_sorted.append(exclude_list[int(northingIndex)])
    
    for i in range(0,  actualNumberOfColumns):
        if(i!=int(eastingIndex) and i!=int(northingIndex)):
            columns_sorted.append(columns[i]) 
            exclude_list_sorted.append(exclude_list[i])
            
    column_names_sorted=[]
    column_names_sorted.append(header['colnames'][int(eastingIndex)])
    column_names_sorted.append(header['colnames'][int(northingIndex)])
    
    for i in range(0,  actualNumberOfColumns):
        if(i!=int(eastingIndex) and i!=int(northingIndex)):
            if(int(label_index)==i):
                column_names_sorted.append('label')
            else:
                column_names_sorted.append(header['colnames'][i])
    for i in range(0, actualNumberOfColumns):
        if(i==0):
            columns_sorted[0][1][0]="x"
        elif(i==1):
            columns_sorted[1][1][0]="y"
        else:
            columns_sorted[i][1][0]=column_names_sorted[i]
  
    populateCsvDataFrames() 
    writeXmlTreeFromCsv(df_in,columns_included)
    
    if(args.normalized is not None):
        if(na_value is not ''):
            for i in range(0,len(columns_in[0])):
                colForMinMax= list(filter(lambda x: x!=str(float(na_value)), df_in[i][2:]))
                colForMinMax=[float(i) for i in colForMinMax]
                data_min= min(colForMinMax)
                data_max= max(colForMinMax)
                for j in range(2, len(columns_in[:,i])):
                    if(columns_in[j,i]!=str(float(na_value))):
                        columns_in[j,i]=((scale_max_list_included[i]-scale_min_list_included[i])*(float(columns_in[j,i])-data_min)/(data_max-data_min))+scale_min_list_included[i] 
        else:
            for i in range(0,len(columns_in[0])):                   
                colForMinMax=df_in[i][2:].astype(float)
                data_min= min(colForMinMax) 
                data_max= max(colForMinMax)
                for j in range(2, len(columns_in[:,i])):
                    columns_in[j,i]=((scale_max_list_included[i]-scale_min_list_included[i])*(float(columns_in[j,i])-data_min)/(data_max-data_min))+scale_min_list_included[i] 
    
    df_in=pd.DataFrame(np.squeeze(np.stack(columns_in, axis=0)))  

    combineCsvColumns()
    d = dict()
    for i in range (2, len(columns)):
        d[tuple((columns[i][1], columns[i][2]))] = i#
    if(len(columns)-2>len(d)):
        print("Warning: Data contains duplicate coordinates. The duplicates are written over, so that only the last duplicate instance is kept.")
        values=list(d.values())
        columns[values]
        columns=np.vstack((columns[0:2],columns[values]))
       
    # Remove linebreaker from headers.
    for i in range(0, len(columns[1])): 
        if (columns[1][i]== "label\n"):
            columns[1][i]="label"
    np.savetxt(output_folder+"/DataPreparation/EditedData.lrn", columns, delimiter="\t",header=(header['rows']+"\n"+str(header['cols'])), fmt="%s",comments='')   
    print("Saved to .lrn File")
    
    
    
"""
Write lrn file from tif input
"""
def write_from_tif_input():
    global na_value
    header=load_input_file(inputFile)
    id_col=[]
    for i in range(0, len(header['data'])):
        id_col.append(i)
      
    header['rows']="%"+str(header['rows'])
    header['cols']="%"+str(header['cols'])
    coltypes=[]
    for i in range(0, (len(header['colnames'])+2)):
        if i<2:
            coltypes.append(0)
        else:
            if(exclude_list[i]==True):
                coltypes.append(0)
            else:
                coltypes.append(1)    
    coltypes=np.append("%9",coltypes)#%9 for id col
    header['colnames']=np.append(("id","x","y"),header['colnames']) #add id x and y to column names 
    firstColumn=np.load(output_folder+"/DataPreparation/outfile0.npy")[4:].reshape(-1,1) 
    id_col_with_header=np.vstack((coltypes[0],header['colnames'][0],np.c_[id_col]))  #create id column 
    columns=np.hstack((id_col_with_header,firstColumn)) #stack id column and first column
    secondColumn=np.load(output_folder+"/DataPreparation/outfile1.npy")[4:].reshape(-1,1) #get x and y out of the way, because we don't wont to apply transforms to coordinate data
    columns=np.hstack((columns,secondColumn)) 
    
    for i in range(2, (len(header['colnames'])-1)):       
        if(os.path.isfile(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")):
            column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")[4:]
        else:
            column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+".npy")[4:]
        column=column.reshape(-1,1)
        column[1][0]=column[1][0].replace("%", "").replace(" ","")                
        columns=np.hstack((columns,column)) 
        
    writeXmlTreeFromTif(header,columns)
    
    for i in range(3, (len(header['colnames'])-1)):   
        if(args.normalized is not None):           
            scale_min=scale_min_list[i]
            scale_max=scale_max_list[i]
        if(exclude_list[i]==False):
            array_for_minmax= np.delete(columns[2:,i], np.where(columns[2:,i] == na_value))
            data_min= min(array_for_minmax.astype(float))
            data_max= max(array_for_minmax.astype(float))            
        if(args.normalized is not None):            
            for j in range(2, len(column)):
                 if(columns[j,i]!=na_value):
                     columns[j,i]=(scale_max-scale_min)*(columns[j,i].astype(float)-data_min)/(data_max-data_min)+scale_min  
                     
    for i in range (1, len(columns[0])):#1 to take ID col into account.
        columns[0][i]=coltypes[i]
        columns[1][i]=columns[1][i].replace('\n', '')
        
    df=pd.DataFrame(columns)
    df.apply(pd.to_numeric,errors='coerce')
    
    if(na_value is not ""):
        na_value=float(na_value)
        df=df.replace(str(na_value),np.nan)
        df=df.dropna()    

    columns=df.values             
    np.savetxt(output_folder+"/DataPreparation/EditedData.lrn", columns, delimiter="\t",header=(header['rows']+"\n"+str(header['cols'])), fmt="%s",comments='')  
    print("Saved to .lrn File")




"""
Create xml-tree containing data transformation stage stats and and write it to file (DataStats.xml), when using CSV input
"""
def writeXmlTreeFromCsv(df_in,columns_included):
    root = ET.Element("data") 
    for i in range(0,len(df_in.columns)):
        if(na_value is not ''):
            colForMinMax=columns_included[i][2:].astype(float)[~np.isnan(columns_included[i][2:].astype(float))]
            colForMinMax= list(filter(lambda x: x!=float(na_value), colForMinMax))
            data_min= min(colForMinMax)
            data_max= max(colForMinMax)
        else:
            colForMinMax=columns_included[i][2:].astype(float)[~np.isnan(columns_included[i][2:].astype(float))]
            data_min= min(colForMinMax)
            data_max= max(colForMinMax)
        newElement=ET.Element(df_in[i][1].replace('\"','')	)
        

        minElement=ET.Element("min")
        minElement.text=str(data_min)
        maxElement=ET.Element("max")
        maxElement.text=str(data_max)      
        is_log_transformed=log_transform_list_included[i] 
        is_winsorized=winsor_list_included[i]
        if (args.normalized is not None):
            scale_min=scale_min_list_included[i]
            scale_max=scale_max_list_included[i]
            scaleMinElement=ET.Element("scaleMin")
            scaleMinElement.text=str(scale_min)
            scaleMaxElement=ET.Element("scaleMax")
            scaleMaxElement.text=str(scale_max)
        winsorElement=ET.Element("winsorized")
        winsorElement.text=str(is_winsorized)
        if(is_winsorized==True):
            winsor_min=winsor_min_list_included[i]
            winsor_max=winsor_max_list_included[i]
            winsorMinElement=ET.Element("winsorMin")
            winsorMinElement.text=str(winsor_min)
            winsorMaxElement=ET.Element("winsorMax")
            winsorMaxElement.text=str(winsor_max)
        logTransformElement=ET.Element("logTransform")
        logTransformElement.text=str(is_log_transformed)
        if(args.normalized is not None):   
            newElement.append(scaleMinElement)
            newElement.append(scaleMaxElement)
        newElement.append(logTransformElement)
        newElement.append(winsorElement)
        if(is_winsorized==True):
            newElement.append(winsorMinElement)
        newElement.append(minElement)
        newElement.append(maxElement)
        root.append(newElement)

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(output_folder+"/DataStats.xml", "w") as f:
        f.write(xmlstr)  
            
        
        
"""
Create xml-tree containing data transformation stage stats and and write it to file (DataStats.xml), when using TIF input
"""
def writeXmlTreeFromTif(header,columns):
    root = ET.Element("data")
    for i in range(2, (len(header['colnames'])-1)):     
           
       
        if(exclude_list[i]==False): 
            column= columns[:,i+1].reshape(-1,1)#+1 because there's already an id col at this point  
            array_for_minmax= np.delete(column[2:], np.where(column[2:] == na_value))
            data_min= min(array_for_minmax.astype(float))
            data_max= max(array_for_minmax.astype(float))    
            newElement=ET.Element(column[1][0].replace('%', '').replace(" ",""))	
                        
                    
            minElement=ET.Element("min")
            minElement.text=str(data_min)
            maxElement=ET.Element("max")
            maxElement.text=str(data_max)   
            is_log_transformed=log_transform_list[i] 
            is_winsorized=winsor_list[i]   
            if(args.normalized is not None):
                scale_min=scale_min_list[i]
                scale_max=scale_max_list[i]
                scaleMinElement=ET.Element("scaleMin")
                scaleMinElement.text=str(scale_min)
                scaleMaxElement=ET.Element("scaleMax")
                scaleMaxElement.text=str(scale_max)      
            winsorElement=ET.Element("winsorized")
            winsorElement.text=str(is_winsorized)  
            if(is_winsorized ==True):
                winsor_min=winsor_min_list[i]
                winsor_max=winsor_max_list[i]
                winsorMinElement=ET.Element("winsorMin")
                winsorMinElement.text=str(winsor_min)
                winsorMaxElement=ET.Element("winsorMax")
                winsorMaxElement.text=str(winsor_max)       
            logTransformElement=ET.Element("logTransform")
            logTransformElement.text=str(is_log_transformed)   
            if(args.normalized is not None):   
                newElement.append(scaleMinElement)
                newElement.append(scaleMaxElement)
            newElement.append(logTransformElement)
            newElement.append(winsorElement)
            if(is_winsorized==True):
                newElement.append(winsorMinElement)
                newElement.append(winsorMaxElement)
            newElement.append(minElement)
            newElement.append(maxElement)            
            root.append(newElement)
            
        if(args.normalized is not None):            
            for j in range(2, len(column)):
                 if(column[j]!=na_value):
                     column[j]=(scale_max-scale_min)*(column[j].astype(float)-data_min)/(data_max-data_min)+scale_min         
    
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(output_folder+"/DataStats.xml", "w") as f:
        f.write(xmlstr)  

"""
load columns from numpy binary dump files, add them to the columns array (default: empty, nonspatial csv uses an array with dummy x and y columns)
"""
def loadColumns(numberOfColumns,columns=[]):
    for i in range(0, numberOfColumns):      
            if(int(label_index)==i):
                column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+"label.npy",allow_pickle=True)[4:]
            else:
                if(os.path.isfile(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")): 
                    column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")[4:]
                else:
                    column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+".npy")[4:]        
            column=column.reshape(-1,1)
            columns.append(column)
    return columns


"""
Create data columsn with empty dummy coordinate data, used by nonspatial csv option.
"""
def createDummyCoordinates():
    columns=[]                   
    x_col=[]
    y_col=[]
    x_col.append(0)  
    y_col.append(0) 
    x_col.append("x")  
    y_col.append("y") 
    for i in range(0, unformattedRows): 
        x_col.append(0)  
        y_col.append(0) 
    columns.append(np.array(x_col).reshape(-1,1))
    columns.append(np.array(y_col).reshape(-1,1))
    return columns


"""
Populate dataframes used with csv option.
"""
def populateCsvDataFrames(indexModifier=0):
    global df_ex
    global df_in
    global columns_ex
    global columns_in
    global na_value
    for i in range(0, len(columns_sorted)) :                				
        columns_sorted[i][1][0]=columns_sorted[i][1][0].replace('\n', '')	
        if(exclude_list_sorted[i]==True):			                        	
            columns_excluded.append(columns_sorted[i])			              
        else:
            columns_included.append(columns_sorted[i])			             
            scale_min_list_included.append(scale_min_list[(i+indexModifier)])		     	
            scale_max_list_included.append(scale_max_list[(i+indexModifier)])	      	 	
            winsor_list_included.append(winsor_list[(i+indexModifier)])
            winsor_min_list_included.append(winsor_min_list[(i+indexModifier)])			
            winsor_max_list_included.append(winsor_max_list[(i+indexModifier)])			
            log_transform_list_included.append(log_transform_list[(i+indexModifier)])	
            
    df_ex=pd.DataFrame(np.squeeze(np.stack(columns_excluded, axis=1)))              
    df_ex = df_ex.replace('NA','nan',  regex=True)   
    df_ex=df_ex.replace(np.nan, 'nan', regex=True)
    
    df_in=pd.DataFrame(np.squeeze(np.stack(columns_included, axis=1)))
    df_in = df_in.replace('NA','nan', regex=True)  
    df_in=df_in.replace(np.nan, 'nan', regex=True)
    for i in range(0,len(df_in.columns)):
        df_in=df_in.loc[df_in[:][i] !='nan']   
    
    rowsToDrop=df_ex.drop(df_in.index)
    df_ex=df_ex.drop(rowsToDrop.index)  
    columns_ex=df_ex.values   
    columns_in=df_in.values   
    if(na_value is not ""):
        na_value=float(na_value)
        df_in=df_in.replace(str(na_value),np.nan)
        
    df_in_header=df_in[:2]
    df_in=df_in[2:].apply(pd.to_numeric,errors='coerce')  
    df_in=pd.concat([df_in_header, df_in])
        
"""
Combine used columns into a single numpy array
"""
def combineCsvColumns():
    global columns_ex
    global columns_in
    global columns
    columns=np.hstack((columns_ex, columns_in))
    columns=((pd.DataFrame(columns)).dropna()).values
    id_col=[]
    for i in range(0, len(columns)-2): 
        id_col.append(i)  
    id_col_with_header=np.vstack((["%9"],["id"],np.c_[id_col]))    
    columns=np.hstack((id_col_with_header, columns))  
    
        



if(fileType=="tif"):
    write_from_tif_input()
    

if(fileType=="csv"):
    write_from_csv_input()
    