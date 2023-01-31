# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 13:08:04 2019

Script to edit data columns saved as numpy arrays saved in binary format. Actual data begins around index 8, the first entries
are used as a header to mark whether data is winsorized, log transformed, is column excluded, winsormin, winsor max, etc...
@author: shautala
"""
import numpy as np
#import sys


#the input column is from a numpy 2d array, return column type is the same
def edit_column(column, isWinsorized,winsorMin,winsorMax,isLogTransformed,ColumnType,scaleMin,scaleMax,noData=None):
    #if input contains optional noData value argument
    if(noData is not None): 
        noDataValue=str(float(noData)) #nyt tähän versioon tän vois tietty toimittaa vaan suoraan oikeassa muodossa. mutta olkoon ensi alkuun näin.
        #Logarithm
        columnValues=column[8:]
        columnValues=columnValues[(columnValues!=noDataValue)]   
        if(isLogTransformed=='true' or isLogTransformed=='True'):
            min_value=np.nanmin(columnValues.astype(np.float64)) # select min value for normalizing data
            column[3]='true' 
            for x in range(8, len(column)): 
                if(column[x]!=noDataValue):
                    column[x]=(float(column[x])-float(min_value))+1 #normalize data before log transform so that all values >=1
                    column[x]=np.log(float(column[x]))   

        if(isWinsorized=='true' or isWinsorized=='True'):
            column[0]='true'
            column[2]=winsorMax
            column[1]=winsorMin
            for x in range (8, len(column)):
                if(column[x]!=noDataValue):
                    if float(column[x])>float(winsorMax):
                        column[x]=float(winsorMax)
                    elif float(column[x])<float(winsorMin):
                        column[x]=float(winsorMin)
         
        column[4]=ColumnType      
        return(column)

    #input doesn't contain nodata value:
    else:
        columnValues=column[8:]
        if(isLogTransformed=='true' or isLogTransformed=='True'):
            min_value=np.nanmin(columnValues.astype(np.float64)) # select min value for normalizing data            
            column[3]='true'
            for x in range(8, len(column)):
                column[x]=(float(column[x])-float(min_value))+1 #Normalize data for log transform, so that all values >=1
                column[x]=np.log(float(column[x]))
        #Winsorize
        if(isWinsorized=='true' or isWinsorized=='True'):
            column[0]='true'
            column[2]=winsorMax
            column[1]=winsorMin
            for x in range (8, len(column)):
                if float(column[x])>float(winsorMax):
                    column[x]=float(winsorMax)
                elif float(column[x])<float(winsorMin):
                    column[x]=float(winsorMin)
        column[5]=scaleMin
        column[6]=scaleMax                         
        column[4]=ColumnType       

        return(column)

        