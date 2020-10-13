# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:50:45 2019

@author: shautala
"""
import numpy as np
    
def load_csv_file(input_file):
    csv_header = read_csv_header(input_file)
    datacols = [i for i, x in enumerate(csv_header['colnames']) if csv_header['colnames'][i].upper() not in ['X', 'Y']]
    data = np.loadtxt(
        input_file, 
        dtype='float32',
        delimiter=',',
        skiprows=1
        ,usecols=(datacols))
    csv_header['data'] = data
    return csv_header
             
def read_csv_coordinate_columns(csv_header):
    coord_cols = [i for i, x in enumerate(csv_header['colnames']) if csv_header['colnames'][i].upper() in ['X', 'Y']]
    fmt = ('%f ' * len(coord_cols)).rstrip()
    return _read_columns(lrn_header, coord_cols, fmt)

def read_csv_data_columns(csv_header):
    data_cols = [i for i, x in enumerate(csv_header['colnames']) if csv_header['colnames'][i].upper() not in ['X', 'Y']]#Tämän jos korvaa sillä että lue indeksistä 2 alkaen tai sitten että names ei x tai y. oisko se jälkimmäine paras. 
    fmt = ('%f ' * len(data_cols)).rstrip()
    return _read_columns(lrn_header, data_cols, fmt)

def _read_columns(csv_header, columns, fmt=''):
    if not type(columns) in (list, tuple):
        raise TypeError('Invalid type: columns must be a list or tuple')
    colnames = ([csv_header['colnames'][i] for i in columns])
    data = np.loadtxt(
                csv_header['file'],
                dtype='float32', 
                delimiter='\t',
                skiprows=csv_header['headerlength'] , 
                usecols=(columns))
    return {'data': data, 'colnames': colnames, 'fmt': fmt}

def read_csv_header(input_file):
    data = np.loadtxt(
        input_file, 
        dtype='float32',
        delimiter=',',
        skiprows=1)
    rows=len(data)
    cols=len(data[0])  
    
    with open(input_file) as fh:
        header_line = fh.readline()
        colnames=header_line.split(",")
    
    return {'file': input_file, 'rows': rows, 'cols': cols, 'colnames': colnames, 'headerlength': 0, 'data': None, 'filetype': 'csv'}