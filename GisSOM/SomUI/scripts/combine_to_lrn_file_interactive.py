# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 16:03:49 2019

@author: shautala

Script for combining data array back to a .lrn file. This lrn file is used as input for som calculation.
For CSV files it is possible to use non-spatial data, in this case this script will output a lrn file 
with x- and y- cols filled with zeroes, for internal use. Final program output will not contain these dummy columns.
"""

#import argparse
from nextsomcore.loadfile import load_input_file
import xml.etree.ElementTree as ET
from xml.dom import minidom
import numpy as np
import pandas as pd
#import os

    
    
"""
Write lrn file from csv input, when input is nonspatial
"""
def write_nonspatial_from_csv(columns,input_file,output_folder,is_scaled,na_value,label_index):

    columns=create_dummy_coordinates(columns) 
    easting_index=0
    northing_index=1
    
    columns_sorted=[]
    columns_sorted.append(columns[:,int(easting_index)])
    columns_sorted.append(columns[:,int(northing_index)])   
    for i in range(0,  len(columns[0])):
        if(i!=int(easting_index) and i!=int(northing_index)):
            columns_sorted.append(columns[:,i]) 
    for i in range(0, len(columns[0])):
        if(i==0):
            columns_sorted[0][7]="x"
        elif(i==1):
            columns_sorted[1][7]="y"


    columns_included=[]
    columns_excluded=[]

    for i in range(0, len(columns_sorted)) :                				
        if(columns_sorted[i][4]=='0'):	                        	
            columns_excluded.append(columns_sorted[i])			              
        else:
            columns_included.append(columns_sorted[i])			             
            
    df_ex=pd.DataFrame(np.squeeze(np.stack(columns_excluded, axis=1)))        #tässä on jo vähän hitaampi vaihe. testaile tätä isolla datalla. että mitkä stepit on hitaita, ja onko kaikki tarpeellisia. esim. onko dataframeksi muuttaminen raskasta ja/tai tarpeellista?      
    df_ex = df_ex.replace('NA','nan',  regex=True)   
    df_ex=df_ex.replace(np.nan, 'nan', regex=True)
    
    df_in=pd.DataFrame(np.squeeze(np.stack(columns_included, axis=1)))
    df_in.iloc[2:,:] = df_in.iloc[2:,:].replace('NA','nan', regex=True)  
    df_in.iloc[2:,:]=df_in.iloc[2:,:].replace(np.nan, 'nan', regex=True)#unify all NA values to same format
    if(na_value !=""):
        na_value=float(na_value)
        df_in=df_in.replace(str(na_value),np.nan)
    for i in range(0,len(df_in.columns)): 
        tempCol=(df_in[:][i] !='nan')#create boolean array on wether data elements are valid numbers or 'nan'
        tempCol[1]=True #assign True to header, so that the header is not labeled False even if it is 'nan', because that should be a valid header as well.
        df_in=df_in.loc[tempCol]   
    
    rowsToDrop=df_ex.drop(df_in.index)
    df_ex=df_ex.drop(rowsToDrop.index)  
    columns_ex=df_ex.values   
    columns_in=df_in.values   

    df_in_header=df_in[:2]
    df_in=df_in[2:].apply(pd.to_numeric,errors='coerce')  
    df_in=pd.concat([df_in_header, df_in])
    
    check_column_duplicates(df_in, easting_index, northing_index, label_index)
    write_xml_tree(columns_included,output_folder,is_scaled,False,na_value)#false for is_spatial
    
    if(is_scaled is not None):
        for i in range(0,len(columns_in[0])):
            colForMinMax=columns_included[i][8:].astype(float)[~np.isnan(df_in[i][8:].astype(float))]
            data_min= min(colForMinMax)
            data_max= max(colForMinMax)#Checkit seuraaville asioille: min ja max ei oo samat, koko columni ei oo NoDataa
            scale_min=float(columns_included[i][5])
            scale_max=float(columns_included[i][6])
            for j in range(8, len(columns_in)):

                if(columns_in[j,i]!=na_value):
                    columns_in[j,i]=((scale_max-scale_min)*(float(columns_in[j,i])-data_min)/(data_max-data_min))+scale_min                 
                    #columns_in on df_in.values.
    df_in=pd.DataFrame(np.squeeze(np.stack(columns_in, axis=0))) 
    columns_in=df_in.values        
    columns=combine_csv_columns(columns_ex,columns_in)
    
    for i in range(0, len(columns[1])): 
        columns[1][i]=columns[1][i].replace("\n","")
    np.savetxt(output_folder+"/DataPreparation/EditedData.lrn", columns, delimiter="\t",header=("%"+str(len(columns)-2)+"\n"+"%"+str(len(columns[0]))), fmt="%s",comments='') #number of cols-2 to take dummy coords into account  #header=(header['rows']+"\n"+str(header['cols'])), fmt="%s",comments='')   
    print("Saved to .lrn File")
    
    
"""
Write lrn file from csv input, when input is spatial
"""    
def write_spatial_from_csv(columns,input_file,output_folder,is_scaled,is_spatial,easting_index,northing_index,label_index,na_value):
    

    columns_sorted=[]
    columns_sorted.append(columns[:,int(easting_index)])
    columns_sorted.append(columns[:,int(northing_index)])
    for i in range(0,  len(columns[0])):
        if(i!=int(easting_index) and i!=int(northing_index)):
            columns_sorted.append(columns[:,i]) 

    for i in range(0, len(columns[0])):
        if(i==0):
            columns_sorted[0][7]="x"
        elif(i==1):
            columns_sorted[1][7]="y"
  

    columns_included=[]
    columns_excluded=[]

    for i in range(0, len(columns_sorted)) :                				
        if(columns_sorted[i][4]=='0'):	                        	
            columns_excluded.append(columns_sorted[i])			              
        else:
            columns_included.append(columns_sorted[i])			             
            
    df_ex=pd.DataFrame(np.squeeze(np.stack(columns_excluded, axis=1)))        #tässä on jo vähän hitaampi vaihe. testaile tätä isolla datalla. että mitkä stepit on hitaita, ja onko kaikki tarpeellisia. esim. onko dataframeksi muuttaminen raskasta ja/tai tarpeellista?      
    df_ex = df_ex.replace('NA','nan',  regex=True)   
    df_ex=df_ex.replace(np.nan, 'nan', regex=True)
    
    df_in=pd.DataFrame(np.squeeze(np.stack(columns_included, axis=1)))
    df_in.iloc[2:,:] = df_in.iloc[2:,:].replace('NA','nan', regex=True)  
    df_in.iloc[2:,:]=df_in.iloc[2:,:].replace(np.nan, 'nan', regex=True)
    if(na_value !=""):
        na_value=float(na_value)
        df_in=df_in.replace(str(na_value),np.nan)
    for i in range(0,len(df_in.columns)): 
        tempCol=(df_in[:][i] !='nan')#create boolean array on wether data elements are valid numbers or 'nan'
        tempCol[1]=True #assign True to header, so that the header is not labeled False even if it is 'nan', because that should be a valid header as well.
        df_in=df_in.loc[tempCol]   
    
    rows_to_drop=df_ex.drop(df_in.index)
    df_ex=df_ex.drop(rows_to_drop.index)  
    columns_ex=df_ex.values   
    columns_in=df_in.values   
    
    df_in_header=df_in[:2]
    df_in=df_in[2:].apply(pd.to_numeric,errors='coerce')  
    df_in=pd.concat([df_in_header, df_in])
    
    check_column_duplicates(df_in, easting_index, northing_index, label_index)

    write_xml_tree(columns_included,output_folder,is_scaled,True,na_value)#true for Is Spatial
    
    if(is_scaled==True):
        if(na_value != ''):
            for i in range(0,len(columns_in[0])):          
                colForMinMax=columns_included[i][8:].astype(float)[~np.isnan(df_in[i][8:].astype(float))]
                colForMinMax= list(filter(lambda x: x!=float(na_value), colForMinMax))               
                data_min= min(colForMinMax)
                data_max= max(colForMinMax)#Checkit seuraaville asioille: min ja max ei oo samat, koko columni ei oo NoDataa. Näissä tapauksissa columni excludeen/poistoon.
                scale_min=float(columns_included[i][5])
                scale_max=float(columns_included[i][6])
                for j in range(8, len(columns_in[:,i])):
                    if(columns_in[j,i]!=str(float(na_value))):
                        columns_in[j,i]=((scale_max-scale_min)*(float(columns_in[j,i])-data_min)/(data_max-data_min))+scale_min 
                        columns_in[j,i]=columns_in[j,i]
                    else:
                         columns_in[j,i]=np.nan
        else:
            for i in range(0,len(columns_in[0])):
                colForMinMax=df_in[i][8:].astype(float)[~np.isnan(df_in[i][8:].astype(float))]                
                data_min= min(colForMinMax) 
                data_max= max(colForMinMax)#Checkit seuraaville asioille: min ja max ei oo samat, koko columni ei oo NoDataa
                scale_min=float(columns_included[i][5])
                scale_max=float(columns_included[i][6])
                for j in range(8, len(columns_in[:,i])):
                    columns_in[j,i]=((scale_max-scale_min)*(float(columns_in[j,i])-data_min)/(data_max-data_min))+scale_min
    
    df_in=pd.DataFrame(np.squeeze(np.stack(columns_in, axis=0)))  

    columns=combine_csv_columns(columns_ex,columns_in)
    columns=check_for_duplicate_coords(columns)

    for i in range(0, len(columns[1])): 
        columns[1][i]=columns[1][i].replace("\n","")

    np.savetxt(output_folder+"/DataPreparation/EditedData.lrn", columns, delimiter="\t",header=("%"+str(len(columns)-2)+"\n"+"%"+str(len(columns[0])-1)), fmt="%s",comments='') #-1 to take added id col to in to accoutn  #(header['rows']+"\n"+str(header['cols'])), fmt="%s",comments='')   
    print("Saved to .lrn File")
    
    
    
"""
Write lrn file from tif input
"""
def write_from_tif_input(columns, output_folder, input_file,is_scaled,na_value=""):
    header=load_input_file(input_file) #this is probably unnecessary. remove.
    id_col=[]
    for i in range(0, len(header['data'])):
        id_col.append(i)
      
    header['rows']="%"+str(header['rows'])
    header['cols']="%"+str(header['cols'])
    coltypes=[]
    for i in range(0, (len(columns[0]))):
        if i<2:
            coltypes.append(0)
        else:
            if(columns[4][i]==True):
                coltypes.append(0)
            else:
                coltypes.append(1)    
    coltypes=np.append("%9",coltypes)#%9 for id col
    header['colnames']=np.append(("id","x","y"),header['colnames']) #add id x and y to column names 
        
    columns_in=[]
    for i in range(0,len(columns[0])):
        if(columns[:,i][4]=='1'):#if column is not excluded
            columns_in.append(columns[:,i])
    write_xml_tree(columns_in,output_folder,is_scaled,True,na_value) #True for is_spatial

    for i in range(2, (len(header['colnames'])-1)):   #start from 2 to skip x and y columns
        if(is_scaled==True):           
            scale_min=float(columns[:,i][5])
            scale_max=float(columns[:,i][6])
        if(columns[:,i][4]=='1'): #if column is not excluded
            array_for_minmax= np.delete(columns[8:,i], np.where(columns[8:,i] == na_value)) #start from 8 to skip column headers
            data_min= min(array_for_minmax.astype(float))
            data_max= max(array_for_minmax.astype(float))            
            if(is_scaled==True):            
                for j in range(8, len(columns)):
                     if(columns[j,i]!=na_value):
                         columns[j,i]=(scale_max-scale_min)*(columns[j,i].astype(float)-data_min)/(data_max-data_min)+scale_min  
                     
    for i in range (1, len(columns[0])):#1 to take ID col into account.
        columns[0][i]=coltypes[i]
        columns[1][i]=columns[1][i].replace('\n', '')
        
        
    
    id_col_with_header=np.vstack((coltypes[0],header['colnames'][0],np.c_[id_col]))  #create id column       
    columns_stacked=np.vstack((columns[4,:],columns[:][7:]))#build a frankenstein's monster out of coltytpes,colheaders and columns themselves
    columns=np.hstack((id_col_with_header, columns_stacked))
    """
    AAAAA^
    """
    df=pd.DataFrame(columns)
    df.apply(pd.to_numeric,errors='coerce')
    
    if(na_value != ""):
        na_value=float(na_value)
        df=df.replace(str(na_value),np.nan)
        df=df.dropna()    

    columns=df.values             
    np.savetxt(output_folder+"/DataPreparation/EditedData.lrn", columns, delimiter="\t",header=(header['rows']+"\n"+str(header['cols'])), fmt="%s",comments='')  
    print("Saved to .lrn File")




"""
Create xml-tree containing data transformation stage stats and and write it to file (DataStats.xml). This information is later used to reverseve (possible) scaling from the SOM calculation result data.
"""
def write_xml_tree(columns_included, output_folder,is_scaled,is_spatial,na_value=""):
    root = ET.Element("data") 
    for i in range(0,len(columns_included)):
        if(na_value !=''):
            colForMinMax=columns_included[i][8:].astype(float)[~np.isnan(columns_included[i][8:].astype(float))]
            colForMinMax= list(filter(lambda x: x!=float(na_value), colForMinMax))
            data_min= min(colForMinMax)
            data_max= max(colForMinMax)
        else:
            colForMinMax=columns_included[i][8:].astype(float)[~np.isnan(columns_included[i][8:].astype(float))]
            data_min= min(colForMinMax)
            data_max= max(colForMinMax)
        newElement=ET.Element(columns_included[i][7].replace('\"','')	)     
        minElement=ET.Element("min")
        minElement.text=str(data_min)
        maxElement=ET.Element("max")
        maxElement.text=str(data_max)      
        is_log_transformed=columns_included[i][3] 
        is_winsorized=columns_included[i][0]
        if (is_scaled==True):
            scale_min=columns_included[i][5]
            scale_max=columns_included[i][6]
            scaleMinElement=ET.Element("scaleMin")
            scaleMinElement.text=str(scale_min)
            scaleMaxElement=ET.Element("scaleMax")
            scaleMaxElement.text=str(scale_max)
        winsorElement=ET.Element("winsorized")
        winsorElement.text=str(is_winsorized)
        if(is_scaled==True):
            winsor_min=columns_included[i][1]
            winsor_max=columns_included[i][2]
            winsorMinElement=ET.Element("winsorMin")
            winsorMinElement.text=str(winsor_min)
            winsorMaxElement=ET.Element("winsorMax")
            winsorMaxElement.text=str(winsor_max)
        logTransformElement=ET.Element("logTransform")
        logTransformElement.text=str(is_log_transformed)
        if(is_scaled==True):   
            newElement.append(scaleMinElement)
            newElement.append(scaleMaxElement)
        newElement.append(logTransformElement)
        newElement.append(winsorElement)
        if(is_scaled==True):
            newElement.append(winsorMinElement)
        newElement.append(minElement)
        newElement.append(maxElement)
        root.append(newElement)
    
    scaledElement=ET.Element("isScaled")
    scaledElement.text=str(is_scaled)
    root.append(scaledElement)     
    spatialElement=ET.Element("isSpatial")
    spatialElement.text=str(is_spatial)
    root.append(spatialElement)
    
    spatialElement=ET.Element("noDataValue")
    spatialElement.text=str(na_value)
    root.append(spatialElement)
    
    xmlstr = minidom.parseString(ET.tostring(root,encoding='utf-8', method='xml')).toprettyxml(indent="   ")
    with open(output_folder+"/DataStats.xml", "w") as f:
        f.write(xmlstr)  
            
        
        


"""
Create data columsn with empty dummy coordinate data, used by nonspatial csv option.
"""
def create_dummy_coordinates(columns):
    x_col=[]
    y_col=[]
    for i in range(0, len(columns)): 
        x_col.append(0)  
        y_col.append(0) 
    x_col[7]="x"
    y_col[7]="y"
    columns=np.hstack((np.array(x_col).reshape(-1,1),np.array(y_col).reshape(-1,1),columns))
    return columns


"""
Populate dataframes used with csv option. UNUSED? DEPRECATED?
"""
def populate_csv_DataFrames(columns_excluded,columns_included,columns_sorted,indexModifier=0):
    global df_ex
    global df_in
    global columns_ex
    global columns_in
    global na_value
    for i in range(0, len(columns_sorted)) :                				
        columns_sorted[i][1][0]=columns_sorted[i][1][0].replace('\n', '')	
        if(columns_sorted[:,i][4]=='0'):		                        	
            columns_excluded.append(columns_sorted[i])			              
        else:
            columns_included.append(columns_sorted[i])			             
            
    df_ex=pd.DataFrame(np.squeeze(np.stack(columns_excluded, axis=1)))              
    df_ex = df_ex.replace('NA','nan',  regex=True)   
    df_ex=df_ex.replace(np.nan, 'nan', regex=True)
    
    df_in=pd.DataFrame(np.squeeze(np.stack(columns_included, axis=1)))
    df_in.iloc[2:,:] = df_in.iloc[2:,:].replace('NA','nan', regex=True)  
    df_in.iloc[2:,:]=df_in.iloc[2:,:].replace(np.nan, 'nan', regex=True)
    if(na_value !=""):
        na_value=float(na_value)
        df_in=df_in.replace(str(na_value),np.nan)
    for i in range(0,len(df_in.columns)): 
        tempCol=(df_in[:][i] !='nan')#create boolean array on wether data elements are valid numbers or 'nan'
        tempCol[1]=True #assign True to header, so that the header is not labeled False even if it is 'nan', because that should be a valid header as well.
        df_in=df_in.loc[tempCol]   
    
    rows_to_drop=df_ex.drop(df_in.index)
    df_ex=df_ex.drop(rows_to_drop.index)  
    columns_ex=df_ex.values   
    columns_in=df_in.values   
    df_in_header=df_in[:2]
    df_in=df_in[2:].apply(pd.to_numeric,errors='coerce')  
    df_in=pd.concat([df_in_header, df_in])
        
"""
Combine used columns into a single numpy array
"""
def combine_csv_columns(columns_ex,columns_in):

    columns=np.hstack((columns_ex, columns_in)) #this can't be the most efficient way to do this. 
    columns=((pd.DataFrame(columns)).dropna()).values
    id_col=[]
    columns[0]=columns[4]#move coltype to beginning
    columns[1]=columns[7]#move header to beginning
    columns=np.delete(columns,range(2,8),0)
    for i in range(0, len(columns)-2): 
        id_col.append(i)  
    id_col_with_header=np.vstack((["%9"],["id"],np.c_[id_col]))    
    columns=np.hstack((id_col_with_header, columns))  
    return columns
    
    
        

def check_for_duplicate_coords(columns):
    ##Check for duplicate coordinates
    d = dict()
    for i in range (2, len(columns)):# start at 2 because we are now working with trimmed columns
        d[tuple((columns[i][1], columns[i][2]))] = i
    if(len(columns)-2>len(d)):
        print("Warning: Data contains duplicate coordinates. The duplicates are written over, so that only the last duplicate instance is kept.")
        values=list(d.values())
        columns[values]
        columns=np.vstack((columns[0:2],columns[values]))
    return columns

def check_column_duplicates(df_in, easting_index, northing_index, label_index):
    for i in range(len(df_in.columns)):
        if (df_in.columns[i] != easting_index) and (df_in.columns[i] != northing_index) and (df_in.columns[i] != label_index):
            #check_column_duplicates(df_in,i)
            df = df_in.iloc[8:]
            array = df[i].to_numpy()
            if (array[0] == array).all():
                raise ValueError('All rows in a column are {}.'.format(array[0]))
    
def combine_to_lrn_file(input_file,output_folder,columns,column_type_list,is_scaled,is_spatial,na_value=""):

    file_type=input_file[-3:].lower()

    for i in range(0,len(column_type_list)):
        if column_type_list[i]=="exclude":             
            columns[:,i][4]=0
        else:
            columns[:,i][4]=1
    easting_index=None
    northing_index=None
    if(is_spatial==True):
        if ('x' not in column_type_list or 'y' not in column_type_list):
            raise ValueError("Please select X and Y columns or set the dataset to non-spatial data before proceeding.")
        easting_index=column_type_list.index("x")
        northing_index=column_type_list.index("y")
        columns[:,easting_index][4]=0#set x, y and label columns as excluded
        columns[:,northing_index][4]=0
    label_index=None
    if('label' in column_type_list):
        label_index=column_type_list.index("label")
        columns[:,label_index][4]=0
        columns[:,label_index][7]='label'
    
    if na_value !="":
        na_value=str(float(na_value))#make sure the string is in float format.
    """
    Parsi läpi vasemmanpuoleisimman columnin radiobuttionien arvot. niistä parsitaan: 
            -eastingIndex
            -northingIndex
            -labelIndex
            -exclude_list
            
    exclude listiä ei tarvii enää kuljettaa erillisenä listana, vaan sille column typellehän on varattu ihan paikka jokaisen columnin alku binääri headereissa.
    
    eli nuo mukana kulkevat listat voi heittää kokonaan pois. mutta columns_included & columns_excluded jako tehdään yhä.
    """  
        
    if(file_type=="tif"):
        write_from_tif_input(columns,output_folder,input_file,is_scaled,na_value)#ain't no labels, varying x&y cols or option for nonspatial in GeoTIFFs
        

    if(file_type=="csv"):
        if (is_spatial==True):
            write_spatial_from_csv(columns,input_file,output_folder,is_scaled,is_spatial,easting_index,northing_index,label_index,na_value)#
        else: #if easting index is none                    
            write_nonspatial_from_csv(columns,input_file,output_folder,is_scaled,na_value,label_index)     
            
    print("Saved to .lrn file")
