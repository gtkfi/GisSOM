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
from nextsomcore.loadfile import load_input_file, read_coordinate_columns
import pandas as pd
import sys

#Slightly modified versions of functions by the same names in loadfile.py
def _read_csv_columns(inputFile, columns, fmt=''): 
    if not type(columns) in (list, tuple):
        raise TypeError('Invalid type: columns must be a list or tuple')
    colnames = np.loadtxt(inputFile, delimiter=",",dtype='str',encoding='utf-8-sig',max_rows = 1)    
    #colnames = ([lrn_header['colnames'][i] for i in columns])
    df=pd.read_csv(inputFile, delimiter=',', header=None, skiprows=1)
    #df=dd.read_csv(inputFile,blocksize=25e6, delimiter=',', header=None, skiprows=1)
    df=df.astype(str)#TODO: check if this step is truly necessary
    labelData=df.values
    df=df.apply(pd.to_numeric,errors='coerce',axis=1)   
    data=df.values
    rows=len(data)
    cols=len(data[0])  
    #data.compute_chunk_sizes()
    #return {'data': data, 'labelData': labelData, 'colnames': colnames, 'fmt': fmt}
    return {'file': inputFile, 'rows': rows, 'cols': cols,'data': data, 'labelData': labelData, 'colnames': colnames, 'filetype': 'csv', 'fmt': fmt}
#'file': input_file, 'rows': rows, 'cols': cols, 'colnames': colnames, 'headerlength': 1, 'data': None, 'filetype': 'csv'

def read_csv_columns(inputFile):
    coord_cols = (0,1)
    fmt = ('%f ' * len(coord_cols)).rstrip()
    return _read_csv_columns(inputFile, coord_cols, fmt)



#lrn is commented out, as it is no longer used as an input type in the later versions

def readInputData(inputFile,inputType):
    if(inputType=="tif"):   
        
        header=load_input_file(inputFile)   
        columns_data=header['data']                       
        coords=read_coordinate_columns(header)   
        if(len(str(header["noDataValue"]))>15):  # longer representations (mayber a 64 bit representation of the largely negative 32 bit no-data value or something?) dont work with float32, but the shorter representations seem to require it
            columns_all=np.concatenate((coords['data'],columns_data),axis=1)
        else:
            columns_all=np.concatenate((coords['data'],columns_data),axis=1).astype('float32') 
        colnames_coords=["x","y"]   #add x and y column names to colnames
        colnames_data=header['colnames']
        colnames=np.append(colnames_coords,colnames_data)  
        checkHeaderValidity(colnames)
        falses=[]   #create a row of "false" values, will be used to initialize data transformation values (no transformations done by default)            
        for i in range(0, len(colnames)):
            falses.append("false")  
        coltypes=[] #create coltypes for data. 0 for coords, 1 for others (all columns are given as individual files so there should be no need to exclude data at this stage)
        for i in range(0, len(colnames)):
            if i<=1:
                coltypes.append(0)
            else:
                coltypes.append(1)       
        colNamesAndTypes=np.vstack((falses,(np.full((1,len(colnames)),0)),(np.full((1,len(colnames)),0)),falses,(np.full((1,len(colnames)),0)),(np.full((1,len(colnames)),0)),coltypes,colnames))  #stack header rows (data transformation:(falses, zeros, zeros,falses), column types, column names).
        allButFirstTwoRows= np.concatenate((colNamesAndTypes,columns_all),axis=0) #stack header rows and data
        #save individual data columns as numpy binary files. These will be used by EditColumn, DrawSomHistogram, and CombineLrnFile python scripts
        #for i in range(0, len(allButFirstTwoRows[0])):
        #    np.save(output_folder+"/DataPreparation/outfile"+str(i), allButFirstTwoRows[:,i]) 
        data={"data":allButFirstTwoRows,"noDataValue":header['noDataValue']}
        return(data)
        #print(header['noDataValue'])

    elif(inputType=="csv"):     
        columns=read_csv_columns(inputFile) 
        colnames=columns['colnames']
        checkHeaderValidity(colnames)
        falses=[]   #create a row of "false" values, will be used to initialize data transformation values (no transformations done by default)             
        for i in range(0, len(colnames)):
            falses.append("false")   
            if(len(colnames[i].replace('\"', '').replace('%', '').replace(" ", "") )==0):
                sys.exit("Error: Empty column headers") 
                
        #for x in range(columns['cols']):
        #    if column_all_equal(columns['data'][:,x]):
        #        raise TypeError('ERROR')
        colNamesAndTypes=np.vstack((falses,(np.full((1,len(colnames)),0)),(np.full((1,len(colnames)),0)),falses,(np.full((1,len(colnames)),0)),(np.full((1,len(colnames)),0)),(np.full((1,len(colnames)),1)),colnames))  #stack header rows (data transformation:(falses, zeros, zeros,falses), column types, column names
        allButFirstTwoRows= np.concatenate((colNamesAndTypes,columns['data']),axis=0) #stack header rows and data
        allButFirstTwoRowsLabel= np.concatenate((colNamesAndTypes,columns['labelData']),axis=0)   #stack header of the label data        
        data={"data":allButFirstTwoRows,"label":allButFirstTwoRowsLabel,"noDataValue":""}
        return(data)
    
    #Add informative errors on bad data: on numeric headers, on data with a fully nodata variable (or variable whose values are all the same), empty variable header. Empty cell?
    #checkHeaderValidity?
def checkHeaderValidity(colnames):
    for colname in colnames:
        if(colname[0].isdigit()):
            raise ValueError("Header can not begin with numeric character:"+colname)
        elif(len(colname)==0):
            raise ValueError("Input file contains empty headers")
            
def column_all_equal(column):
    if type(column) is list:
        group = column.groupby()
        return next(group, True) and not next(group, False)
    if type(column) is tuple:
        return len(set(column)) == 1