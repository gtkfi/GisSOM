import os
import sys
import subprocess
import platform

""" 
Input:
1) Working directory
2) Path of python exe file
3) Force reinstall (true or false)
"""
#This is a relic from times when pyhon was not bundled in the software. script for installing necessary python packages.

platform=platform.architecture()
working_dir=sys.argv[1]
python_path=sys.argv[2]
force_reinstall=((sys.argv[3])).lower() #as true or false.

#Install GDAL: This is separate, because it is installed from a pre-built wheel.
print("checking package GDAL")
if(platform[0]=='64bit'):
    if(force_reinstall=="true"):
        os.system(python_path+' -m pip install --force-reinstall'+working_dir+"/GDAL-3.0.1-cp37-cp37m-win_amd64.whl")   
    else:
        os.system(python_path+' -m pip install '+working_dir+"/GDAL-3.0.1-cp37-cp37m-win_amd64.whl")  
else:
    if(force_reinstall=="true"):
        os.system(python_path+' -m pip install --force-reinstall '+working_dir+"/GDAL-3.0.1-cp37-cp37m-win32.whl")
    else:
        os.system(python_path+' -m pip install '+working_dir+"/GDAL-3.0.1-cp37-cp37m-win_amd64.whl")  
    
      
# packages to install. Maybe for later versions this could be read from a txt file? this way it would be easy for even a maallikko to add a package to the install list.
# #should upgrade pip be added to the list?
packages_to_install = [
        "numpy",       
        "scipy",        
        "scikit-learn",
        "matplotlib==3.1.0",
        "pandas",
        "plotly",
        "seaborn",
        "somoclu==1.7.4",
        "dash",
        "gevent",
        "matplotlib-scalebar",
        ]
#remove matlpotlib when version 3.1.2 is released (3.1.1 fails to produce proper heatmaps)
#Install all other packages besides GDAL:
def install(packages):
    si = subprocess.STARTUPINFO()               
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW #Don't open cmd window
    for package in packages:
        print("Checking package "+package+"\n")
        if(force_reinstall=="true"):
            result=subprocess.check_output(python_path+' -m pip install --upgrade --force-reinstall '+package+' --proxy=http://suoja-proxy.vyv.fi:8080',startupinfo=si)
        else:
            result=subprocess.check_output(python_path+' -m pip install '+package+' --proxy=http://suoja-proxy.vyv.fi:8080',startupinfo=si)       
        print(result)
        sys.stdout.flush() #flust stdout to prevent text buffering. This will most likely be replaced with -u command line param.
    print("\n")
    sys.stdout.flush()
    print("\n")
    sys.stdout.flush()
    print("done")
    print("--------")
    print("Configuration finished.")

if __name__ == '__main__':
    install(packages_to_install)


