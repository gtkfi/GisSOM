# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:10:46 2019

Script that servers as launch point to loading geotiff, csv or lrn files. Possibly more filetypes in the future

@author: shautala
"""

from lrnfile import load_lrn_file, read_lrn_coordinate_columns, read_lrn_data_columns, lrn_read_lrn_header
from load_geotiff import load_geotiff_files, read_geotiff_coordinate_columns, read_geotiff_data_columns
from load_csv import load_csv_file, read_csv_coordinate_columns,read_csv_data_columns,read_csv_header

"""
eli lopulta vasta täällä tarvii olla checki inputfilen tyypistä
"""


#load input file
def load_input_file(input_file):#input file in case of lrn, input file list in case of geoTiff
     if(input_file[-3:].lower()=="lrn"):#if input is lrn
        lrn_header=load_lrn_file(input_file)
        return lrn_header
     elif(input_file[-3:].lower()=="csv"):
        csv_header=load_csv_file(input_file)
        return csv_header
     else: 
        geotiff_header=load_geotiff_files(input_file)
        return geotiff_header
    

def read_coordinate_columns(header):   
    if(header['filetype']=='lrn'):
        coords=read_lrn_coordinate_columns(header)    
        return coords
    elif(header['filetype']=='csv'):
        coords=read_csv_coordinate_columns(header)
        return coords
    else:
        coords=read_geotiff_coordinate_columns(header)
        return coords


def read_data_columns(header):
    if(header['filetype']=='lrn'):
        data=read_lrn_data_columns(header)
        return data
    elif(header['filetype']=='csv'):
        data=read_csv_data_columns(header)
        return data
    else:
        data=read_geotiff_data_columns()
        return data


def read_header(input_file):
    if(input_file[-3:].lower()=="lrn"):
        lrn_header=lrn_read_lrn_header(input_file)
        return lrn_header
    elif(input_file[-3:].lower()=="csv"):
        csv_header=read_csv_header(input_file)
        return csv_header
    else:
        return None
    
