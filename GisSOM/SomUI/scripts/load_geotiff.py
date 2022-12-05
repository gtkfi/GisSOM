# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 09:46:21 2019
Script for reading geotiff input data files.
@author: shautala
"""

import numpy as np
from osgeo import gdal
import os
import sys

def load_geotiff_files(input_file_list):
    
    width_0 = None
    height_0 = None
    gt_0 = None
    prj_0=None
    path_0=None
    geotiff_list_as_string=input_file_list # At this points the assumption is made that the coordinates of separate files are identical. So the coordinates can just be taken from any one of the individual files.
    returndata=[]
    colnames=[]
    if("," in geotiff_list_as_string):
        geotiff_list_2=geotiff_list_as_string.split(",")#geotiff_list is str. geotiff_list_2 is array #maybe change the parameter name...?
    else:
        geotiff_list_2=[geotiff_list_as_string]
    for geotiffpath in geotiff_list_2: 
        src_ds = gdal.Open(geotiffpath)       
        if(width_0 is None):        #stash baseline values on first loop, for checking that projection etc. match for all files
            width_0 = src_ds.RasterXSize
            height_0 = src_ds.RasterYSize
            gt_0 = src_ds.GetGeoTransform()
            prj_0=src_ds.GetProjection()
            path_0=geotiffpath
        width = src_ds.RasterXSize
        height = src_ds.RasterYSize
        gt = src_ds.GetGeoTransform()
        prj=src_ds.GetProjection()
        if(gt!=gt_0):
            print("Warning: Geotransform of "+geotiffpath+" does not match with "+path_0)
        if(prj!=prj_0):
            print("Warning: Projection of "+geotiffpath+" does not match with "+path_0)
        if(width!=width_0 or height!=height_0):
            sys.exit("Error: Grid of "+geotiffpath+" does not match."+path_0)
        data = src_ds.ReadAsArray()
        flat=data.flatten(order='C')
        
        if(len(returndata)>0):
            returndata=np.column_stack((returndata,flat))
        else:
            returndata=flat
        colnames.append(os.path.basename(geotiffpath))            
    rows=len(returndata)   
    if("," in geotiff_list_as_string):
        cols=len(returndata[0])    
    else:
        cols=1            
    band=src_ds.GetRasterBand(1)
    noDataValue= band.GetNoDataValue()
    dataType=band.DataType
    return {'rows': rows, 'cols': cols, 'colnames': colnames, 'headerlength': 0, 'data': returndata, 'filetype': 'geotiff','originaldata':data, 'geotransform':gt, 'noDataValue':noDataValue, 'dataType':dataType}   

def read_geotiff_coordinate_columns(geotiff_header):
    coordinates_x=[]
    coordinates_y=[]           
    data=geotiff_header['originaldata']
    gt=geotiff_header['geotransform'] #gt[0], gt[1], gt[3] and gt[4] have all that is needed 
    for i in range(0,len(data)):
        for j in range(0,len(data[i])):
            coordinates_x.append(j*gt[1]+gt[0])
            coordinates_y.append(i*gt[5]+gt[3])
    coordinates=np.column_stack((coordinates_x,coordinates_y)) #Coordinates are just indexes at this stage. TODO: use gt to tranform them back into real world values.
    return {'data': coordinates, 'colnames': geotiff_header['colnames'], 'fmt': '%f %f'} 

def read_geotiff_data_columns(geotiff_header):
    return {'data': geotiff_header['data'], 'colnames': geotiff_header['colnames'], 'fmt': ('%f ' * 3).rstrip()} 



