using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.CommandWpf;
using SomUI.Model;
using SomUI.Service;
using NLog;
using System.Runtime.CompilerServices;
using System.Net;
using CommonServiceLocator;
using GalaSoft.MvvmLight.Ioc;
using System.ComponentModel;
using System.Windows.Controls;
using System.IO;
using System.Diagnostics;
using System.Collections.ObjectModel;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Microsoft.Win32;
using System.Text.RegularExpressions;
using System.Windows;
using MahApps.Metro.Controls;
using MahApps.Metro.Controls.Dialogs;
using System.Threading;
using System.Xml;
using System.Linq;
namespace SomUI.ViewModel
{
    /// <summary> 
    /// This class contains properties that the Views can data bind to.
    /// In older versions the software used pyhton script files for process execution, and required the user to install a separate python environment. 
    /// Newer versions instead use PyInstaller to bundle the script along with the python environment into one executable, and so instead of calling scripts newer versions call executables, and do not require the user to install a python environment.
    /// This history lesson might explain some quirks in the code.
    /// The python scripts which the executables are compiled from are located in the scripts folder.
    /// </summary>
    public class SomViewModel : ViewModelBase, INotifyPropertyChanged
    {

        private readonly ILogger logger = NLog.LogManager.GetCurrentClassLogger();
        private readonly IDialogService dialogService;
        public event PropertyChangedEventHandler PropertyChanged;
        private SomModel model;
        public UserControl activeView;
        private bool isBusy;
        private bool isImgFile;
        private bool isGeoTiffFile;
        private bool isCsvFile;
        private bool fileSelected;
        private bool showAdvancedParams;
        protected string _bitMapPath = string.Empty;
        private int selectedColumnIndex;
        private int runningProcessCount;
        private int selectedClusterIndex;
        private bool isSelectedEasting;
        private bool isSelectedNorthing;
        private bool isSelectedLabel;
        private bool showSettingsFlyout;
        private string pythonPath;
        private string pythonLogText;
        private double normalizationMin;
        private double normalizationMax;
        DateTime lastRead = DateTime.MinValue;

        private SomTool SomTool;
        private FileSystemWatcher somPlotWatcher;
        //ViewModelLocator viewModelLocator;
        private string flyOutText;
        private bool statusFlyOutOpen;
        //private int status;//0 and 1, according to whether run was succesful.
        public ObservableCollection<string> MapTypes { get; } = new ObservableCollection<string>() { "toroid", "planar" };
        public ObservableCollection<string> GridShapes { get; } = new ObservableCollection<string>() { "rectangular", "hexagonal" };
        public ObservableCollection<string> Initializations { get; } = new ObservableCollection<string>() { "random", "pca" };
        public ObservableCollection<string> Neighborhoods { get; } = new ObservableCollection<string>() { "gaussian", "bubble" };
        public ObservableCollection<string> TrainingFunctions { get; } = new ObservableCollection<string>() { "linear", "exponential" };
        // Lists of result images
        public ObservableCollection<ImageSource> SomImageList { get; }
        public ObservableCollection<ImageSource> GeoSpaceImageList { get; }
        public ObservableCollection<ImageSource> BoxPlotList { get; }
        public ObservableCollection<ImageSource> ScatterPlotList { get; }
        public ObservableCollection<ImageSource> ClusterPlotList { get; }
        private ImageSource dataHistogram;
        private ObservableCollection<string> columnNames;
        private ObservableCollection<DataColumn> columnData;
        public RelayCommand<string> SelectCsvFileCommand { get; }
        public RelayCommand VisualizeExistingResultsCommand { get; }
        public RelayCommand OpenManualCommand { get; }
        public RelayCommand<ImageSource> OpenPlotCommand { get; }
        public RelayCommand RunClusteringCommand { get; }
        public RelayCommand WriteGeotifCommand { get; }
        public RelayCommand SelectLrnFileCommand { get; }
        public RelayCommand SelectFilesCommand { get; }
        public RelayCommand RunToolCommand { get; }
        public RelayCommand DrawCommand { get; }
        public RelayCommand DrawScatterplotsCommand { get; }
        public RelayCommand ImgListTest { get; }
        public RelayCommand SaveChangesCommand { get; }
        public RelayCommand SelectFolderCommand { get; }
        public RelayCommand LaunchInWebBrowserCommand { get; }
        public RelayCommand SelectGeoTiffFileCommand { get; }
        public RelayCommand SaveClusterCommand { get; }
        public RelayCommand SelectSomCommand { get; }
        public RelayCommand ShowModelDialogIfNoSettingsFile { get; }
        public RelayCommand ForcePythonReinstallCommand { get; }
        public RelayCommand SelectPythonFileCommand { get; }
        public RelayCommand ShowModelDialog { get; }
        public RelayCommand ShowSettingsFlyOutCommand { get; }
        public RelayCommand SelectSomResultFolderCommand { get; }
        public RelayCommand DrawClusterPlotsCommand { get; }
        public RelayCommand SaveClusterFileCommand { get; }
        public RelayCommand LoadClusterFileCommand { get; }
        public RelayCommand SaveFileCommand { get; }
        public RelayCommand<DataColumn> RemoveTifCommand { get; }
        public RelayCommand DrawResultsInteractiveCommand { get; }
        public RelayCommand<string> ShowResultsInFileSystemCommand { get; }

        public RelayCommand<ObservableCollection<BoolStringHelper>> SelectAllCommand { get; }
        public RelayCommand<ObservableCollection<BoolStringHelper>> DeSelectAllCommand { get; }
        public RelayCommand<DataColumn> UnCheckEastingCommand { get; }
        public RelayCommand<DataColumn> UnCheckNorthingCommand { get; }
        public RelayCommand<DataColumn> UnCheckLabelCommand { get; }
        public RelayCommand AddLabelDataCommand { get; }
        public SomViewModel(IDialogService dialogService)
        {
            this.logger = NLog.LogManager.GetCurrentClassLogger();
            logger.Trace("Loading SomViewModel");
            this.dialogService = dialogService;
            SomTool = new SomTool();
            columnNames = new ObservableCollection<string>();
            columnData = new ObservableCollection<DataColumn>();
            SomImageList = new ObservableCollection<ImageSource>();
            GeoSpaceImageList = new ObservableCollection<ImageSource>();
            BoxPlotList = new ObservableCollection<ImageSource>();
            ScatterPlotList = new ObservableCollection<ImageSource>();
            ClusterPlotList = new ObservableCollection<ImageSource>();

            pythonLogText = "";
            isBusy = false;
            isImgFile = false;
            isGeoTiffFile = false;
            isCsvFile = false;
            fileSelected = false;
            runningProcessCount = 0;
            showAdvancedParams = false;
            flyOutText = "";
            isSelectedLabel = false;
            statusFlyOutOpen = false;
            showSettingsFlyout = false;
            selectedColumnIndex = -2;
            this.dialogService = dialogService;
            model = new SomModel
            {
                EastingColumnIndex = 0,
                NorthingColumnIndex = 1,
                LabelColumnIndex = -2,
                InputFile = "Choose Input File",
                SomResultsFolder = "Location of the folder",
                InRasterList = new List<string>(),
                Output_file_geospace = null,
                Output_file_somspace = null,
                Som_y = 10,
                Som_x = 10,
                Epochs = 10,
                WinsorMin = "0",
                WinsorMax = "0",
                IsWinsorized = "False",
                IsLogTransformed = "False",
                IsExcluded = "0",
                KMeans_min = 2,
                KMeans_max = 25,
                KMeans = "true",
                KMeans_min_last_calculation = 2,
                KMeans_max_last_calculation = 0,
                KMeans_initializations = 5,
                Output_Folder = Path.Combine(System.IO.Path.GetTempPath(), "GisSOM"),
                InitialNeighborhood = 0,
                FinalNeighborhood = 1,
                TrainingRateFunction = "linear",
                TrainingRateInitial = 0.1,
                TrainingRateFinal = 0.01,
                InitialCodeBook = "",
                NoDataValue = "",
                IsSpatial = true,
                IsNormalized = true,
                NormalizationMin = 0,
                NormalizationMax = 1,
                InteractiveType = "Cluster",
                DataShape = "grid",
                BoxPlotList = new ObservableCollection<BoolStringHelper> { },
                ScatterPlotList = new ObservableCollection<BoolStringHelper> { },
                ColumnDataList = new ObservableCollection<DataColumn> { },
                RunId = "",
                SelectedInteractiveColumn = 0
            };

            try {
                Directory.CreateDirectory(Path.Combine(Model.Output_Folder, "DataPreparation"));
                Directory.CreateDirectory(Path.Combine(Model.Output_Folder, "DataForOriginalPlots", "DataPreparation"));
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to create Data preparation folder.");
            }

            //Clear parts of temp folder
            System.IO.DirectoryInfo di = new DirectoryInfo(Path.Combine(Model.Output_Folder, "DataPreparation"));
            try
            {
                foreach (FileInfo file in di.GetFiles())
                {
                    file.Delete();
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to clear temp folder.");
            }
            di = new DirectoryInfo(Path.Combine(Model.Output_Folder, "DataForOriginalPlots", "DataPreparation"));
            try
            {
                foreach (FileInfo file in di.GetFiles())
                {
                    file.Delete();
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to clear temp folder.");
            }
            di = new DirectoryInfo(Path.Combine(Model.Output_Folder, "DataPreparation"));

            RunToolCommand = new RelayCommand(RunTool, CanRunTool);
            SelectCsvFileCommand = new RelayCommand<string>((string s) => SelectCsvFile(s));
            SelectLrnFileCommand = new RelayCommand(SelectLrnFile, CanRunTool);
            VisualizeExistingResultsCommand = new RelayCommand(VisualizeExistingResult, CanRunTool);
            OpenManualCommand = new RelayCommand(OpenManual);
            SelectFilesCommand = new RelayCommand(SelectImgFiles, CanRunTool);
            SelectGeoTiffFileCommand = new RelayCommand(SelectGeoTiffFile, CanRunTool);
            DrawCommand = new RelayCommand(EditAndDraw, CanRunTool);
            DrawScatterplotsCommand = new RelayCommand(DrawScatterPlots, CanRunTool);
            SaveChangesCommand = new RelayCommand(SaveChanges, CanRunTool);
            SelectFolderCommand = new RelayCommand(SelectFolder);
            LaunchInWebBrowserCommand = new RelayCommand(LaunchInWebBrowser);
            RunClusteringCommand = new RelayCommand(CalcAndDrawClusters, CanRunTool);
            WriteGeotifCommand = new RelayCommand(WriteGeotif);
            SaveClusterCommand = new RelayCommand(SaveCluster, CanRunTool);
            SelectSomCommand = new RelayCommand(SelectSomFile, CanRunTool);
            SelectPythonFileCommand = new RelayCommand(SelectPythonFile);
            SelectSomResultFolderCommand = new RelayCommand(SelectSomResultFolder, CanRunTool);
            DrawClusterPlotsCommand = new RelayCommand(DrawClusterPlots, CanRunTool);
            OpenPlotCommand = new RelayCommand<ImageSource>(OpenPlotExternally);
            SaveFileCommand = new RelayCommand(SaveFile);
            SaveClusterFileCommand = new RelayCommand(SaveClusterFile);
            LoadClusterFileCommand = new RelayCommand(LoadClusterFile);
            ShowResultsInFileSystemCommand = new RelayCommand<string>((string s)=>ShowResultsInFileSystem(s));
            RemoveTifCommand = new RelayCommand<DataColumn>((DataColumn d) => RemoveTifFromInput(d));
            ShowModelDialog = new RelayCommand(OpenModelDialog);
            ShowSettingsFlyOutCommand = new RelayCommand(ShowSettingsFlyOutMethod, CanRunTool);
            SelectAllCommand = new RelayCommand<ObservableCollection<BoolStringHelper>>((ObservableCollection<BoolStringHelper> collection) => SelectAll(collection));
            DeSelectAllCommand = new RelayCommand<ObservableCollection<BoolStringHelper>>((ObservableCollection<BoolStringHelper> collection) => DeSelectAll(collection));
            UnCheckEastingCommand = new RelayCommand<DataColumn>((DataColumn d) => UnCheckEasting(d));
            UnCheckNorthingCommand = new RelayCommand<DataColumn>((DataColumn d) => UnCheckNorthing(d));
            UnCheckLabelCommand = new RelayCommand<DataColumn>((DataColumn d) => UnCheckLabel(d));
            AddLabelDataCommand = new RelayCommand(AddDataLabelColumn);
            DrawResultsInteractiveCommand = new RelayCommand(DrawResultsInteractive);
            if (File.Exists(Path.Combine(Model.Output_Folder, "settingsFile.txt")))
            {
                pythonPath = File.ReadAllText(Path.Combine(Model.Output_Folder, "settingsFile.txt"));
            }
        }

        /// <summary>
        /// Function to split the input .lrn file to individual columns that are used by the EditColumn function and python script. 
        /// Columns are saved as 2D numpy arrays of float-32. 
        /// The beginning of the column contains information on the column (col name atleast) and data preparation procedures: 
        /// wheter the column was winsorized(and winsor min max values), if column was log transformed or not, is column excluded or not
        /// </summary>
        private async void SplitToColumns()
        {
            try 
            { 
            RunningProcessCount++;
            await Task.Run(async () =>
            {
                Task t = SomTool.SplitLrnFile(Model, ScriptOutputForSplitToColumns, ScriptError);
                await t;
                RunningProcessCount--;
            });
            }
            catch (Exception ex)
            {
                logger.Error("Failed to read data");
                PythonLogText += "Failed to read data";
                App.Current.Dispatcher.Invoke((Action)delegate         //delegate to access different thread
                {
                    dialogService.ShowNotification("Failed to read data.", "Error");
                });
                RunningProcessCount--;
            }
        }

        /// <summary>
        /// Draw histogram of the data column selected in the GUI data preparation stage.
        /// </summary>
        private async void DrawHistogram()
        {
            try {
                RunningProcessCount++;
                DataHistogram = await SomTool.DrawHistogram(Model, SelectedColumnIndex, IsSelectedNorthing, IsSelectedEasting);
                RunningProcessCount--;
                if (DataHistogram == null && SelectedColumnIndex != -1)
                {
                    logger.Error("Failed to draw dataistogram");
                    App.Current.Dispatcher.Invoke((Action)delegate         //delegate to access different thread
                    {
                        dialogService.ShowNotification("Failed to draw histogram.", "Error");
                    });

                }
            }
            catch (Exception ex)
            {
                logger.Error("Failed to draw dataistogram");
                PythonLogText += "Failed to draw dataistogram";
                App.Current.Dispatcher.Invoke((Action)delegate         //delegate to access different thread
                {
                    dialogService.ShowNotification("Failed to draw histogram.", "Error");
                });
            }
        }

        /// <summary>
        /// Function to edit data columns in the preparation stage: applying log transform, winsoring, excluding a column, selecting x and y columns.
        /// Proper column is loaded according to SelectedColumnIndex parameter, and the respective data operations are passed on as parameters (User selects these in the UI and they are bound to Model).
        /// </summary>
        private void EditColumn()
        {
            SomTool.EditColumn(Model, SelectedColumnIndex, IsSelectedNorthing, IsSelectedEasting, IsSelectedLabel, ScriptOutput, ScriptError);
        }

        /// <summary>
        /// Function to save the changes made in data preparation stage to the data file. Saves the data as EditedData.lrn
        /// </summary>
        private async void SaveChanges()
        {
            if (Model.IsSpatial && ((Model.ColumnDataList.All(x => x.IsEasting == false)) || (Model.ColumnDataList.All(x => x.IsNorthing == false))))
            {//if data is set as spatial data, and no x or y column has been selected
                dialogService.ShowNotification("Please select X and Y columns or set the dataset to non-spatial data before proceeding.", "Error");
            }
            else { 
                RunningProcessCount++;
            
                if (Model.ColumnDataList.All(x => x.IsLabel == false))
                {
                    Model.LabelColumnIndex = -2;
                }

                PythonLogText = "";
                ServiceLocator.SetLocatorProvider(() => SimpleIoc.Default);
                EditColumn();
                SomTool.SaveChanges(Model, SelectedColumnIndex, IsSelectedNorthing, IsSelectedEasting, IsSelectedLabel, ScriptOutput, ScriptError);
                ServiceLocator.SetLocatorProvider(() => SimpleIoc.Default);
                var main = ServiceLocator.Current.GetInstance<MainViewModel>();
                main.ChangeToSomParameterView();
                RunningProcessCount--;
            }
        }

        /// <summary>
        /// Run nextsom_wrap python script
        /// </summary>
        private async void RunTool()
        {
            Model.InteractiveResultColumnList.Clear();
            Model.InteractiveResultColumnList.Add("Cluster");
            for (int i = 0; i < Model.ColumnDataList.Count(); i++)
            {
                if (Model.ColumnDataList[i].IsExcluded.ToString() != "True")
                {
                    Model.InteractiveResultColumnList.Add(Model.ColumnDataList[i].Name);
                }
            }

            RunningProcessCount++;
            PythonLogText = "";
            ServiceLocator.SetLocatorProvider(() => SimpleIoc.Default);
            var time = DateTime.Now.ToString("yyyyMMddHHmmss");
            time = time.Replace(".", "").Replace(" ", "_");
            if (Model.RunId == "")
            {
                Model.OutputFolderTimestamped = Path.Combine(Model.Output_Folder, "Out_" + time + "_" + Model.Som_x + "x" + Model.Som_y + "_" + Model.GridShape);
            }
            else
            {
                Model.OutputFolderTimestamped = Path.Combine(Model.Output_Folder, "Out_" + Model.RunId);
            }


            CreateFolderStructure(Model.OutputFolderTimestamped);
            RegisterFolderWatcher(Model.OutputFolderTimestamped);

            try
            {


                DirectoryInfo di = new DirectoryInfo(Path.Combine(Model.Output_Folder, "DataPreparation"));
                /*
                foreach (FileInfo f in di.GetFiles())
                {
                    if (f.Name.Contains("label"))
                        f.CopyTo(Path.Combine(Model.OutputFolderTimestamped, "DataPreparation", f.Name), true);

                }
                di = new DirectoryInfo(Path.Combine(Model.Output_Folder,"DataForOriginalPlots", "DataPreparation"));
                foreach (FileInfo f in di.GetFiles())
                {ScatterPlotList
                    if (!f.Name.ToLower().Contains("edited") && !f.Name.ToLower().Contains("label"))
                        f.CopyTo(Path.Combine(Model.OutputFolderTimestamped,"DataForOriginalPlots", "DataPreparation", f.Name), true);
                }
                */
                if (File.Exists(Path.Combine(Model.Output_Folder, "DataStats.xml")))
                {
                    FileInfo fi = new FileInfo(Path.Combine(Model.Output_Folder, "DataStats.xml"));
                    fi.CopyTo(Path.Combine(Model.OutputFolderTimestamped, "DataStats.xml"), true);
                }

                /*
                foreach (FileInfo f in di.GetFiles())
                {
                    f.CopyTo(Path.Combine(Model.OutputFolderTimestamped, "DataForOriginalPlots", "DataPreparation", f.Name), true);
                }
                */

                await Task.Run(async () =>
                {
                    Task t = SomTool.RunTool(Model, SomImageList, GeoSpaceImageList, BoxPlotList, ScatterPlotList, ClusterPlotList, ScriptOutput, ScriptError);
                    await t;
                    App.Current.Dispatcher.Invoke((Action)delegate         //delegate to access different thread
                    {
                        dialogService.ShowNotification("SOM run complete.", "Success");
                    });

                });
                Model.ScatterPlotList.Clear();
                string line1 = File.ReadLines(Path.Combine(Model.OutputFolderTimestamped, "result_som.txt")).First();
                var headerArray = line1.Split(' ');
                for (int i = 2; i < headerArray.Count() - 3; i++)
                {
                    Model.ScatterPlotList.Add(new BoolStringHelper(headerArray[i], true));
                }


            }
            catch (Exception ex)
            {
                dialogService.ShowNotification("Failed to complete SOM run.", "Error");
            }
            DrawResults("true");
            if (Model.KMeans != "False")
            {
                DrawClusters();
                SelectedClusterIndex = Model.KMeans_min;
            }
            //if (Model.Output_file_geospace.Length > 0)
            DrawResultsInteractive();
            ClusterPlotList.Clear();
            RunningProcessCount--;


        }

        /// <summary>
        /// Run python script for drawing result plots of som calculation.
        /// </summary>
        private async void DrawResults(string redraw)
        {
            //string GeoPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Geo");
            //string SomPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Som");
            //string BoxPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Boxplot");
            //string ScatterPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Scatterplot");
            await Task.Run(async () =>
            {
                RunningProcessCount++;
                Task t = SomTool.DrawResults(redraw, Model, SomImageList, GeoSpaceImageList, BoxPlotList, ScatterPlotList, ScriptOutputForPlots, ScriptError);
                await t;
                RunningProcessCount--;
                
            });

        }
        private async void DrawResultsInteractive()
        {

            await Task.Run(async () =>
            {
                //BrowserToolTip = "";
                RunningProcessCount++;
                ServiceLocator.SetLocatorProvider(() => SimpleIoc.Default);
                Task t = SomTool.DrawResultsInteractive(Model, ScriptOutput, ScriptError);
                await t;
                RunningProcessCount--;
            });
            BrowserToolTip = "";

        }

        /// <summary>
        /// Run new round of clustering on somoclu result data
        /// </summary>
        private async void RunClustering()
        {

            await Task.Run(async () =>
            {
                RunningProcessCount++;
                Task t = SomTool.RunClustering(Model, ClusterPlotList, ScriptOutput, ScriptError);
                await t;

                DrawClusters();
                SelectedClusterIndex = Model.KMeans_min;//Model.KMeans_min;
                RunningProcessCount--;
            });
        }
        private async void WriteGeotif()
        {
            await Task.Run(async () =>
            {
                RunningProcessCount++;
                Task t = SomTool.WriteGeotif(Model, ScriptOutput, ScriptError);
                await t;

                DrawClusters();
                RunningProcessCount--;
            });

        }

        /// <summary>
        /// Draw plots of 3 best clustering results
        /// </summary>
        private async void DrawClusters()
        {
            RunningProcessCount++;
            SomTool.DrawClusters(Model, ClusterPlotList, ScriptOutput, ScriptError);
            RunningProcessCount--;
        }
        private async void DrawScatterPlots()
        {

            await Task.Run(async () =>
            {
                ClearFolder(Path.Combine(Model.OutputFolderTimestamped, "Scatterplot"));
                App.Current.Dispatcher.Invoke((Action)delegate
                {
                    ScatterPlotList.Clear();
                });

                RunningProcessCount++;
                Task t = SomTool.DrawScatterPlots(Model, ScriptOutputForPlots, ScriptError);
                await t;

                //DrawClusters();  
                RunningProcessCount--;
            });

        }
        /// <summary>
        /// Save selected clustering result to som calculation result txt files.
        /// </summary>
        private async void SaveCluster()
        {

            await Task.Run(async () =>
            {
                RunningProcessCount++;
                Task t = SomTool.SaveCluster(Model, SelectedClusterIndex, SomImageList, GeoSpaceImageList, BoxPlotList, ScatterPlotList, ScriptOutput, ScriptError);
                await t;

                DrawResults("false");
                DrawResultsInteractive();
                RunningProcessCount--;
            });
        }
        /// <summary>
        /// Function to draw selected cluster
        /// </summary>
        private async void RunDashDraw()
        {
            RunningProcessCount++;
            SomTool.RunDashDraw(Model, ScriptOutput, ScriptError);
            RunningProcessCount--;
        }

        #region Loading files and folders
        /// <summary>
        /// Load som.dictionary file (at least for using as existing codebook, any other functionality?)
        /// </summary>
        private void SelectSomFile()
        {
            try
            {
                string somFile = dialogService.OpenFileDialog("", "dictionary files|*.dictionary;", true, true);
                {
                    Model.InitialCodeBook = somFile;         //need an option to unselect som file? yes you do. or at least deselect the option for codebook.         
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to show OpenFileDialog");
            }

        }
        /// <summary>
        /// Function to load CSV files as input data. 
        /// </summary>
        /// 
        private void SelectCsvFile(string dataShape)
        {
            try
            {
                PythonLogText = "";
                string inputFile = dialogService.OpenFileDialog("", "CSV files|*.csv;", true, true);
                if (inputFile != null) {
                    Model.DataShape = dataShape;
                    Model.LabelColumnIndex = -2;
                    Model.EastingColumnIndex = 0;
                    Model.NorthingColumnIndex = 1;
                    IsSelectedEasting = false;
                    IsSelectedNorthing = false;
                    IsSelectedLabel = false;
                    Model.ColumnDataList.Clear();
                    model.InputFile = inputFile;
                    model.InputFile = inputFile.Replace("\\", "/");
                    model.InRasterList = new List<string> { inputFile };
                    FileSelected = true;
                    ClearFolder(Path.Combine(Model.Output_Folder, "DataPreparation"));
                    ReadCsvColumnNames();
                    ClearFolder(Path.Combine(Model.Output_Folder, "DataPreparation"));
                    SplitToColumns();
                    IsGeoTiffFile = false;
                    IsCsvFile = true;
                    RaisePropertyChanged("IsGeoTiffFile");
                }
                

            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to show OpenFileDialog");
            }
        }
        /// <summary>
        /// Function to load .lrn files as input.
        /// </summary>
        private void SelectLrnFile()
        {
            try
            {
                string inputFile = dialogService.OpenFileDialog("", "*.lrn | *.lrn;", true, true);
                logger.Trace("SelectLrnFile inputfile: {} ", inputFile);
                if (!string.IsNullOrEmpty(inputFile))
                {
                    Model.LabelColumnIndex = -2;
                    Model.EastingColumnIndex = 0;
                    Model.NorthingColumnIndex = 1;
                    IsSelectedEasting = false;
                    IsSelectedNorthing = false;
                    IsSelectedLabel = false;
                    model.InputFile = inputFile;
                    model.InputFile = inputFile.Replace("\\", "/");
                    model.InRasterList = new List<string> { inputFile };
                    FileSelected = true;
                    ClearFolder(Path.Combine(Model.Output_Folder, "DataPreparation"));
                    ReadColumnNames();
                    SplitToColumns();
                    IsGeoTiffFile = false;
                    IsCsvFile = false;
                    Model.IsSpatial = true;
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to show OpenFileDialog");
            }
        }
        /// <summary>
        /// Function to show dialog for choosing a folder, used to select custom output folder. Uses SelectFolderDialog defined in DialogService class to display file browser. 
        /// </summary>
        private void SelectFolder()
        {
            var oldFolder = Model.Output_Folder;
            try
            {
                string outputFolder = dialogService.SelectFolderDialog("c:\\", Environment.SpecialFolder.MyComputer);//Tähän C:\\ tilalle se DefaultFolder? ja sit se asetetaan kans aina. vai pitääkö tää ehkä tehdä dialogservicen puolella?
                if (!string.IsNullOrEmpty(outputFolder))
                {
                    Model.Output_Folder = Path.Combine(outputFolder, "GisSOM");
                    CreateFolderStructure(Model.Output_Folder);//Create folder structure for new output folder
                    var oldFolderPath = Path.Combine(oldFolder, "DataForOriginalPlots", "DataPreparation");
                    DirectoryInfo di = new DirectoryInfo(oldFolderPath);

                    if (Directory.Exists(oldFolderPath))
                    {
                        foreach (FileInfo f in di.GetFiles())
                        {
                            f.CopyTo(Path.Combine(Model.Output_Folder, "DataForOriginalPlots", "DataPreparation", f.Name), true);
                        }
                    }
                    var oldFolderPath_original = Path.Combine(oldFolder, "DataPreparation");
                    DirectoryInfo di_original = new DirectoryInfo(oldFolderPath_original);
                    if (Directory.Exists(oldFolderPath_original))
                    {
                        foreach (FileInfo f in di_original.GetFiles())
                        {
                            f.CopyTo(Path.Combine(Model.Output_Folder, "DataPreparation", f.Name), true);
                        }
                    }
                    string filePath = Path.Combine(oldFolder, "DataStats.xml");
                    if (File.Exists(filePath))
                    {
                        FileInfo fi = new FileInfo(filePath);
                        fi.CopyTo(Path.Combine(Model.Output_Folder, "DataStats.xml"), true);
                    }

                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to show FolderBrowserDialog");
                Model.Output_Folder = oldFolder;
            }
        }
        /// <summary>
        /// A method to select multiple .IMG files. Currently unused and unfinished.
        /// </summary>
        private void SelectImgFiles()
        {
            try
            {
                List<string> files = dialogService.OpenFilesDialog("", ".img|*.img;", true, true);
                if (!string.IsNullOrEmpty(files.ToString()))
                {
                    model.InRasterList = files;
                    IsImgFile = true;
                    FileSelected = true;
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to show OpenFileDialog");
            }
        }
        /// <summary>
        /// Method to open dialog for selecting a .tif file.
        /// </summary>
        private void SelectGeoTiffFile()
        {
            try
            {
                PythonLogText = "";
                Model.DataShape = "grid";
                List<string> inputFiles = dialogService.OpenFilesDialog("", "*.tif | *.tif;", true, true);
                if (inputFiles != null)
                {
                    if (inputFiles.Count > 0)
                    {
                        if (IsGeoTiffFile == false)
                        { //clear ColumnNames list if geotiff file was not previously selected (no lrn files creeping in to this list
                            Model.LabelColumnIndex = -2;
                            Model.EastingColumnIndex = 0;
                            Model.NorthingColumnIndex = 1;
                            IsSelectedEasting = false;
                            IsSelectedNorthing = false;
                            IsSelectedLabel = false;
                            ColumnNames.Clear();
                            Model.InRasterList.Clear();
                            Model.ColumnDataList.Clear();
                            Model.ColumnDataList.Add(new DataColumn("x", true, false, false, false, 0, 1, false, false, 0, 1));
                            Model.ColumnDataList.Add(new DataColumn("y", false, true, false, false, 0, 1, false, false, 0, 1));
                            ClearFolder(Path.Combine(Model.Output_Folder, "DataPreparation"));
                        }
                        IsGeoTiffFile = true;
                        IsCsvFile = false;
                        RaisePropertyChanged("IsGeoTiffFile");
                        Model.IsSpatial = true;
                        Model.InputFile = null;
                        foreach (string inputFile in inputFiles)
                        {
                            Model.InRasterList.Add(inputFile.Replace("\\", "/"));
                        }
                        foreach (string s in Model.InRasterList)
                        {
                            Model.InputFile += Model.InputFile == null ? s : "," + s;
                        }
                        FileSelected = true;

                        ReadGeoTiffColumnNames();
                        if (Model.InRasterList.Count > 1)
                        {
                            SplitToColumns();

                        }
                        else
                            ClearFolder(Path.Combine(Model.Output_Folder, "DataPreparation"));
                    }
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to show OpenFileDialog");
            }
        }

        private async void AddDataLabelColumn()
        {
            string inputFile = dialogService.OpenFileDialog("", "CSV files|*.csv;", true, true);
            if (!string.IsNullOrEmpty(inputFile))
            {
                try
                {
                    RunningProcessCount++;
                    Model.NewLabelData = inputFile;
                    await Task.Run(async () =>
                    {
                        Task t = SomTool.NewLabelData(Model, ScriptOutput, ScriptError);
                        await t;
                        RunningProcessCount--;
                    //SomImageList.Add(Model.NewLabelPlot);
                    //SomImageList.Add(Model.NewLabelLegend);
                    App.Current.Dispatcher.Invoke((Action)delegate
                        {
                            SomImageList.Clear();
                            AddToImageCollection(SomImageList, Path.Combine(Model.OutputFolderTimestamped, "Som"));
                        });

                    });
                }
                catch (Exception ex)
                {

                    logger.Error(ex, "Error in reading adding new label data");
                    dialogService.ShowNotification("Error in reading adding new label data", "Error");
                }
                //Do something with Model.newlabelplot and model.newlabelLegend. or not. just set them in the tool?
            }
        }

        private void RemoveTifFromInput(DataColumn d)//string s)
        {
            string s = d.Name;
            try
            {
                if (s != "x" && s != "y")
                {

                    var dataPrepFolder = Path.Combine(Model.Output_Folder, "DataPreparation");
                    DirectoryInfo di = new DirectoryInfo(dataPrepFolder);

                    string oldFileName;
                    bool move = false;
                    for (int i = 0; i < ColumnNames.Count(); i++)
                    {
                        if (ColumnNames[i] == s)
                        {
                            move = true;
                            if(i== ColumnNames.Count() - 1)
                            {
                                //last column, delete now.
                                File.Delete(Path.Combine(dataPrepFolder, "outfile" + i + ".npy"));
                            }
                            Model.ColumnDataList.Remove(d);
                        }
                        else if (move == true)
                        {
                            FileInfo[] fi = di.GetFiles();

                            foreach (FileInfo f in di.GetFiles())
                            {
                                oldFileName = f.Name;
                                var fileNumber = oldFileName.Substring(7, 1);
                                if (Int32.Parse(fileNumber) >= i)
                                {
                                    var newFileName = f.Name.Replace(fileNumber.ToString(), (Int32.Parse(fileNumber) - 1).ToString());
                                    MoveWithReplace(Path.Combine(dataPrepFolder, oldFileName), Path.Combine(dataPrepFolder, newFileName));
                                }
                            }
                            break;
                        }
                    }



                    for (int i = 0; i < Model.InRasterList.Count; i++)
                    {
                        string fileName = Model.InRasterList[i].Substring((Model.InRasterList[i].Length - s.Length));
                        if (fileName == s)
                        {//if name matches, remove from input tif lists 
                            Model.InRasterList.Remove(Model.InRasterList[i]);
                            ColumnNames.Remove(s);
                        }
                    }
                    Model.InputFile = null;
                    foreach (string str in Model.InRasterList)
                    {
                        Model.InputFile += Model.InputFile == null ? str : "," + str;
                    }
                }
                else { throw new Exception("Can't remove x or y column."); }
                SelectedColumnIndex = 2;
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to remove input column");
            }
        }

        /// <summary>
        /// Select python exe path manually
        /// </summary>
        public void SelectPythonFile()
        {

            try
            {
                string exeFile = dialogService.OpenFileDialog("", "EXE files|*.exe;", true, true);
                if (!string.IsNullOrEmpty(exeFile))
                {
                    PythonPath = exeFile;
                    OpenModelDialog();
                    try
                    {
                        System.IO.File.WriteAllText(Path.Combine(Model.Output_Folder, "settingsFile.txt"), pythonPath);                     
                    }
                    catch (Exception ex)
                    {
                        logger.Error("Could not write settings to file: " + ex);
                        ShowErrorFlyout("Could not write settings to file.");
                    }
                    try
                    {
                        var metroWindow = (Application.Current.MainWindow as MetroWindow);
                        var dialog = metroWindow.GetCurrentDialogAsync<BaseMetroDialog>();
                        metroWindow.HideMetroDialogAsync(dialog.Result);
                    }
                    catch (Exception)
                    {

                    }
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to show OpenFileDialog");
            }
        }
#endregion


#region Functions to read column names
        /// <summary>
        /// Function to read column names from .lrn data file.
        /// </summary>
        private void ReadColumnNames()
        {
            try
            {
                System.IO.StreamReader file = new System.IO.StreamReader(Model.InputFile);
                string line = null;

                while (true)
                {
                    line = file.ReadLine();
                    System.Console.WriteLine(line);
                    if (!(line.StartsWith("#") || line.StartsWith("%")))
                    {
                        break;
                    }
                }
                file.Close();
                System.Console.ReadLine();
                string[] words = line.Split(' ');
                if (words.Length < 2)
                    words = line.Split('\t'); 
                ColumnNames.Clear();
                for (int i = 1; i < words.Length; i++)
                {
                    ColumnNames.Add(words[i]);
                    Model.ColumnDataList.Add(new DataColumn (words[i], false, false, false,false,0,1, false, false, 0, 1));
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Input file not found or malformed.");
            }
        }
        /// <summary>
        /// Method to add geotif column names to list in data preparation view.
        /// </summary>
        private void ReadGeoTiffColumnNames()
        {
            ColumnNames.Clear();
            ColumnNames.Add("x");
            ColumnNames.Add("y");
            Model.ColumnDataList.Clear();
            Model.ColumnDataList.Add(new DataColumn("x", true, false, false, false, 0, 1, false, false, 0, 1));
            Model.ColumnDataList.Add(new DataColumn("y", false, true, false, false, 0, 1, false, false, 0, 1));
            foreach (string s in Model.InRasterList)
            {
                ColumnNames.Add(Path.GetFileName(s));
                Model.ColumnDataList.Add(new DataColumn(Path.GetFileName(s), false, false, false, false, 0, 1, false, false, 0, 1));
            }
        }
        /// <summary>
        /// Method to add csv column names to list in data preparation view.
        /// </summary>
        private void ReadCsvColumnNames()
        {
            try
            {
                System.IO.StreamReader file = new System.IO.StreamReader(Model.InputFile);
                string line = file.ReadLine();
                string[] words = line.Split(',');
                ColumnNames.Clear();
                for (int i = 0; i < words.Length; i++)
                {
                    ColumnNames.Add(words[i]);
                    Model.ColumnDataList.Add(new DataColumn(words[i], false, false, false, false, 0, 1, false, false, 0, 1));
                }
            }
            catch (Exception ex) 
            {
                logger.Error(ex, "Error in reading input file"); 
                if (ex.Message.Contains("another process"))
                    dialogService.ShowNotification("The file is being used in another process. Please close it and try again.", "Error");
                else
                    dialogService.ShowNotification("Error in reading input file", "Error");
            }
        }
#endregion

        

        private void CreateFolderStructure(string root)
        {         
            try
            {
                Directory.CreateDirectory(Path.Combine(root, "Interactive"));
                Directory.CreateDirectory(Path.Combine(root, "DataPreparation"));
                Directory.CreateDirectory(Path.Combine(root, "DataForOriginalPlots", "DataPreparation"));
                Directory.CreateDirectory(Path.Combine(root, "Clustering"));
                Directory.CreateDirectory(root + "/Som");
                Directory.CreateDirectory(root + "/Geo");
                Directory.CreateDirectory(Path.Combine(root, "BoxPlot"));
                Directory.CreateDirectory(Path.Combine(root, "ScatterPlot"));
                Directory.CreateDirectory(Path.Combine(root, "GeoTIFF"));
            }
            catch (Exception ex)
            {
                logger.Error("Error creating folder structure: " + ex);
                FlyOutText = "Could not create project folder";
                StatusFlyOutOpen = true;
            }
        }


        /// <summary>
        /// Open dialog for python package installation. Not used anymore.
        /// </summary>
        public void OpenModelDialog()
        {   
            ServiceLocator.SetLocatorProvider(() => SimpleIoc.Default);
            var mainViewModel = ServiceLocator.Current.GetInstance<MainViewModel>();
            mainViewModel.DialogContentSource = "SomViewModel";
            dialogService.ShowMessageDialog();
        }

        public void OnSomPlotChanged(object source, FileSystemEventArgs e)
        {
            DateTime lastWriteTime = File.GetLastWriteTime(e.FullPath);          
            if (lastWriteTime.ToString() != lastRead.ToString())
            {

            if (Model.KMeans != "False"&&Model.IsSpatial==true) { 
                try
                {
                    RunDashDraw();
                    var imageSource = BitmapFromUri(new Uri(Path.Combine(Model.OutputFolderTimestamped, "somplot_interactive.png")));
                    Model.InteractiveResultSomPlot = imageSource;
                    RaisePropertyChanged("Model.InteractiveResultSomPlot");
                }
                catch (Exception ex)
                {
                    ShowErrorFlyout("Could not create bitmap: ", ex.Message);
                }
                    lastRead = lastWriteTime;
                }
            }
        }


        /// <summary>
        /// For file watcher
        /// </summary>
        /// <param name="source"></param>
        /// <param name="e"></param>
        public static void OnChanged(object source, System.EventArgs e)
        {
            Console.WriteLine("File changed");
        }
        /// <summary>
        ///  For file watcher
        /// </summary>
        /// <param name="source"></param>
        /// <param name="e"></param>
        public static void OnRenamed(object source, System.EventArgs e)
        {
            Console.WriteLine("File Renamed");
        }

        /// <summary>
        /// Open interactive plot in web browser.
        /// </summary>
        public void LaunchInWebBrowser()
        {
            try
            {
                System.Diagnostics.Process.Start("http://localhost:8050/");
            }
            catch (Exception ex)
            {

                logger.Error(" Failed to open in external browser."+ex); 
            }
        }


        private void VisualizeExistingResult()
        {
            
            try
            {
                string outputFolder = dialogService.SelectFolderDialog("c:\\", Environment.SpecialFolder.MyComputer);
                if (!string.IsNullOrEmpty(outputFolder))
                {
                    Model.OutputFolderTimestamped = outputFolder;                
                    XmlDocument doc = new XmlDocument();
                    doc.Load(Path.Combine(Model.OutputFolderTimestamped, "RunStats.xml"));
                    XmlNode node = doc.DocumentElement.SelectSingleNode("dataShape");
                    string dataShape = node.InnerText;
                    node = doc.DocumentElement.SelectSingleNode("kmeans_min");
                    string kmeansMin = node.InnerText;
                    node = doc.DocumentElement.SelectSingleNode("kmeans_max");
                    string kmeansMax = node.InnerText;
                    node = doc.DocumentElement.SelectSingleNode("som_x");
                    string som_x = node.InnerText;
                    node = doc.DocumentElement.SelectSingleNode("som_y");
                    string som_y = node.InnerText;

                    node = doc.DocumentElement.SelectSingleNode("isSacled");
                    string normalized = "False";                 
                    if (node != null)
                    {
                        normalized= node.InnerText;
                    }

                    node = doc.DocumentElement.SelectSingleNode("gridtype");
                    Model.GridShape = node.InnerText;

                    node = doc.DocumentElement.SelectSingleNode("spatial");
                    Model.IsSpatial = bool.Parse(node.InnerText);



                    Model.DataShape = dataShape;
                    Model.KMeans_min = Int32.Parse(kmeansMin);
                    Model.KMeans_min_last_calculation= Int32.Parse(kmeansMin);
                    Model.KMeans_max = Int32.Parse(kmeansMax);
                    Model.IsNormalized = bool.Parse(normalized);
                    Model.Som_x = Int32.Parse(som_x);
                    Model.Som_y = Int32.Parse(som_y);

                    Model.ScatterPlotList.Clear();
                    string line1 = File.ReadLines(Path.Combine(Model.OutputFolderTimestamped, "result_som.txt")).First();
                    var headerArray = line1.Split(' ');
                    for (int i = 2; i < headerArray.Count() - 3; i++)
                    {
                        Model.ScatterPlotList.Add(new BoolStringHelper(headerArray[i], true));
                    }


                    Model.InputFile = Path.Combine(Model.OutputFolderTimestamped, "InputData.lrn");

                    ReadColumnNames();
                    Model.ColumnDataList[0].IsEasting = true;
                    Model.ColumnDataList[1].IsNorthing = true;
                    System.IO.StreamReader file = new System.IO.StreamReader(Model.InputFile);
                    file.ReadLine();
                    file.ReadLine();
                    var colTypes= file.ReadLine();
                    colTypes = colTypes.Substring(3);
                    colTypes = colTypes.Replace("\t", " ");

                    var colTypes2 = colTypes.Split(' ');
                    //line1 = File.ReadLines(Path.Combine(Model.OutputFolderTimestamped, "result_som.txt")).First();

                    Model.InteractiveResultColumnList.Clear();
                    Model.InteractiveResultColumnList.Add("Cluster");
                    for (int i = 0; i < Model.ColumnDataList.Count(); i++)
                    {
                        Model.ColumnDataList[i].IsExcluded= colTypes2[i]=="0" ? true : false;
                        
                        if (Model.ColumnDataList[i].IsExcluded.ToString() != "True")
                        {
                            Model.InteractiveResultColumnList.Add(Model.ColumnDataList[i].Name);
                        }
                    }
                    RegisterFolderWatcher(Model.OutputFolderTimestamped);
                    //doc = new XmlDocument();
                    //doc.Load(Path.Combine(Model.OutputFolderTimestamped, "DataStats.xml"));
                    //XmlNode node = doc.DocumentElement.SelectSingleNode("dataShape");
                    //string dataShape = node.InnerText;
                    //node = doc.DocumentElement.SelectSingleNode("kmeans_min");
                    //string kmeansMin = node.InnerText;
                    //node = doc.DocumentElement.SelectSingleNode("kmeans_max");
                    //string kmeansMax = node.InnerText;




                    Model.Output_file_geospace= Path.Combine(Model.OutputFolderTimestamped, "result_geo.txt");
                    Model.Output_file_somspace= Path.Combine(Model.OutputFolderTimestamped, "result_som.txt");
                    Model.ClusterFilePath = Path.Combine(Model.OutputFolderTimestamped, "cluster.dictionary");
                
                    Model.InputFile = Path.Combine(Model.OutputFolderTimestamped, "InputData.lrn");

                    //the clusters tab is not fully functional with this yet. the min and max cluster numbers are not loaded. Implement this, after RunStats.txt file has been changed. This needs some parsing. maybe change the file to json or xml, something that is easier to read. ---- cluster tab should be functional now.
                    string GeoPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Geo");
                    string SomPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Som");
                    string BoxPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Boxplot");
                    string ScatterPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Scatterplot");


                    AddToImageCollection(SomImageList, SomPlotDirectory);
                    AddToImageCollection(GeoSpaceImageList, GeoPlotDirectory);
                    AddToImageCollection(BoxPlotList, BoxPlotDirectory);
                    AddToImageCollection(ScatterPlotList, ScatterPlotDirectory);

                    var main = ServiceLocator.Current.GetInstance<MainViewModel>();
                    main.ChangeToSomResultView();
                    //SomTool.DrawResultsInteractive(Model, ScriptOutput, ScriptError);
                    DrawResultsInteractive();
                    SomTool.DrawClusters(Model, ClusterPlotList, ScriptOutput, ScriptError);
                    SelectedClusterIndex = Model.KMeans_min;
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to load old results");
                dialogService.ShowNotification("Failed to complete SOM run.", "Error");
            }
        }


        /// <summary>
        /// Stub function to Edit Column and draw histogram, in that order. Should be expanded or removed?
        /// </summary>
        public void EditAndDraw()
        {
            EditColumn();
            DrawHistogram();
        }

        /// <summary>
        /// Select and get images of a folder containing Som results.
        /// </summary>
        private void SelectSomResultFolder()
        {
            try
            {
                Model.SomResultsFolder = dialogService.SelectFolderDialog("c:\\", Environment.SpecialFolder.MyComputer);
            }
            catch(Exception ex)
            {
                logger.Error(ex, "Failed to show FolderBrowserDialog");
                dialogService.ShowNotification("Failed to open dialog.", "Error");
            }
        }

        private void DrawClusterPlots()
        {
            if (Directory.Exists(Model.SomResultsFolder))
            {
                SomTool.DrawClusterPlots(Model.SomResultsFolder, SomImageList);
            }
            else
            {
                dialogService.ShowNotification("Failed read the folder.", "Error");
            }
        }

        /// <summary>
        /// Function to return boolean for telling if the program is busy or not
        /// </summary>
        /// <returns> Boolean representing whether program is busy or not</returns>
        private bool CanRunTool()
        {
            return !IsBusy;
        }

        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
        public void ShowSettingsFlyOutMethod()
        {
            ShowSettingsFlyOut = true;
        }
        private async void CalcAndDrawClusters()
        {
            RunClustering();                      
            RaisePropertyChanged("ClusterPlotList");
        }
        void Display(string output)
        {
            PythonLogText += output + "\r\n"; 
        }

        private void ShowErrorFlyout(string msg)
        {
            if (msg.ToLower().Contains("error"))
            {
                if (StatusFlyOutOpen == false)
                {
                    FlyOutText = msg;
                    StatusFlyOutOpen = true;
                }
            }
        }
        private void ShowErrorFlyout(string msg, string errors)
        {
            if (!String.IsNullOrEmpty(errors))
                Display(errors);
            logger.Error(errors);
            if (msg.ToLower().Contains("error"))
            {
                if (StatusFlyOutOpen == false)
                {
                    FlyOutText = msg;
                    StatusFlyOutOpen = true;
                }
            }
        }
        private void ShowErrorFlyoutAlways(string msg)
        {
            if (StatusFlyOutOpen == false)
            {
                FlyOutText = msg;
                StatusFlyOutOpen = true;
            }
        }
        /// <summary>
        /// Method to create simple http post command, used to send shutdown message to interactive plot 
        /// </summary>
        /// <param name="URI"></param>
        /// <param name="Parameters"></param>
        /// <returns></returns>
        private void HttpPost(string URI, string Parameters)//
        {
            try
            {
                System.Net.WebRequest req = System.Net.WebRequest.Create(URI);
                req.Proxy = WebRequest.DefaultWebProxy;
                //Add these, as we're doing a POST
                req.ContentType = "application/x-www-form-urlencoded";
                req.Method = "POST";      
                byte[] bytes = System.Text.Encoding.ASCII.GetBytes(Parameters);
                req.ContentLength = bytes.Length;
                System.IO.Stream os = req.GetRequestStream();
                os.Write(bytes, 0, bytes.Length); 
                os.Close();
                System.Net.WebResponse resp = req.GetResponse();
                if (resp == null) return;
                System.IO.StreamReader sr = new System.IO.StreamReader(resp.GetResponseStream());
                resp.Close();
                return;
            }
            catch (Exception)
            {
                return;
            }
        }

        /// <summary>
        /// Draw bitmap from file path. Bitmaps are used, so files used as image sources are not locked, and image elements can be updated in runtime.
        /// </summary>
        /// <param name="source"> File path</param>
        /// <returns> Bitmap created from file path</returns>
        public static ImageSource BitmapFromUri(Uri source)
        {
            var bitmap = new BitmapImage();
            bitmap.BeginInit();
            bitmap.UriSource = source;
            bitmap.CreateOptions = BitmapCreateOptions.IgnoreImageCache; //Image cache must be ignored, to be able to update the images
            bitmap.CacheOption = BitmapCacheOption.OnLoad;
            bitmap.EndInit();
            bitmap.Freeze(); //Bitmap must be freezable, so it can be accessed from other threads.
            return bitmap;
        }

        public static ImageSource BitmapFromUriWithLimitedSize(Uri source)
        {
            var bitmap = new BitmapImage();
            bitmap.BeginInit();
            bitmap.UriSource = source;
            bitmap.CreateOptions = BitmapCreateOptions.IgnoreImageCache; //Image cache must be ignored, to be able to update the images
            bitmap.CacheOption = BitmapCacheOption.OnLoad;
            bitmap.DecodePixelWidth = 400;
            bitmap.EndInit();
            bitmap.Freeze(); //Bitmap must be freezable, so it can be accessed from other threads.
            return bitmap;
        }


        public void ClearFolder(string dirPath)
        {

            if (Directory.Exists(dirPath))
            {
                DirectoryInfo di = new DirectoryInfo(dirPath);
                try
                {
                    
                    foreach (FileInfo file in di.GetFiles())
                    {
                        file.Delete();
                    }
                 

                }
                catch (Exception ex)
                {
                    logger.Error(ex, "Failed to clear folder");
                }
            }
        }
        private void OpenManual()
        {
            string filePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "UserManual_GisSOM.pdf");
            try
            {
                //if (File.Exists(filePath))
                //{
                    Process.Start(filePath);
                //}


            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to open user manual");
                dialogService.ShowNotification("Failed to open user manual.", "Error");
            }
        }
        private void OpenPlotExternally(ImageSource imgSrc)
        {            
            string filePath = imgSrc.ToString();
            filePath =filePath.Replace("{", "");
            filePath = filePath.Replace("file:", "");
            filePath = filePath.Replace("///", "");
            filePath = filePath.Replace("\"", "");
            try
            {
                if (File.Exists(filePath))
                {
                    Process.Start(filePath);
                }
                
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to open image file");
                dialogService.ShowNotification("Failed to open image file.", "Error");
            }
        }

        private void SaveFile()
        {
            try { 
            string savePath = dialogService.SaveFileDialog("", "png|*.png;", true, true, "Image");
                FileInfo fi = new FileInfo(Path.Combine(Model.OutputFolderTimestamped, "somplot_interactive.png"));
                fi.CopyTo(savePath, true);

            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to save interactive plot.");
            }
        }
        private void SaveClusterFile()
        {
            try
            {
                string savePath = dialogService.SaveFileDialog(Path.Combine(Model.OutputFolderTimestamped,"Clustering"), "dictionary|*.dictionary;", true, true, "clusters");
                FileInfo fi = new FileInfo(Path.Combine(Model.OutputFolderTimestamped, "cluster.dictionary"));

                fi.CopyTo(savePath, true);

            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to save cluster file.");
            }
        }
        private void LoadClusterFile()
        {
            string inputFile = dialogService.OpenFileDialog(Path.Combine(Model.OutputFolderTimestamped, "Clustering"), "*.dictionary | *.dictionary;", true, true);
            try
            {
                File.Copy(inputFile, Path.Combine(Model.OutputFolderTimestamped,"cluster.dictionary"), true);
                Model.ClusterFilePath = Path.Combine(Model.OutputFolderTimestamped, "cluster.dictionary");
                DrawClusters();

 
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to open user manual");
                dialogService.ShowNotification("Failed to open user manual.", "Error");
            }
        }

        private void RegisterFolderWatcher(string folderPath)
        {
            somPlotWatcher = new FileSystemWatcher
            {
                Path = Path.Combine(folderPath, "Interactive"),
                NotifyFilter =  NotifyFilters.LastWrite
                | NotifyFilters.FileName | NotifyFilters.DirectoryName
                
            };
            //NotifyFilter = NotifyFilters.LastAccess | NotifyFilters.LastWrite
            //    | NotifyFilters.FileName | NotifyFilters.DirectoryName
            somPlotWatcher.Changed += new FileSystemEventHandler(OnSomPlotChanged);
            //somPlotWatcher.Changed += new FileSystemEventHandler(OnChanged);
            somPlotWatcher.Created += new FileSystemEventHandler(OnChanged);
            somPlotWatcher.Deleted += new FileSystemEventHandler(OnChanged);
            somPlotWatcher.Renamed += new RenamedEventHandler(OnRenamed);
            somPlotWatcher.EnableRaisingEvents = true;

        }


        public string BrowserToolTip//hacky solution for refreshing browser tooltip
        {
            get
            {
                return "";
            }
            set
            {
                OnPropertyChanged();
                RaisePropertyChanged("BrowserToolTip");
            }
        }
        //public int RunningProcessCount
        //{
        //    get { return runningProcessCount; }
        //    set
        //    {
        //        if (value == runningProcessCount)
        //            return;
        //        else
        //            runningProcessCount = value;
        //        if (runningProcessCount == 0)
        //            IsBusy = false;
        //        else
        //            IsBusy = true;
        //    }
        //}

        /// <summary>
        /// Get and set selectedColumnIndex, for keeping track of seleced data column in DataPreparationView
        /// </summary>
        public int SelectedColumnIndex
        {
            get { return selectedColumnIndex; }
            set
            {
                if (value == selectedColumnIndex) return;
                EditColumn();//Saves the edits to previously selected column before changing columnIndex
                selectedColumnIndex = value;
                OnPropertyChanged();
                RaisePropertyChanged("SelectedColumnIndex");
                DrawHistogram();
                if (value >= 0)
                {
                    NormalizationMin = Model.ColumnDataList[value].NormalizationMin;
                    NormalizationMax = Model.ColumnDataList[value].NormalizationMax;
                }
                
                //if (value == Model.LabelColumnIndex)
                //    IsSelectedLabel = true;
                //else
                //    IsSelectedLabel = false;

            }
        }
        /// <summary>
        /// Name of Input file columns, used by listbox in DataPreparationView
        /// </summary>
        public ObservableCollection<string> ColumnNames
        {
            get { return columnNames; }
            set
            {
                if (value == columnNames) return;
                columnNames = value;
            }
        }

        public ObservableCollection<DataColumn> ColumnData
        {
            get { return columnData; }
            set
            {
                if (value == columnData) return;
                columnData = value;
            }
        }

        /// <summary>
        /// Getting and setting the source for the histogram shown in data preparation stage
        /// </summary>
        public ImageSource DataHistogram
        {
            get { return dataHistogram; }
            set
            {
                if (value == dataHistogram) return;
                dataHistogram = value;
                OnPropertyChanged();
                RaisePropertyChanged("DataHistogram");
            }
        }

        /// <summary>
        /// Get and set the _bitMapPath property
        /// </summary>
        public string BitMapPath
        {
            get { return _bitMapPath; }
            set
            {
                _bitMapPath = string.Empty;
                _bitMapPath = value;
                OnPropertyChanged("BitMapPath");
            }
        }
        /// <summary>
        /// Get and set SomModel
        /// </summary>
        public SomModel Model
        {
            get
            {
                return model;
            }
            set
            {
                model = value;
                RaisePropertyChanged("SomModel");
            }

        }
        /// <summary>
        /// Get or set boolean for checking if selected file is .img. Currently unused and unfinished.
        /// </summary>
        public bool IsImgFile
        {
            get { return isImgFile; }
            set
            {
                if (value == isImgFile) return;
                isImgFile = value;
                OnPropertyChanged();
            }
        }
        /// <summary>
        /// Get or set boolean for checking if selected file is geotiff format
        /// </summary>
        public bool IsGeoTiffFile
        {
            get { return isGeoTiffFile; }
            set
            {
                if (value == isGeoTiffFile) return;
                isGeoTiffFile = value;
                OnPropertyChanged();
            }
        }
        /// <summary>
        /// Get or set boolean for checking if selected file is csv format
        /// </summary>
        public bool IsCsvFile
        {
            get { return isCsvFile; }
            set
            {
                if (value == isCsvFile) return;
                isCsvFile = value;
                OnPropertyChanged();
            }
        }


        /// <summary>
        /// get and set fileSelected variable for checking if user has selecetd an input file.
        /// </summary>
        public bool FileSelected
        {
            get { return fileSelected; }
            set
            {
                if (value == fileSelected) return;
                fileSelected = value;
                OnPropertyChanged();
            }
        }
        /// <summary>
        /// Binding from xaml to show advanced parameters section. should this binding be moved fully to XAML? bind visibilty directly to togglebutton isChecked property
        /// I don't think the viewModel needs this information in this case.
        /// </summary>
        public bool ShowAdvancedParams
        {
            get { return showAdvancedParams; }
            set
            {
                if (value == showAdvancedParams) return;
                showAdvancedParams = value;
                OnPropertyChanged();
            }
        }
        /// <summary>
        /// Get or set boolean for checking whether tool is running
        /// </summary>
        public bool IsBusy
        {
            get { return isBusy; }
            set
            {
                if (isBusy == value) return;
                isBusy = value;
                RaisePropertyChanged(() => IsBusy);
                OnPropertyChanged();
                RunToolCommand.RaiseCanExecuteChanged();
                SelectCsvFileCommand.RaiseCanExecuteChanged();
                //SelectLrnFileCommand.RaiseCanExecuteChanged();
                SelectFilesCommand.RaiseCanExecuteChanged();
            }
        }
        public int SelectedClusterIndex
        {
            get { return selectedClusterIndex; }
            set
            {
                if (selectedClusterIndex == value) return;
                selectedClusterIndex = value;
            }
        }
        public bool IsSelectedNorthing
        {
            get { return isSelectedNorthing; }
            set
            {
                if (isSelectedNorthing == value) return;
                isSelectedNorthing = value;
                if (isSelectedNorthing == true)
                {
                    IsSelectedEasting = false;
                }
                OnPropertyChanged();
                RaisePropertyChanged("IsSelectedNorthing");
            }
        }
        public bool IsSelectedEasting
        {
            get { return isSelectedEasting; }
            set
            {
                if (isSelectedEasting == value) return;
                isSelectedEasting = value;
                if (isSelectedEasting == true)
                {
                    IsSelectedNorthing = false;
                }
                OnPropertyChanged();
                RaisePropertyChanged("IsSelectedNorthing");
            }
        }
        public bool IsSelectedLabel
        {
            get { return isSelectedLabel; }
            set
            {
                if (isSelectedLabel == value) return;
                isSelectedLabel = value;
                OnPropertyChanged();
                RaisePropertyChanged("IsSelectedLabel");
            }
        }
        public string FlyOutText
        {
            get { return flyOutText; }
            set
            {
                if (flyOutText == value) return;
                flyOutText = value;
                OnPropertyChanged();
            }
        }
        public bool StatusFlyOutOpen
        {
            get { return statusFlyOutOpen; }
            set
            {
                if (statusFlyOutOpen == value) return;
                statusFlyOutOpen = value;
                OnPropertyChanged();
            }
        }
        public bool ShowSettingsFlyOut//Rename this, so the method can be named properly
        {
            get { return showSettingsFlyout; }
            set
            {
                if (showSettingsFlyout == value) return;
                showSettingsFlyout = value;
                OnPropertyChanged();
            }
        }
        public string PythonPath //This is now deprecated? unnecessary? because of change into pre-packaged python exe files
        {
            get
            {
                return pythonPath;
            }
            set
            {
                if (pythonPath == value) return;
                pythonPath = value;
                OnPropertyChanged();
            }
        }
        public string PythonLogText 
        {
            get { return pythonLogText; }
            set
            {
                if (pythonLogText == value) return;
                pythonLogText = value;
                OnPropertyChanged();       
            }
        }

        public double NormalizationMin//delete this from Model, as these are moved to DataColumns
        {  
            get { return normalizationMin; }
            set{ if (normalizationMin == value) return;
                normalizationMin = value;
                OnPropertyChanged();
                Model.ColumnDataList[SelectedColumnIndex].NormalizationMin = value;
            }
        }

        public double NormalizationMax//delete this from Model, as these are moved to DataColumns
        {
            get { return normalizationMax; }
            set
            {
                if (normalizationMax == value) return;
                normalizationMax = value;
                OnPropertyChanged();
                Model.ColumnDataList[SelectedColumnIndex].NormalizationMax = value;
            }
        }


        private void AddToImageCollection(ObservableCollection<ImageSource> ImageCollection, string PlotDirectory)
        {
            ImageSource imageSrc;
            DirectoryInfo d;
            FileInfo[] Files;
            string fullPath;
            try
            {
                App.Current.Dispatcher.Invoke((Action)delegate         //delegate to access different thread
                {
                    ImageCollection.Clear();
                });
                d = new DirectoryInfo(PlotDirectory);
                Files = d.GetFiles("*.png").OrderBy(p => p.CreationTime).ToArray(); //Getting png files
                
                foreach (FileInfo file in Files)
                {
                    fullPath = Path.Combine(PlotDirectory, file.Name);//full path of images to copy to final output destination
                    
                    imageSrc = BitmapFromUriWithLimitedSize(new Uri(fullPath));    //HERE: if Files()count yli jotain, aseta max koko.
                    App.Current.Dispatcher.Invoke((Action)delegate
                    {
                        ImageCollection.Add(imageSrc);
                    });

                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to show output images");
            }
        }
        private void MoveWithReplace(string sourceFileName, string destFileName)
        {

            //first, delete target file if exists, as File.Move() does not support overwrite.
            if (File.Exists(destFileName))
            {
                File.Delete(destFileName);
            }

            File.Move(sourceFileName, destFileName);

        }

        public int RunningProcessCount
        {
            get { return runningProcessCount; }
            set
            {
                if (value == runningProcessCount)
                    return;
                else
                    runningProcessCount = value;
                if (runningProcessCount == 0)
                    IsBusy = false;
                else
                    IsBusy = true;
            }
        }
        //private bool CanRunTool()
        //{
        //    return !IsBusy;
        //}

        //public bool IsBusy
        //{
        //    get { return isBusy; }
        //    set
        //    {
        //        if (isBusy == value) return;
        //        isBusy = value;
        //        RaisePropertyChanged(() => IsBusy);
        //        OnPropertyChanged();
        //    }
        //}
        /// <summary>
        /// Get script process output.
        /// </summary>
        /// <param name="myProcess">Process</param>
        private void ScriptOutput(Process myProcess)
        {
            myProcess.OutputDataReceived += new DataReceivedEventHandler((sender, e) =>
            {
                if (!String.IsNullOrEmpty(e.Data) && !e.Data.ToLower().Contains("matplotlibdata") && !e.Data.ToLower().Contains("return_n_iter") && !e.Data.ToLower().Contains("HTTP"))
                {
                    PythonLogText += e.Data + "\r\n";
                    if (!e.Data.ToLower().Contains("POST") && !e.Data.ToLower().Contains("typeerror") && e.Data.ToLower().Contains("error"))
                    {
                        //dialogService.ShowNotification("Failed to draw interactive plot.See the log file for details.", "Error");
                    }
                }
            });
        }

        private void ScriptOutputForPlots(Process myProcess)
        {
            string GeoPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Geo");
            string SomPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Som");
            string BoxPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Boxplot");
            string ScatterPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Scatterplot");
            myProcess.OutputDataReceived += new DataReceivedEventHandler((sender, e) =>
            {
                if (!String.IsNullOrEmpty(e.Data) && !e.Data.ToLower().Contains("matplotlibdata") && !e.Data.ToLower().Contains("return_n_iter") && !e.Data.ToLower().Contains("HTTP"))
                {
                    PythonLogText += e.Data + "\r\n";
                    if (!e.Data.ToLower().Contains("POST") && !e.Data.ToLower().Contains("typeerror") && e.Data.ToLower().Contains("error"))
                    {
                        //dialogService.ShowNotification("Failed to draw interactive plot.See the log file for details.", "Error");
                    }
                    if (e.Data.ToLower().Contains("geospace"))
                    {
                        AddToImageCollection(GeoSpaceImageList, GeoPlotDirectory);

                    }
                    if (e.Data.ToLower().Contains("somspace"))
                    {
                        AddToImageCollection(SomImageList, SomPlotDirectory);
                    }
                    if (e.Data.ToLower().Contains("boxplot"))
                    {
                        AddToImageCollection(BoxPlotList, BoxPlotDirectory);
                        var SomViewModel = ServiceLocator.Current.GetInstance<SomViewModel>();
                        SomViewModel.RaisePropertyChanged("BoxPlotList");

                    }
                    if (e.Data.ToLower().Contains("scatterplot"))
                    {
                        AddToImageCollection(ScatterPlotList, ScatterPlotDirectory);
                    }
                }


            });
        }

        /// <summary>
        /// Get script process error output.
        /// </summary>
        /// <param name="myProcess">Process</param>
        private void ScriptError(Process myProcess)
        {
            myProcess.ErrorDataReceived += new DataReceivedEventHandler((sender, e) =>
            {
                if (!String.IsNullOrEmpty(e.Data) && !e.Data.Contains("MATPLOTLIBDATA") && !e.Data.Contains("hoverdata") && !e.Data.ToLower().Contains("return_n_iter")&& !e.Data.ToLower().Contains("matplotlibdeprecationwarning") && !e.Data.ToLower().Contains("exec(bytecode") && !e.Data.Contains("POST") && !e.Data.Contains("GET"))//filter out persistent and unnecessary python warnings
                {
                    logger.Error(e.Data);
                    PythonLogText += e.Data + "\r\n";
                }
            });
        }

        /// <summary>
        /// Get script process output.
        /// </summary>
        /// <param name="myProcess">Process</param>
        private void ScriptOutputForSplitToColumns(Process myProcess)
        {
            myProcess.OutputDataReceived += new DataReceivedEventHandler((sender, e) =>
            {
                if (!String.IsNullOrEmpty(e.Data) && !e.Data.ToLower().Contains("matplotlibdata") && !e.Data.ToLower().Contains("return_n_iter") && !e.Data.ToLower().Contains("HTTP"))
                {
                    if(e.Data.ToLower().Contains("warning"))
                        PythonLogText += e.Data + "\r\n";//only print warnings
                    if (!String.IsNullOrEmpty(e.Data))
                    {
                        
                            Model.NoDataValue = e.Data;
                        //dialogService.ShowNotification("Failed to draw interactive plot.See the log file for details.", "Error");
                    }
                }
            });
        }

        /// <summary>
        /// Get script process error output.
        /// </summary>
        /// <param name="myProcess">Process</param>
        //private void ScriptErrorForSplitToColumns(Process myProcess)
        //{
        //    myProcess.ErrorDataReceived += new DataReceivedEventHandler((sender, e) =>
        //    {
        //    });
        //}

        private void SelectAll(ObservableCollection<BoolStringHelper> collection)
        {
            for (int i=0;i<collection.Count;i++)
            {
                collection[i].IsSelected = true;//.Item2 = true;
            }
        }

        private void DeSelectAll(ObservableCollection<BoolStringHelper> collection)
        {
            for (int i = 0; i < collection.Count; i++)
            {
                collection[i].IsSelected = false;
            }
        }

        private void UnCheckNorthing(DataColumn item)
        {

            foreach (DataColumn c in Model.ColumnDataList)
            {
                if (item.Name != c.Name)
                { //tai miten vertaatkaan
                    c.IsNorthing = false;
                }
            }
        }
        private void UnCheckEasting(DataColumn item)
        {

            foreach (DataColumn c in Model.ColumnDataList)
            {
                if (item.Name != c.Name)
                { //tai miten vertaatkaan
                    c.IsEasting = false;
                }
            }
        }
        private void UnCheckLabel(DataColumn item)
        {

            foreach (DataColumn c in Model.ColumnDataList)
            {
                if (item.Name != c.Name)
                { //tai miten vertaatkaan
                    c.IsLabel = false;
                }
            }
        }

        public void ShowResultsInFileSystem(string s)
        {

            try
            {
                if(s.Length>0)
                    Process.Start(Path.Combine(Model.OutputFolderTimestamped,s));
                else
                    Process.Start(Model.OutputFolderTimestamped);

            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to open results folder.");
                dialogService.ShowNotification("Failed to open results folder.", "Error");
            }
        }
    }
}
