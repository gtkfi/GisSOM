# GisSOM

GisSOM performs unsupervised self-organizing maps (SOM) clustering to a given dataset. Results are presented in the SOM coordinates, and also spatial coordinates if given. Also scatter and boxplots are used to visualize the per cluster data distribution.  

<img src="/Screenshots/som_2.png" width="800" height="400">
  
<sup>Som results plotted in somspace</sup>

## Features

* Spatial or non-spatial input data
  * CSV and GeoTIFF
Results in SOM and geographic coordinates
  * CSV, txt and image files
* Interactive plot
  * highlighting data associated with a specific cluster or SOM cell
  * relation between SOM and geographic space
* Easy installation
  * Built-in Python scripts

## Screenshots

Data preparation:  
<img src="/Screenshots/som_1.png" width="800" height="400">
  
Results in Geospace:  
<img src="/Screenshots/som_3.png" width="800" height="400">
  
Interactive plot:  
<img src="/Screenshots/Interactive_plot.gif" width="400" height="200">  

## Installation

To download the installer for GisSOM, go to the Releases-section (<https://github.com/gtkfi/GisSOM/releases>), and download the GisSOM_Release.zip -file, which contains the installer along with the user manual and license information.

## About the code

GisSOM is implemented in C# and XAML using the Windows Presentation Foundation (WPF) framework, according to the Model-View-ViewModel (MVVM) design model. Computational tasks related to data preprocessing, som calculation and visualization of the results are handled by Python scripts. The software uses Python version 3.7, and the Python scripts and the python environment are bundled into executables using PyInstaller.

## Development

If you wan't to develop GisSOM, or use it or parts of it in your own projects in accordance with it's license, you are welcome to do so. Just clone or download the code, open the solution with VS 2019, set up the Nuget packages, and you should be ready to go.
If you want to edit and run your own versions of the python scripts, you're going to need a working installation of Python 3.7, with all the required libraries installed (required libraries are listed in the Tech Spec file, under the GisSOM/SomUI/Documents folder).
GisSOM uses bundled python executables by default, but this can be switched off by setting the usePyExes-variable in the SomTools class (rows 44 and 45 in version 1.1.0), and providing your Python installation path in the pythonPath-variable.

```C#
private string pythonPath ="C:/Your/Python/Path/pythonw.exe";
private bool usePyExes = false;
```

<sup>All set for debugging!</sup>

## Contirubte  

If you want to contribute to GisSOM, you can just fork the repository, and submit a pull request with your changes.  
  
## History

30.08.2021 GisSOM beta version 1.1 release  
17.11.2020 GisSOM beta version 1.0.1 release  
12.10.2020 GisSOM beta version 1.0 release  
