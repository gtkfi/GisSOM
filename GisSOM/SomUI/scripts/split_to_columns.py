# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:02:56 2019

@author: shautala

Python script to split input file to individual data columns, that are stored as numpy binary files.
These numpy files are used in data transformation stage by EditColumn, DrawSomHistogram, and CombineToLrnFile
python scripts. 

Input type is either .lrn file or GeoTIFF file.
"""


import numpy as np
import ast
from loadfile import load_input_file, read_coordinate_columns, read_data_columns, read_header
import pandas as pd
import sys

inputFile=sys.argv[1]
output_folder=sys.argv[2]
inputType=inputFile[-3:].lower()

#Slightly modified versions of functions by the same names in loadfile.py
def _read_csv_columns(lrn_header, columns, fmt=''): 
    if not type(columns) in (list, tuple):
        raise TypeError('Invalid type: columns must be a list or tuple')
    colnames = ([lrn_header['colnames'][i] for i in columns])
    df=pd.read_csv(inputFile, delimiter=',', header=None, skiprows=1)
    df=df.astype(str)
    labelData=df.values
    df=df.apply(pd.to_numeric,errors='coerce')   
    data=df.values
    return {'data': data, 'labelData': labelData, 'colnames': colnames, 'fmt': fmt}

def read_csv_columns(lrn_header):
    coord_cols = (0,1)
    fmt = ('%f ' * len(coord_cols)).rstrip()
    return _read_csv_columns(lrn_header, coord_cols, fmt)



#lrn is commented out, as it is no longer used as an input type in the later versions
"""
def _read_columns(lrn_header, columns, fmt=''):  
    if not type(columns) in (list, tuple):
        raise TypeError('Invalid type: columns must be a list or tuple')
    colnames = ([lrn_header['colnames'][i] for i in columns])   
    df=pd.read_csv(inputFile, delimiter='\t', header=None, skiprows=lrn_header['headerlength'], usecols=columns)
    df=df.astype(str)
    labelData=df.values
    df=pd.read_csv(inputFile, delimiter='\t', header=None, skiprows=lrn_header['headerlength'], usecols=columns)
    df=df.apply(pd.to_numeric,errors='coerce')  
    data=df.values
    return {'data': data, 'labelData': labelData, 'colnames': colnames, 'fmt': fmt}

def read_columns(lrn_header):
    coord_cols = [i for i, x in enumerate(lrn_header['coltypes']) if x == 0 or x==1 ]
    fmt = ('%f ' * len(coord_cols)).rstrip()
    return _read_columns(lrn_header, coord_cols, fmt)
"""




"""
if(inputType=="lrn"):                                 
    header=read_header(inputFile)             #read lrn file
    columns_all=read_columns(header)              
    cleanHeader=np.delete(header['coltypes'],0)   #Delete ID column from column types
    cleanColNames=np.delete(header['colnames'],0) #Delete ID column from column names
    falses=[]                                     #create a row of "false" values, will be used to initialize data transformation values (no transformations done by default)
    for i in range(0, len(cleanColNames)):
        falses.append("false")    
    colNamesAndTypes=np.vstack((falses,(np.full((1,len(cleanColNames)),0)),(np.full((1,len(cleanColNames)),0)),falses,cleanHeader,cleanColNames)) #stack header rows (data transformation:(falses, zeros, zeros,falses), column types, column names
    allButFirstTwoRows= np.concatenate((colNamesAndTypes,columns_all['data']),axis=0)   #stack header on top of data 
    allButFirstTwoRowsLabel= np.concatenate((colNamesAndTypes,columns_all['labelData']),axis=0)   #stack header of hte label data 
    for i in range(0, len(allButFirstTwoRows[0])):                                      #save individual data columns as numpy binary files. These will be used by EditColumn, DrawSomHistogram, and CombineLrnFile python scripts
        np.save(output_folder+"/DataPreparation/outfile"+str(i)+"label", allButFirstTwoRowsLabel[:,i])
        np.save(output_folder+"/DataPreparation/outfile"+str(i), allButFirstTwoRows[:,i])
"""
if(inputType=="tif"):   
    header=load_input_file(inputFile)   #here inputfile is a list of input files.     
    columns_data=header['data']                       
    coords=read_coordinate_columns(header)   
    columns_all=np.concatenate((coords['data'],columns_data),axis=1)     
    colnames_coords=["x","y"]   #add x and y column names to colnames
    colnames_data=header['colnames']
    colnames=np.append(colnames_coords,colnames_data)  
    falses=[]   #create a row of "false" values, will be used to initialize data transformation values (no transformations done by default)            
    for i in range(0, len(colnames)):
        falses.append("false")  
    coltypes=[] #create coltypes for data. 0 for coords, 1 for others (all columns are given as individual files so there should be no need to exclude data at this stage)
    for i in range(0, len(colnames)):
        if i<=1:
            coltypes.append(0)
        else:
            coltypes.append(1)       
    colNamesAndTypes=np.vstack((falses,(np.full((1,len(colnames)),0)),(np.full((1,len(colnames)),0)),falses,coltypes,colnames))  #stack header rows (data transformation:(falses, zeros, zeros,falses), column types, column names).
    allButFirstTwoRows= np.concatenate((colNamesAndTypes,columns_all),axis=0) #stack header rows and data
    #save individual data columns as numpy binary files. These will be used by EditColumn, DrawSomHistogram, and CombineLrnFile python scripts
    for i in range(0, len(allButFirstTwoRows[0])):
        np.save(output_folder+"/DataPreparation/outfile"+str(i), allButFirstTwoRows[:,i]) 
    print(header['nodatavalue'])

elif(inputType=="csv"):  
    header=read_header(inputFile)       
    columns_test=read_csv_columns(header) 
    columns_data=columns_test['data']    
    header['data']=columns_data
    columns_all=columns_data
    colnames=header['colnames']
    falses=[]   #create a row of "false" values, will be used to initialize data transformation values (no transformations done by default)             
    for i in range(0, len(colnames)):
        falses.append("false")   
        if(len(colnames[i].replace('\"', '').replace('%', '').replace(" ", "") )==0):
            sys.exit("Error: Empty column headers")
    coltypes=[] #create coltypes for data. 0 for coords, 1 for others (all columns are given as individual files so there should be no need to exclude data at this stage)
    for i in range(0, len(colnames)):
        if i<=1:
            coltypes.append(0)
        else:
            coltypes.append(1)    
    colNamesAndTypes=np.vstack((falses,(np.full((1,len(colnames)),0)),(np.full((1,len(colnames)),0)),falses,coltypes,colnames))  #stack header rows (data transformation:(falses, zeros, zeros,falses), column types, column names
    allButFirstTwoRows= np.concatenate((colNamesAndTypes,columns_all),axis=0) #stack header rows and data
    allButFirstTwoRowsLabel= np.concatenate((colNamesAndTypes,columns_test['labelData']),axis=0)   #stack header of hte label data 
    
    for i in range(0, len(allButFirstTwoRows[0])): #save individual data columns as numpy binary files. These will be used by EditColumn, DrawSomHistogram, and CombineLrnFile python scripts
        np.save(output_folder+"/DataPreparation/outfile"+str(i)+"label", allButFirstTwoRowsLabel[:,i])
        np.save(output_folder+"/DataPreparation/outfile"+str(i), allButFirstTwoRows[:,i])
