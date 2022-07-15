# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:50:45 2019
Script for loading csv input data files
@author: shautala
"""
import numpy as np

    
def load_csv_file(input_file):
    csv_header = read_csv_header(input_file)
    datacols = [i for i, x in enumerate(csv_header['colnames']) if i>=2]
    data = np.loadtxt(
        input_file, 
        dtype='str',
        delimiter=',',
        skiprows=1,
        encoding="utf-8-sig",
        usecols=(datacols))
    csv_header['data'] = data
    return csv_header 
           
def read_csv_coordinate_columns(csv_header):
    coord_cols=[]   #csv just assumes that coord cols are the two first cols. 
    coord_cols.append(0)
    coord_cols.append(1)
    fmt = ('%f ' * len(coord_cols)).rstrip()
    return _read_columns(csv_header, coord_cols, fmt)

def read_csv_data_columns(csv_header):
    data_cols=[]
    for i in range(2, len(csv_header['colnames'])):
        data_cols.append(i)
    return _read_columns(csv_header, data_cols)

def _read_columns(csv_header, columns, fmt=''):
    if not type(columns) in (list, tuple):
        raise TypeError('Invalid type: columns must be a list or tuple')
    colnames = ([csv_header['colnames'][i] for i in columns])
    data = np.loadtxt(
                csv_header['file'],
                dtype='float32', 
                encoding="utf-8-sig",
                delimiter=',',
                skiprows=csv_header['headerlength'] , 
                usecols=(columns))
    return {'data': data, 'colnames': colnames, 'fmt': fmt}


def read_csv_header(input_file):
    data = np.loadtxt(
        input_file, 
        dtype='str',
        delimiter=',',
        skiprows=1,
        encoding="utf-8-sig")
    rows=len(data)
    cols=len(data[0])  
    
    with open(input_file,encoding='utf-8-sig') as fh:
        header_line = fh.readline()
        colnames=header_line.split(",")
    
    return {'file': input_file, 'rows': rows, 'cols': cols, 'colnames': colnames, 'headerlength': 1, 'data': None, 'filetype': 'csv'}

