# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 09:11:14 2019

@author: shautala
"""

from osgeo import gdal
import subprocess
import sys
from pip._internal import main as pip
import os
#os.system('python -m pip install argh --proxy=http://suoja-proxy.vyv.fi:8080')
#def install(package):
#    subprocess.call([sys.executable, "-m", "pip", "install", package, "--proxy=\"https://suoja-proxy.vyv.fi:8080\""])
    
#install("argh")



pip_install_argument = "install"
pip_optional_params="--proxy=suoja-proxy.vyv.fi:8080"
# packages to install
packages_to_install = [
        "numpy",        # math magic 1
        "scipy",        # math magic 2
        "scikit-learn",
        "matplotlib",
        "pandas",
        "plotly",
        "seaborn",
        "somoclu==1.7.4",
        "dash",
        "gevent",
        "GDAL",
        "matplotlib-scalebar",
        "argh"
        ]

def install(packages):
    """installes given packages via pip

    Args:
        package names as list

    Returns:
        None

    """
    global pip_install_argument
    for package in packages:
        #pip([pip_install_argument, package, pip_optional_params])
        os.system('python -m pip install '+package+' --proxy=http://suoja-proxy.vyv.fi:8080')
        #subprocess.call([sys.executable, "-m", "pip", "install", package])

if __name__ == '__main__':
    print("testi")
    install(packages_to_install)

geotiffpath="C:/Users/shautala/Documents/GeoTIFF/AEM_Re_500m.tif"
#geotiffpath="C:/Users/shautala/Documents/GeoTIFF/AEM_ReIm_500m.tif"
#geotiffpath="C:/Users/shautala/Documents/GeoTIFF/AM_DGRF_500m.tif"
src_ds = gdal.Open(geotiffpath)
data = src_ds.ReadAsArray()
meta=src_ds.GetMetadata()


width = src_ds.RasterXSize
height = src_ds.RasterYSize
gt = src_ds.GetGeoTransform()
minx = gt[0]
miny = gt[3] + width*gt[4] + height*gt[5] 
maxx = gt[0] + width*gt[1] + height*gt[2]
maxy = gt[3] 



prj=src_ds.GetProjection()

#vertailu...
#eka geotiff luettaessa nää vois ottaa talteen.
#ja aina seuraavia luettaessa verrata näihin että täsmääkö.

#mitä tarvii verrata: widht ja height ei ainakaan tarvi.
#minx miny maxx maxy, ja joku osa projista.