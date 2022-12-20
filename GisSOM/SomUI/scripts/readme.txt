Current python build version: 3.9

Required python packages:

matplotlib
numpy
seaborn
pandas
gevent
dash
plotly
GDAL
flask
scipy
scikit-learn
somoclu 1.7.4
GDAL 3.4.3

GDAL installation from pip does not work, easiest way to install is download a pre-built wheel and install that locally with pip.




Building executables with PyInstaller:
The provided Batch File (PyInstallerAuto.bat, in scripts folder) contains series of commands for building executables with PyInstaller, and copying them to the Solution scripts/executables folder, and the corresponding bin and release folders.
Before running update the two variables in the beginning of the batch file: path for the solution directory, and path for the PyInstaller output directory.

