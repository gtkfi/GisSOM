# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:03:49 2019

@author: shautala

Script for combining individual data columns back to a .lrn file. This lrn file is used as input for som calculation.
For CSV files it is possible to use non-spatial data, in this case this script will output a lrn file 
with x- and y- cols filled with zeroes, for internal use. Final program output will not contain these dummy columns.
"""

#Import warnings are ignoder because of a persistent matplotlib deprecationwarning

import warnings
import argparse
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")
    import matplotlib.pyplot as plt
    from loadfile import load_input_file, read_coordinate_columns,  read_lrn_header
    import numpy as np
    import pandas as pd
    import os
    import sys

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


args=parser.parse_args()    

eastingIndex=None
northingIndex=None
inputFile=args.input_file
if(args.eastingIndex is not None):
    eastingIndex=args.eastingIndex    
if(args.northingIndex is not None):
    northingIndex=args.northingIndex   
output_folder=args.output_folder
na_value=""
if(len(args.na_value)>0):
    na_value=args.na_value    
fileType=inputFile[-3:].lower()




if(fileType=="lrn"):
    id_col =  pd.read_csv(inputFile,skiprows=3, usecols=[0], delimiter='\t') 
    id_col=id_col.values                                                    
    header=read_lrn_header(inputFile)
    actualNumberOfColumns=header['cols']-1
    cords=read_coordinate_columns(header)   
    header['rows']="%"+str(header['rows'])#format first rows with '%' sign according to lrn format
    header['cols']="%"+str(header['cols'])
    header['coltypes'][0]="%"+str(header['coltypes'][0])  
    header['colnames'][0]="%"+str(header['colnames'][0])
    id_col_with_header=np.vstack((header['coltypes'][0],header['colnames'][0],id_col))  #stack header cells on top of id_col.
    columns=[]
    columns_sorted=[]   
    for i in range(0, actualNumberOfColumns):      
        if(os.path.isfile(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")): #If the data column has been edited, use the edited version,
            column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")[4:]
        else:
            column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+".npy")[4:]     #otherwise use an unedited version.     
        column=column.reshape(-1,1)
        columns.append(column)      
    columns_sorted.append(columns[int(eastingIndex)])    #Data columns labelled as easting and northing will respectively be set to columns 0 and 1, and renamed x and y.
    columns_sorted.append(columns[int(northingIndex)])  
    columns_sorted[0][1][0]="x" 
    columns_sorted[1][1][0]="y" 
    for i in range(0,  actualNumberOfColumns):
        if(i!=int(eastingIndex) and i!=int(northingIndex)):
            columns_sorted.append(columns[i])            
    columns_excluded=[]
    columns_included=[]           
    for i in range(0, len(columns_sorted)) :       
        if(columns_sorted[i][0][0]=='0'):
            columns_excluded.append(columns_sorted[i])
        else:
            columns_included.append(columns_sorted[i])   
    df_ex=pd.DataFrame(np.squeeze(np.stack(columns_excluded, axis=1)))        #replace exluded columns' NA values with 'NaN' string so they won't cause deletion of rows.        
    df_ex = df_ex.replace('nan', 'NA', regex=True)      #this might not be necessary but OK just in case.
    columns_ex=df_ex.values
    
    if(args.normalized is not None): 
        for i in range(0,len(columns_included)): 
            data_min= min(columns_included[i][2:].astype(float))
            data_max= max(columns_included[i][2:].astype(float))
            for j in range(2, len(columns_included[i])):
                if(columns_included[i][j]!=na_value):
                    columns_included[i][j]=(columns_included[i][j].astype(float)-data_min)/(data_max-data_min) 
    #normalize columns_in! for loop col by col
    df_in=pd.DataFrame(np.squeeze(np.stack(columns_included, axis=1)))
    if(na_value is not ""):
        na_value=float(na_value)
        df_in=df_in.replace(str(na_value),np.nan)
    df_in_header=df_in[:2]
    df_in=df_in[2:].apply(pd.to_numeric,errors='coerce')   #Skip headers so that they are not removed
    df_in=pd.concat([df_in_header, df_in])
    columns_in=df_in.values     
    columns=np.hstack((columns_ex, columns_in))
    columns=((pd.DataFrame(columns)).dropna()).values
    columns=np.hstack((id_col_with_header[4:], columns))  
    #add lrn header to stacked columns and save as lrn file. '#comment' rows are not copied, because this is not an output file, and comments are not needed for som calculation.
    np.savetxt(output_folder+"/DataPreparation/EditedData.lrn", columns, delimiter="\t",header=(header['rows']+"\n"+str(header['cols'])), fmt="%s",comments='')
    print("Saved to .lrn File")


if(fileType=="tif"):
    
    header=load_input_file(inputFile)
    id_col=[]
    for i in range(0, len(header['data'])):
        id_col.append(i)
    header['rows']="%"+str(header['rows'])
    header['cols']="%"+str(header['cols'])
    coltypes=[]#create coltypes, %9 for id col, 0 for x and y, 1 for the rest
    for i in range(0, (len(header['colnames'])+2)):
        if i<2:
            coltypes.append(0)
        else:
            coltypes.append(1)                                    
    coltypes=np.append("%9",coltypes)
    header['colnames']=np.append(("id","x","y"),header['colnames']) #add id x and y to column names 
    print(header['colnames'])
    firstColumn=np.load(output_folder+"/DataPreparation/outfile0.npy")[4:].reshape(-1,1) 
    id_col_with_header=np.vstack((coltypes[0],header['colnames'][0],np.c_[id_col]))  #create id column #
    columns=np.hstack((id_col_with_header,firstColumn)) #stack id column and first column
    secondColumn=np.load(output_folder+"/DataPreparation/outfile1.npy")[4:].reshape(-1,1) #get x and y out of the way, because we don't wont to apply transforms to coordinate data
    columns=np.hstack((columns,secondColumn)) 
    for i in range(2, (len(header['colnames'])-1)):       
        if(os.path.isfile(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")):
            column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")[4:]
        else:
            column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+".npy")[4:]
        column=column.reshape(-1,1)
        if(args.normalized is not None): 
            array_for_minmax= np.delete(column[2:], np.where(column[2:] == na_value))
            data_min= min(array_for_minmax.astype(float))
            data_max= max(array_for_minmax.astype(float))
            for i in range(2, len(column)):
                 if(column[i]!=na_value):
                     column[i]=(column[i].astype(float)-data_min)/(data_max-data_min)              
        columns=np.hstack((columns,column))   
    
    df=pd.DataFrame(columns)
    df.apply(pd.to_numeric,errors='coerce')
    
    if(na_value is not ""):
        na_value=float(na_value)
        df=df.replace(str(na_value),np.nan)
        df=df.dropna()    
    columns=df.values             
    np.savetxt(output_folder+"/DataPreparation/EditedData.lrn", columns, delimiter="\t",header=(header['rows']+"\n"+str(header['cols'])), fmt="%s",comments='')  #add lrn header to stacked columns, save to file.
    print("Saved to .lrn File")


if(fileType=="csv"):

    header=read_lrn_header(inputFile)    
    actualNumberOfColumns=header['cols']
    header=load_input_file(inputFile)    
    unformattedRows=header['rows']
    header['rows']="%"+str(header['rows'])
    header['cols']="%"+str(header['cols'])  
    coltypes=[]    #create coltypes, %9 for id col, 0 for x and y, 1 for the rest
    for i in range(0, (len(header['colnames'])+2)):
        if i<2:
            coltypes.append(0)
        else:
            coltypes.append(1)
    coltypes=np.append("%9",coltypes)
    columns=[]
    columns_sorted=[]   
  #Is there a function that can add vectors as well as 2d arrays? this seems silly.
    if eastingIndex is not None:

        for i in range(0, actualNumberOfColumns):      
            if(os.path.isfile(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")): 
                column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")[4:]
            else:
                column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+".npy")[4:]        
            column=column.reshape(-1,1)
            columns.append(column)
        columns_sorted.append(columns[int(eastingIndex)])
        columns_sorted.append(columns[int(northingIndex)])
        for i in range(0,  actualNumberOfColumns):
            if(i!=int(eastingIndex) and i!=int(northingIndex)):
                columns_sorted.append(columns[i]) 
        column_names_sorted=[]
        column_names_sorted.append(header['colnames'][int(eastingIndex)])
        column_names_sorted.append(header['colnames'][int(northingIndex)])
        for i in range(0,  actualNumberOfColumns):
            if(i!=int(eastingIndex) and i!=int(northingIndex)):
                column_names_sorted.append(header['colnames'][i])
        for i in range(0, actualNumberOfColumns):
            if(i==0):
                columns_sorted[0][1][0]="x"
            elif(i==1):
                columns_sorted[1][1][0]="y"
            else:
                columns_sorted[i][1][0]=column_names_sorted[i]    
        columns_excluded=[]
        columns_included=[]           
        for i in range(0, len(columns_sorted)) :       
            if(columns_sorted[i][0][0]=='0'):
                columns_excluded.append(columns_sorted[i])
            else:
                columns_included.append(columns_sorted[i])
         
        df_ex=pd.DataFrame(np.squeeze(np.stack(columns_excluded, axis=1)))        #replace exluded columns' NA values with 'NaN' string so they won't cause deletion of rows.        
        df_ex = df_ex.replace('nan', 'NA', regex=True)      
        columns_ex=df_ex.values
        if(args.normalized is not None):
            for i in range(0,len(columns_included)):
                data_min= min(columns_included[i][2:].astype(float))
                data_max= max(columns_included[i][2:].astype(float))
                for j in range(2, len(columns_included[i])):
                    if(columns_included[i][j]!=na_value):
                        columns_included[i][j]=(columns_included[i][j].astype(float)-data_min)/(data_max-data_min)
        df_in=pd.DataFrame(np.squeeze(np.stack(columns_included, axis=1)))
        if(na_value is not ""):
            na_value=float(na_value)
            df_in=df_in.replace(str(na_value),np.nan)
        #if(args.normalized is not None):
        df_in_header=df_in[:2]
        df_in=df_in[2:].apply(pd.to_numeric,errors='coerce')   #skip headers so they won't be removed
        df_in=pd.concat([df_in_header, df_in])
        columns_in=df_in.values     
        #normalize columns_in! for loop
        columns=np.hstack((columns_ex, columns_in))
        columns=((pd.DataFrame(columns)).dropna()).values

        id_col=[]
        for i in range(0, len(columns)-2): 
            id_col.append(i)  
        id_col_with_header=np.vstack((["%9"],["id"],np.c_[id_col]))  #create id column        #'comment' rows are not copied, because this is not an output file, and comments are not needed for som calculation.    
        columns=np.hstack((id_col_with_header, columns))         


    else: #if easting index is none                    
        x_col=[]
        y_col=[]
        x_col.append(0)  
        y_col.append(0) 
        x_col.append("x")  
        y_col.append("y") 
        for i in range(0, unformattedRows): 
            x_col.append(0)  
            y_col.append(0) 
        columns.append(np.array(x_col).reshape(-1,1))#a simple list won't do, these have to be reshaped into numpy 2d arrays of shape (len,1), because loading the binary arrays results in them being this shape.
        columns.append(np.array(y_col).reshape(-1,1))
        for i in range(0, actualNumberOfColumns):      
            if(os.path.isfile(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")): #If the data column has been edited, use the edited version,
                column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+"_edited.npy")[4:]
            else:
                column=np.load(output_folder+"/DataPreparation/outfile"+str(i)+".npy")[4:]     #otherwise use an unedited version.      
            column=column.reshape(-1,1)
            columns.append(column)
            
        for i in range(0,  actualNumberOfColumns+2):#+2 because two dummy coordinate columns are added to beginning (this is to keep the shape of the lrn file the same for reading the edited input data in som calculation.)
            columns_sorted.append(columns[i])
        column_names_sorted=[]
        column_names_sorted.append('x')
        column_names_sorted.append('y')

        for i in range(0,  actualNumberOfColumns):
            column_names_sorted.append(header['colnames'][i])
        for i in range(0, actualNumberOfColumns):
            if(i>1):
                columns_sorted[i][1][0]=column_names_sorted[i]   
        columns_excluded=[]
        columns_included=[]           
        for i in range(0, len(columns_sorted)) :       
            if(columns_sorted[i][0][0]=='0'):
                columns_excluded.append(columns_sorted[i])
            else:
                columns_included.append(columns_sorted[i])
         
        df_ex=pd.DataFrame(np.squeeze(np.stack(columns_excluded, axis=1)))        #replace exluded columns' NA values with 'NaN' string so they won't cause deletion of rows.        
        df_ex = df_ex.replace('nan', 'NA', regex=True)     
        columns_ex=df_ex.values
        
        if(args.normalized is not None):
            for i in range(0,len(columns_included)):
                data_min= min(columns_included[i][2:].astype(float))
                data_max= max(columns_included[i][2:].astype(float))
                for j in range(2, len(columns_included[i])):
                    if(columns_included[i][j]!=na_value):
                        columns_included[i][j]=(columns_included[i][j].astype(float)-data_min)/(data_max-data_min) 
        df_in=pd.DataFrame(np.squeeze(np.stack(columns_included, axis=1)))
        if(na_value is not ""):
            na_value=float(na_value)
            df_in=df_in.replace(str(na_value),np.nan)
        df_in_header=df_in[:2]
        df_in=df_in[2:].apply(pd.to_numeric,errors='coerce')   #skip headers so they won't be removed
        df_in=pd.concat([df_in_header, df_in])
        columns_in=df_in.values     
        columns=np.hstack((columns_ex, columns_in))
        columns=((pd.DataFrame(columns)).dropna()).values
        id_col=[]
        for i in range(0, len(columns)-2): 
            id_col.append(i)
        id_col_with_header=np.vstack((["%9"],["id"],np.c_[id_col]))  #create id column        #'comment' rows are not copied, because this is not an output file, and comments are not needed for som calculation.                  
        columns=np.hstack((id_col_with_header, columns))   
        
    # Remove linebreaker.
    for i in range(0, len(columns[1])): 
        if (columns[1][i]== "label\n"):
            columns[1][i]="label"
    #add header to stacked columns, save to file.
    np.savetxt(output_folder+"/DataPreparation/EditedData.lrn", columns, delimiter="\t",header=(header['rows']+"\n"+str(header['cols'])), fmt="%s",comments='')   
    print("Saved to .lrn File")