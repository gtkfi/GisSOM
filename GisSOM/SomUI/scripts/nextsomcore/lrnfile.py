# -*- coding: utf-8 -*-
"""
The module contains  functions to read lrn-files

@author: Janne Kallunki
"""

import numpy as np

def load_lrn_file(input_file):
    lrn_header = read_lrn_header(input_file)
    datacols = [i for i, x in enumerate(lrn_header['coltypes']) if x == 1]
    data = np.loadtxt(
        input_file, 
        dtype='float32',
        delimiter='\t',
        skiprows=lrn_header['headerlength'] ,
        usecols=(datacols))
    lrn_header['data'] = data
    return lrn_header

def read_lrn_header(input_file):
    linenum = 0
    with open(input_file) as fh:
        while True:
            line = fh.readline()
            linenum += 1
            if line.startswith('#'):
                continue
            if line.startswith('%'):
                if not 'rows' in locals():
                    try:
                        rows = int(line[1:].rstrip())
                    except ValueError:
                        raise Exception("Failed to obtain valid row count from lrn-file.")
                    continue
                elif not 'cols' in locals():
                    try:
                        cols = int(line[1:].rstrip())
                    except ValueError:
                        raise Exception("Failed to obtain valid column count from lrn-file.")
                    continue
            if not 'colmap' in locals():
                try:
                    colmap = [int(x) for x in line[1:].rstrip().split()]
                except ValueError:
                    raise Exception("Failed to convert column type values")
                continue
            if not 'colnames' in locals():
                colnames = line.split()
                break

    if len(colnames) != len(colmap):
        print(colnames)
        print (colmap)
        raise Exception("Column names don't match with the column types.")
    return {'file': input_file, 'rows': rows, 'cols': cols, 'coltypes': colmap, 'colnames': colnames, 'headerlength': linenum, 'data': None, 'filetype': 'lrn'}

def read_lrn_coordinate_columns(lrn_header):
    coord_cols = [i for i, x in enumerate(lrn_header['coltypes']) if x == 0 and lrn_header['colnames'][i].upper() in ['X', 'Y', 'Z']]
    fmt = ('%f ' * len(coord_cols)).rstrip()
    return _read_columns(lrn_header, coord_cols, fmt)

def read_lrn_data_columns(lrn_header):
    data_cols = [i for i, x in enumerate(lrn_header['coltypes']) if x == 1]
    fmt = ('%f ' * len(data_cols)).rstrip()
    return _read_columns(lrn_header, data_cols, fmt)

def _read_columns(lrn_header, columns, fmt=''):
    if not type(columns) in (list, tuple):
        raise TypeError('Invalid type: columns must be a list or tuple')
    colnames = ([lrn_header['colnames'][i] for i in columns])
    data = np.loadtxt(
                lrn_header['file'],
                dtype='float32', 
                delimiter='\t',
                skiprows=lrn_header['headerlength'] , 
                usecols=(columns))
    return {'data': data, 'colnames': colnames, 'fmt': fmt}
