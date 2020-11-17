# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 09:46:21 2019

@author: shautala
"""

import numpy as np
from osgeo import gdal
import os

"""
Old version of the script, current version directly under /scripts 
"""
def load_geotiff_files(input_file_list):
    
    #Following code is done under the assumption that the coordinate systems have been already checked to match. So, we can use the coordinates of a single for all columns.
    geotiff_list_as_string=input_file_list 
    returndata=[]
    colnames=[]
    if("," in geotiff_list_as_string):
        geotiff_list_2=geotiff_list_as_string.split(",")#geotiff_list is str. geotiff_list_2 is array
    else:
        geotiff_list_2=[geotiff_list_as_string]

    for geotiffpath in geotiff_list_2:         
        print(geotiffpath)
        src_ds = gdal.Open(geotiffpath)
        data = src_ds.ReadAsArray()
        temp=data.flatten(order='C')
        if(len(returndata)>0):
            returndata=np.column_stack((returndata,temp))
        else:
            returndata=temp
        colnames.append(os.path.basename(geotiffpath))            
    rows=len(returndata)   
    if("," in geotiff_list_as_string):
        cols=len(returndata[0])    
    else:
        cols=1           
    return {'rows': rows, 'cols': cols, 'colnames': colnames, 'headerlength': 0, 'data': returndata, 'filetype': 'geotiff','originaldata':data}
    

"""
required to return: ['rows', 'cols', 'colmap', 'colnames']
-rows:easy
-cols:easy
-colmap: not necessary. there is only 1 data column, it will be used.
-colanmes: use name of raster file/user specified input.
"""

"""
This is required, accessed from core
"""
def read_geotiff_coordinate_columns(geotiff_header):
    coordinates_x=[]
    coordinates_y=[]            
    data=geotiff_header['originaldata']
    for i in range(0,len(data)):
        for j in range(0,len(data[i])):
            coordinates_x.append(j)
            coordinates_y.append(i)
    coordinates=np.column_stack((coordinates_x,coordinates_y))   #these coordinates are still table indices, not actual real world coordinates.

    return {'data': coordinates, 'colnames':["x","y"], 'fmt': '%f %f'}    

"""
    This is required, accessed from core
"""
def read_geotiff_data_columns(geotiff_header):
    data_cols = [i for i, x in enumerate(geotiff_header['colnames']) if 0 == 0] #   replace this kludge with something sensible
    fmt = ('%f ' * len(data_cols)).rstrip()
    return {'data': geotiff_header['data'], 'colnames': geotiff_header['colnames'], 'fmt': fmt}
