NextSomCore 0.1 - How to install

Download and install C++ Compiler for Python 2.7:
https://www.microsoft.com/en-us/download/details.aspx?id=44266

Open command prompt and type:
cd path\where\sources\are\
set path=c:\Python2710\ArcGIS10.4;c:\Python2710\ArcGIS10.4\Scripts;%path%
Update pip
pip install --upgrade pip  (or python -m pip install --upgrade pip)

Install system wide:
python setup.py install
nextsom_wrap.py can be called everywhere

Run locally:
python nextosom_wrap.py <arguments>

Build binary, source and wheel packages
python setup.py bdist sdist --formats=zip bdist_wheel 

Build a standalone executable(includes python interpreter and all used libraries in one executable nextsom_wrap.exe):
pip install pyinstaller
pyinstaller nextsom_wrap.spec

Command line arguments for nextsom_wrap.py (nextsom_wrap.py --help):
usage: nextsom_wrap.py [-h]
                       input_file output_file_geospace output_file_somspace
                       som_x som_y epochs

Script for generating self organizing maps

positional arguments:
  input_file            Input file(*.lrn)
  output_file_geospace  Text file that will contain calculated values: {X Y Z}
                        data1 data2 dataN som_x som_y cluster b_data1 b_data2
                        b_dataN in geospace.
  output_file_somspace  Text file that will contain calculated values: som_x
                        som_y b_data1 b_data2 b_dataN umatrix cluster in
                        geospace.
  som_x                 X dimension of generated SOM
  som_y                 Y dimension of generated SOM
  epochs                Number of epochs to run

optional arguments:
  -h, --help            show this help message and exit


Limitations:
-Compiled with ArcGIS 10.4.1 and Python 2.7.10
-X,Y,Z columns are mandadory in the input file. Should be optional. Will be fixed.
-Only equal som_x som_y works correctly (10,10 20,20 100,100). This is under inspection
-No CUDA support included in this build. Parallel CPU support is the default.
-No hits per BMU column at the moment. Will be added
-Cluster size is 8. Should be input parameter. Will be fixed.
-No binary file format. Numpy on disk binary array format could be one possibility. 




