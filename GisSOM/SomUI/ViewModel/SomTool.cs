using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using SomUI.Model;
using SomUI.Service;
using NLog;
using System.Runtime.CompilerServices;
using System.Net;
using CommonServiceLocator;
using GalaSoft.MvvmLight.Ioc;
using System.ComponentModel;
using System.IO;
using System.Diagnostics;
using System.Collections.ObjectModel;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Xml;

namespace SomUI.ViewModel
{
    /// Python process executables are launched from this VM. Most of the UI bound properties and interaction logic is handled by SomViewModel. NOTE: This really shouldn't be a 
    //ViewModel by definition? More of a model, or a "Tool" class separate from MVVM? at least not a ViewModel.   
    public class SomTool //: ViewModelBase, INotifyPropertyChanged
    {
        private readonly ILogger logger = NLog.LogManager.GetCurrentClassLogger();
        private string pythonPath = "C:/Users/shautala/AppData/Local/Programs/Python/Python39/python.exe"; // used for debugging.
        private bool usePyExes = false;//for switching running of scripts between packed python executables and full python installation. used for debugging.
        private ObservableCollection<Process> PythonProcesses = new ObservableCollection<Process>();

        private event PropertyChangedEventHandler PropertyChanged;

        /// <summary>
        /// Initialize new instance of SomTool class
        /// </summary>
        public SomTool()
        {
            this.logger = NLog.LogManager.GetCurrentClassLogger();
            if (File.Exists(Path.Combine(System.IO.Path.GetTempPath(), "GisSOM", "settingsFile.txt")))
            {
                pythonPath = File.ReadAllText(Path.Combine(System.IO.Path.GetTempPath(), "GisSOM", "settingsFile.txt"));
            }
        }
       


        /// <summary>
        /// Draw interactive plots
        /// </summary>
        /// <param name="Model">SomModel</param>
        /// <param name="ScriptOutput"></param>
        /// <param name="ScriptError"></param>
        public async Task DataPreparationInteractive(SomModel Model, Action<Process> ScriptOutput, Action<Process> ScriptError)
        {
            await Task.Run(async () =>
            {
                //HttpPost("http://localhost:8051/shutdown", "message=shuts down interactive data preparation"); //Task t = 
                      
                //var dataPrepFolder = Path.Combine(Model.Output_Folder, "DataPreparation"); //Folder to save edited input file into                             
                
                ProcessStartInfo myProcessStartInfo;
                var scriptPath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "data_preparation_interactive.py");         
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "data_preparation_interactive.exe");

                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);

                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true;

          
                if (usePyExes)
                    myProcessStartInfo.Arguments ="--input_file="+"\"" + Model.InputFile + "\"" + " " + "--output_folder="+ "\"" + Model.Output_Folder + "\"" + " " + "--data_shape="+"\"" + Model.DataShape + "\"";
                else
                    myProcessStartInfo.Arguments = "-u" + " " +"\"" + scriptPath + "\""+" "+ "--input_file="+"\"" + Model.InputFile + "\"" + " " + "--output_folder="+ "\"" + Model.Output_Folder + "\"" + " " + "--data_shape="+"\"" + Model.DataShape + "\"";
                myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");
                Console.WriteLine(myProcessStartInfo.Arguments);
                using (var myProcess = new Process())
                {
                    PythonProcesses.Add(myProcess);
                    myProcess.StartInfo = myProcessStartInfo;
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginOutputReadLine();
                    myProcess.BeginErrorReadLine();
                    myProcess.Close();
                    PythonProcesses.Remove(myProcess);
                };



            });
        }



        /// <summary>
        /// Main somoclu run
        /// </summary>
        /// <param name="Model"></param>
        /// <param name="SomImageList"></param>
        /// <param name="GeoSpaceImageList"></param>
        /// <param name="BoxPlotList"></param>
        /// <param name="ScatterPlotList"></param>
        /// <param name="ClusterPlotList"></param>
        /// <param name="ScriptOutput"></param>
        /// <param name="ScriptError"></param>
        public async Task RunTool(SomModel Model, ObservableCollection<ImageSource> SomImageList, ObservableCollection<ImageSource> GeoSpaceImageList, ObservableCollection<ImageSource> BoxPlotList, ObservableCollection<ImageSource> ScatterPlotList, ObservableCollection<ImageSource> ClusterPlotList, Action<Process> ScriptOutput, Action<Process> ScriptError)//kopiona model?
        {
            await Task.Run(() =>
            {
                App.Current.Dispatcher.Invoke((Action)delegate
                {
                    SomImageList.Clear();
                    GeoSpaceImageList.Clear();
                    BoxPlotList.Clear();
                    ScatterPlotList.Clear();
                    ClusterPlotList.Clear();
                });
                
                var scriptPath = System.AppDomain.CurrentDomain.BaseDirectory + "scripts/nextsom_wrap.py";
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "nextsom_wrap.exe");
                var editedData = Path.Combine(Model.Output_Folder, "DataPreparation", "EditedData.lrn");
                Model.Output_file_somspace = Model.OutputFolderTimestamped + "/result_som.txt";
                //if (Model.IsSpatial == true)
                //    Model.Output_file_geospace = Model.OutputFolderTimestamped + "/result_geo.txt";
                //else
                //    Model.Output_file_geospace = "";


                XmlDocument doc = new XmlDocument();
                
                var dataStatsFilePath = Path.Combine(Model.OutputFolderTimestamped, "DataStats.xml");
                try
                {
                    doc.Load(dataStatsFilePath);
                    XmlNode root = doc.DocumentElement;
                    XmlNode scaledNode = root.SelectSingleNode("descendant::" + "isScaled");
                    Model.IsNormalized = bool.Parse(scaledNode.InnerText); //
                    XmlNode spatialNode = root.SelectSingleNode("descendant::" + "isSpatial");
                    Model.IsSpatial = bool.Parse(spatialNode.InnerText); //
                }
                catch(Exception ex)
                {
                    logger.Error(ex, "Failed to read parameters from DataStats.txt -file. Data will be assumed to be non-spatial and non-scaled");
                    Model.IsNormalized = false;
                    Model.IsSpatial = false;
                }
                Model.Output_file_geospace = Model.OutputFolderTimestamped + "/result_geo.txt";//Change it so that even when the run is nonspatial a dummy file is written
                string inputFile;
                if (File.Exists(editedData))
                {
                    inputFile = editedData;
                }
                else
                    inputFile = Model.InputFile;

                try
                {
                    File.Copy(inputFile, Path.Combine(Model.OutputFolderTimestamped, "InputData.lrn"));
                }
                catch (Exception ex)
                {
                    logger.Error(ex, "Failed to copy input data.");
                }

                var logFilePath = Path.Combine(Model.OutputFolderTimestamped, "RunStats.txt");
                try
                {
                    if (File.Exists(logFilePath))
                        File.Delete(logFilePath);
                }
                catch (Exception ex)
                {
                    logger.Error(ex, "Failed to clear RunStats.txt.");
                }
                using (StreamWriter sw = File.CreateText(logFilePath))
                {
                    sw.WriteLine("Run Date:{0}\r\n\r\n", DateTime.UtcNow);
                    sw.Write(
                    "Som input Parameters: \r\n\r\n" + "InputFile: '{0}'\r\n" + "ScriptPath: '{1}'\r\n" + "OutGeoFile: '{2}'\n" + "OutSomFile: '{3}'\r\n" + "som_x: '{4}'\r\n" + "som_y: '{5}'\r\n" +
                    "epochs: '{6}'\r\n" + "kmeans_min: '{7}'\r\n" + "kmeans_max: '{8}'\r\n" + "kmeans_init: '{9}'\r\n" + "kmeans: '{10}'\r\n" +
                    "neighborhood: {11}\r\n" + "radius0: {12}\r\n" + "radiusN: {13}\r\n" + "maptype: {14}\r\n" + "scalecooling: {15}\r\n" +
                    "scale0: {16}\r\n" + "scaleN: {17}\r\n" + "initialization: {18}\r\n" + "gridtype: {19}\r\n" + "dataShape: {20}\r\n" + "output_folder: {21}\r\n\r\n",
                    Model.InputFile, scriptPath, Model.Output_file_geospace, Model.Output_file_somspace, Model.Som_x, Model.Som_y,
                    Model.Epochs, Model.KMeans_min, Model.KMeans_max, Model.KMeans_initializations, Model.KMeans,
                    Model.Neighborhood, Model.InitialNeighborhood, Model.FinalNeighborhood, Model.MapType, Model.TrainingRateFunction,
                    Model.TrainingRateInitial, Model.TrainingRateFinal, Model.Initialization, Model.GridShape, Model.DataShape, Model.OutputFolderTimestamped
                );
                    WriteRunStatsXml(Model,Path.Combine(Model.OutputFolderTimestamped, "RunStats.xml"));
                }
                logger.Trace( 
                    "SomInputParams:\n" + "\tInputFile: '{0}'\n" + "\tScriptPath: '{1}'\n" + "\tOutGeoFile: '{2}'\n" + "\tOutSomFile: '{3}'\n" + "\tsom_x: '{4}'\n" + "\tsom_y: '{5}'\n" +
                    "\tepochs: '{6}'\n" + "\tkmeans_min: '{7}'\n" + "\tkmeans_max: '{8}'\n" + "\tkmeans_init: '{9}'\n" + "\tkmeans: '{10}'\n" +
                    "\tneighborhood: {11}\n" + "\tradius0: {12}\n" + "\tradiusN: {13}\n" + "\tmaptype: {14}\n" + "\tscalecooling: {15}\n" +
                    "\tscale0: {16}\n" + "\tscaleN: {17}\n" + "\tinitialization: {18}\n" + "\tgridtype: {19}\n" + "\toutput_folder: {20}\n",
                    Model.InputFile, scriptPath, Model.Output_file_geospace, Model.Output_file_somspace, Model.Som_x, Model.Som_y,
                    Model.Epochs, Model.KMeans_min, Model.KMeans_max, Model.KMeans_initializations, Model.KMeans,
                    Model.Neighborhood, Model.InitialNeighborhood, Model.FinalNeighborhood, Model.MapType, Model.TrainingRateFunction,
                    Model.TrainingRateInitial, Model.TrainingRateFinal, Model.Initialization, Model.GridShape, Model.OutputFolderTimestamped
                );



                //var scaleMinList = new List<double>();
                //var scaleMaxList = new List<double>(); //this is not an elegant solution, needs reworking.

                //for (int i = 0; i < Model.ColumnDataList.Count(); i++)//in this case exclusion and inclusion is already handed on the data side of things, so take only included cols.
                //{
                //    if (Model.ColumnDataList[i].IsExcluded == false)
                //    {
                //        scaleMinList.Add(Model.ColumnDataList[i].NormalizationMin);
                //        scaleMaxList.Add(Model.ColumnDataList[i].NormalizationMax);
                //    }

                //}


                ProcessStartInfo myProcessStartInfo;
                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);

                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true;
                if (usePyExes)
                    myProcessStartInfo.Arguments = "";
                else
                    myProcessStartInfo.Arguments = "-u" + " " + "\"" + scriptPath + "\"" + " ";


                myProcessStartInfo.Arguments += "--input_file=" + "\"" + inputFile + "\"" + " " +
                        "--output_file_somspace=" + "\"" + Model.Output_file_somspace + "\"" + " " +
                        "--som_x=" + Model.Som_x + " " +
                        "--som_y=" + Model.Som_y + " " +
                        "--epochs=" + Model.Epochs + " " +
                        "--kmeans_min=" + Model.KMeans_min + " " +
                        "--kmeans_max=" + Model.KMeans_max + " " +
                        "--kmeans_init=" + Model.KMeans_initializations + " " +
                        "--kmeans=" + Model.KMeans + " " +
                        "--neighborhood=" + Model.Neighborhood + " " +
                        "--radius0=" + Model.InitialNeighborhood + " " +
                        "--radiusN=" + Model.FinalNeighborhood + " " +
                        "--maptype=" + Model.MapType + " " +
                        "--scalecooling=" + Model.TrainingRateFunction + " " +
                        "--scale0=" + Model.TrainingRateInitial + " " +
                        "--scaleN=" + Model.TrainingRateFinal + " " +
                        "--initialization=" + Model.Initialization + " " +
                        "--gridtype=" + Model.GridShape + " " +
                        "--output_folder=" + "\"" + Model.OutputFolderTimestamped + "\"";

                if (Model.InitialCodeBook != "")     //If initial codebook parameter was given, pass it on as a command line variable
                    myProcessStartInfo.Arguments += " " + "--initialcodebook=" + "\"" + Model.InitialCodeBook + "\"";
                if (Model.Output_file_geospace.Length > 0)
                    myProcessStartInfo.Arguments += " " + "--output_file_geospace=" + "\"" + Model.Output_file_geospace + "\"";
                if (Model.InputFile.Substring(Model.InputFile.Length - 3) == "tif")
                    myProcessStartInfo.Arguments += " " + "--geotiff_input=" + "\"" + Model.InputFile + "\"";
                if (Model.LabelColumnIndex>-2)
                    myProcessStartInfo.Arguments += " " + "--label=" + "\"" + "true" + "\"";
                if (Model.IsNormalized == true)
                {
                    myProcessStartInfo.Arguments += " " + "--normalized=" + "\"" + "True" + "\"";//+ " " + "--scale_min_list=" + string.Join(",", scaleMinList) + " " + "--scale_max_list=" + string.Join(",", scaleMaxList) ;//+"--minN=" +Model.NormalizationMin+ " " +"--maxN="+ Model.NormalizationMax;
                }

                myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");
                using (var myProcess = new Process())
                {
                    PythonProcesses.Add(myProcess);
                    myProcess.StartInfo = myProcessStartInfo;
                    //PythonLogText = "";
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginErrorReadLine();
                    myProcess.BeginOutputReadLine();
                    myProcess.WaitForExit();
                    myProcess.Close();
                    PythonProcesses.Remove(myProcess);
                };
            });

            Model.KMeans_min_last_calculation = Model.KMeans_min;
            Model.KMeans_max_last_calculation = Model.KMeans_max;
            Model.ClusterFilePath = Path.Combine(Model.OutputFolderTimestamped, "cluster.dictionary");
            //if (Model.KMeans != "False")
            //    DrawClusters(Model, ClusterPlotList);
            //App.Current.Dispatcher.Invoke((Action)delegate
            //{
            //    ClusterPlotList.Clear();
            //});
            
        }


        /// <summary>
        /// Draw result images
        /// </summary>
        /// <param name="redraw"></param>
        /// <param name="Model"></param>
        /// <param name="SomImageList"></param>
        /// <param name="GeoSpaceImageList"></param>
        /// <param name="BoxPlotList"></param>
        /// <param name="ScatterPlotList"></param>
        /// <param name="ScriptOutput"></param>
        /// <param name="ScriptError"></param>
        public async Task DrawResults(string redraw, SomModel Model, ObservableCollection<ImageSource> SomImageList, ObservableCollection<ImageSource> GeoSpaceImageList, ObservableCollection<ImageSource> BoxPlotList, ObservableCollection<ImageSource> ScatterPlotList, Action<Process> ScriptOutput, Action<Process> ScriptError)
        {
            

            await Task.Run(() =>
            {
                string GeoPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Geo");
                string SomPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Som");
                string BoxPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Boxplot");
                string ScatterPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Scatterplot");
                ClearFolder(SomPlotDirectory);
                ClearFolder(GeoPlotDirectory);
                ClearFolder(BoxPlotDirectory);
                ClearFolder(ScatterPlotDirectory);

                //HttpPost("http://localhost:8050/shutdown", "message=shuts down interactive plots"); //send shutdown message to close any open interactive plots. The actual message doesnt matter, only the address.
                var dataPrepFolder = Path.Combine(Model.Output_Folder, "DataPreparation"); //Folder to read edited input file from
                var outputDir = Model.OutputFolderTimestamped;
                string inputFile;
                if (File.Exists(Path.Combine(dataPrepFolder, "EditedData.lrn")))
                {
                    inputFile = Path.Combine(dataPrepFolder, "EditedData.lrn");
                }
                else
                    inputFile = Model.InputFile;

                var somPlotScriptPath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "nextsom_plot.py");            //Path to python script file in case of script launch
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "nextsom_plot.exe"); //path to executable file in case of executable launch (default).
                ProcessStartInfo myProcessStartInfo;
                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);

                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true;



                XmlDocument doc = new XmlDocument();

                var dataStatsFilePath = Path.Combine(Model.OutputFolderTimestamped, "DataStats.xml");
                try
                {
                    doc.Load(dataStatsFilePath);
                    XmlNode root = doc.DocumentElement;
                    XmlNode scaledNode = root.SelectSingleNode("descendant::" + "isScaled");
                    Model.IsNormalized = bool.Parse(scaledNode.InnerText); //
                    XmlNode spatialNode = root.SelectSingleNode("descendant::" + "isSpatial");
                    Model.IsSpatial = bool.Parse(spatialNode.InnerText); //
                    XmlNode nodataNode = root.SelectSingleNode("descendant::" + "noDataValue");
                    Model.NoDataValue = nodataNode.InnerText;
                }
                catch (Exception ex)
                {
                    logger.Error(ex, "Failed to read parameters from DataStats.txt -file. This may affect plotting results.");
                    Model.IsNormalized = false;
                    Model.IsSpatial = false;
                    Model.NoDataValue = "";
                }



                if (usePyExes)
                    myProcessStartInfo.Arguments =  " "+"--outsomfile=" + "\"" + Model.Output_file_somspace + "\"" + " " + "--som_x=" + Model.Som_x + " " + "--som_y=" + Model.Som_y + " " + "\"" + "--input_file=" + inputFile + "\"" + " " + "\"" + "--dir=" + Model.OutputFolderTimestamped + "\"" + " " + "--grid_type=" + Model.GridShape + " --noDataValue=\"" + Model.NoDataValue + "\"";
                else
                    myProcessStartInfo.Arguments = "-u" + " " + "\"" + somPlotScriptPath + "\"" + " " + "--outsomfile=" + "\"" + Model.Output_file_somspace + "\"" + " " + "--som_x=" + Model.Som_x + " " + "--som_y=" + Model.Som_y + " " + "--input_file=" + "\"" + inputFile + "\"" + " " + "--dir=" + "\"" + Model.OutputFolderTimestamped + "\"" + " " + "--grid_type=" + Model.GridShape + " --noDataValue=\"" + Model.NoDataValue + "\"";

                //myProcessStartInfo.Arguments += " " + "--labelIndex=" + "\"" + Model.LabelColumnIndex + "\"";
                //myProcessStartInfo.Arguments += " " + "--original_data_dir=" + "\"" + Model.Output_Folder + "\"";
                myProcessStartInfo.Arguments += " " + "--dataType=" + "\"" + Model.DataShape + "\"";
                if(Model.IsSpatial==true)
                {
                    myProcessStartInfo.Arguments += " " + "--outgeofile=" + "\"" + Model.Output_file_geospace + "\"";
                    //myProcessStartInfo.Arguments += " " + "--eastingIndex=" + "\"" + Model.EastingColumnIndex + "\"";
                    //myProcessStartInfo.Arguments += " " + "--northingIndex=" + "\"" + Model.NorthingColumnIndex + "\"";                   
                }
              myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");
                using (var myProcess = new Process())
                {
                    PythonProcesses.Add(myProcess);
                    myProcess.StartInfo = myProcessStartInfo;
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginErrorReadLine();
                    myProcess.BeginOutputReadLine();
                    myProcess.WaitForExit();
                    myProcess.Close();
                    PythonProcesses.Remove(myProcess);
                };               
            });          
        }

        /// <summary>
        /// Add new label data to an already existing som result
        /// </summary>
        /// <param name="Model"></param>
        /// <param name="ScriptOutput"></param>
        /// <param name="ScriptError"></param>
        /// <returns></returns>
        public async Task NewLabelData(SomModel Model, Action<Process> ScriptOutput, Action<Process> ScriptError)
        {
            await Task.Run(() =>
            {
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "new_label_data.exe"); 
                var somPlotScriptPath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "new_label_data.py");
                ProcessStartInfo myProcessStartInfo;
                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);

                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true;

                if (usePyExes)
                    myProcessStartInfo.Arguments = " " + "--outsomfile=" + "\"" + Model.Output_file_somspace + "\""+" " + "--outgeofile=" + "\"" + Model.Output_file_geospace + "\""+" " + " " + "--som_x=" + Model.Som_x + " " + "--som_y=" + Model.Som_y + " " + "\"" + "--input_file=" + Model.InputFile + "\"" + " " + "\"" + "--dir=" + Model.OutputFolderTimestamped + "\"" + " " + "--grid_type=" +"\""+ Model.GridShape+"\""+" "+ "--newLabelData="+"\""+Model.NewLabelData+"\"";//+newlabeldata
                else
                    myProcessStartInfo.Arguments = "-u" + " " + "\"" + somPlotScriptPath + "\"" + " " + "--outsomfile=" + "\"" + Model.Output_file_somspace + "\""+" " + "--outgeofile=" + "\"" + Model.Output_file_geospace + "\"" + " " + "--som_x=" + Model.Som_x + " " + "--som_y=" + Model.Som_y + " " + "--input_file=" + "\"" + Model.InputFile + "\"" + " " + "--dir=" + "\"" + Model.OutputFolderTimestamped + "\"" + " " + "--grid_type=" +"\""+ Model.GridShape+"\"" + " " + "--newLabelData=" + "\"" +Model.NewLabelData+ "\"";
                myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");
                using (var myProcess = new Process())
                {
                    myProcess.StartInfo = myProcessStartInfo;
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginErrorReadLine();
                    myProcess.BeginOutputReadLine();
                    myProcess.WaitForExit();
                    myProcess.Close();
                };            

                var BitMapPath = Path.Combine(Model.OutputFolderTimestamped,"Som", "cluster_new.png");
                ImageSource imageSrc = BitmapFromUri(new Uri(BitMapPath));
                Model.NewLabelPlot = imageSrc;

                BitMapPath = Path.Combine(Model.OutputFolderTimestamped, "Som", "labels_new.png");
                imageSrc = BitmapFromUri(new Uri(BitMapPath));
                Model.NewLabelLegend = imageSrc;                
            });
        }

        /// <summary>
        /// Draw scatterplots from som results
        /// </summary>
        /// <param name="Model"></param>
        /// <param name="ScriptOutput"></param>
        /// <param name="ScriptError"></param>
        /// <returns></returns>
        public async Task DrawScatterPlots(SomModel Model, Action<Process> ScriptOutput, Action<Process> ScriptError)
        {

            await Task.Run(() =>
            {

                var formattedDrawList = new List<int>();
                for(int i=0; i < Model.ScatterPlotList.Count; i++)
                {
                    if (Model.ScatterPlotList[i].IsSelected == true)
                        formattedDrawList.Add(1);
                    else 
                        formattedDrawList.Add(0);
                }
                string ScatterPlotDirectory = Path.Combine(Model.OutputFolderTimestamped, "Scatterplot");
                //ClearFolder(ScatterPlotDirectory);
                var dataPrepFolder = Path.Combine(Model.Output_Folder, "DataPreparation"); //Folder to read edited input file from
                var outputDir = Model.OutputFolderTimestamped;
                string inputFile;
                if (File.Exists(Path.Combine(dataPrepFolder, "EditedData.lrn")))
                {
                    inputFile = Path.Combine(dataPrepFolder, "EditedData.lrn");
                }
                else
                    inputFile = Model.InputFile;

                var somPlotScriptPath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "draw_scatterplots.py");            //Path to python script file in case of script launch
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "draw_scatterplots.exe"); //path to executable file in case of executable launch (default).
                ProcessStartInfo myProcessStartInfo;
                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);
                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true;


                if (usePyExes)
                    myProcessStartInfo.Arguments = " " + "--outsomfile=" + "\"" + Model.Output_file_somspace + "\"" + " " + "--som_x=" + Model.Som_x + " " + "--som_y=" + Model.Som_y + " " + "\"" + "--input_file=" + inputFile + "\"" + " " + "\"" + "--dir=" + Model.OutputFolderTimestamped + "\"" + " " + "--draw_list=" + "\""+ String.Join(", ", formattedDrawList.ToArray()).Replace(" ","")+ "\""; 
                else
                    myProcessStartInfo.Arguments = "-u" + " " + "\"" + somPlotScriptPath + "\"" + " " + "--outsomfile=" + "\"" + Model.Output_file_somspace + "\"" + " " + "--som_x=" + Model.Som_x + " " + "--som_y=" + Model.Som_y + " " + "--input_file=" + "\"" + inputFile + "\"" + " " + "--dir=" + "\"" + Model.OutputFolderTimestamped + "\"" + " " + "--draw_list=" + "\"" + String.Join(", ", formattedDrawList.ToArray()).Replace(" ", "") + "\"";

                myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");


                using (var myProcess = new Process())
                {
                    PythonProcesses.Add(myProcess);
                    myProcess.StartInfo = myProcessStartInfo;
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginOutputReadLine();
                    myProcess.BeginErrorReadLine();
                    myProcess.WaitForExit();
                    myProcess.Close();
                    PythonProcesses.Remove(myProcess);
                };
            });
        }


        /// <summary>
        /// Draw interactive plots
        /// </summary>
        /// <param name="Model">SomModel</param>
        /// <param name="ScriptOutput"></param>
        /// <param name="ScriptError"></param>
        public async Task DrawResultsInteractive(SomModel Model, Action<Process> ScriptOutput, Action<Process> ScriptError)
        {
            await Task.Run(async () =>
            {
                HttpPost("http://localhost:8050/shutdown");//, "message=shuts down interactive plots"); //Task t = 
                //await t;


                


                var dataPrepFolder = Path.Combine(Model.OutputFolderTimestamped, "DataPreparation"); //Folder to read edited input file from
                var outputDir = Path.Combine(Model.OutputFolderTimestamped, "somresults");
                string inputFile;
                if (File.Exists(Path.Combine(dataPrepFolder, "EditedData.lrn")))
                {
                    inputFile = Path.Combine(dataPrepFolder, "EditedData.lrn");
                }
                else
                    inputFile = Model.InputFile;

                ProcessStartInfo myProcessStartInfo;
                var somPlotScriptPath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "nextsom_plot_dash.py");
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "nextsom_plot_dash.exe");
                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);


                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true;

                var interactiveFolder = Path.Combine(Model.OutputFolderTimestamped, "Interactive");

                // DEPRECATED
                try
                {
                    System.IO.File.WriteAllText(Path.Combine(Model.OutputFolderTimestamped, "clickData2.txt"), "-1"); //create these files. this should be really handled in a better way, the whole system for checking if the user has clicked a new cluster
                    System.IO.File.WriteAllText(Path.Combine(interactiveFolder, "clickData2.txt"), "-1");
                }
                catch (Exception ex)
                {
                    logger.Error("Selection error in interactive plot, " + ex);
                }

                if (usePyExes)
                    myProcessStartInfo.Arguments = " " + "--outsomfile=" + "\"" + Model.Output_file_somspace + "\"" + " " + "--som_x=" + Model.Som_x + " " + "--som_y=" + Model.Som_y + " " + "--outgeofile=" + "\"" + Model.Output_file_geospace + "\"" + " "  + "--input_file=" + "\"" + Model.InputFile + "\"" + " " + "--interactive_dir=" + "\"" + interactiveFolder + "\"" + " " + "--dir=" + "\"" + Model.OutputFolderTimestamped + "\"" + " " + "--grid_type=" + "\"" + Model.GridShape + "\" " + "--data_type=" + "\"" + Model.DataShape + "\"";
                else
                    myProcessStartInfo.Arguments = "-u" + " " + "\"" + somPlotScriptPath + "\"" + " " + "--outsomfile=" + "\"" + Model.Output_file_somspace + "\"" + " " + "--som_x=" + Model.Som_x + " " + "--som_y=" + Model.Som_y + " "+ "\""+ "--outgeofile=" + Model.Output_file_geospace + "\""+ " " + "--input_file=" + "\"" + Model.InputFile + "\"" + " " + "--interactive_dir="+ "\"" + interactiveFolder +"\""+" "+ "--dir=" + "\"" + Model.OutputFolderTimestamped + "\""  + " " + "--grid_type=" + "\"" + Model.GridShape + "\" "+ "--data_type="+"\""+Model.DataShape+"\"";

             
                myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");
                using (var myProcess = new Process())
                {
                    PythonProcesses.Add(myProcess);
                    myProcess.StartInfo = myProcessStartInfo;
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginOutputReadLine();
                    myProcess.BeginErrorReadLine();
                    myProcess.Close();
                    PythonProcesses.Remove(myProcess);
                };


            });          
        }

        /// <summary>
        /// Run new round of clustering on somoclu result data
        /// </summary>
        public async Task RunClustering(SomModel Model, ObservableCollection<ImageSource> ClusterPlotList, Action<Process> ScriptOutput, Action<Process> ScriptError)
        {
            await Task.Run(() =>
            {
                
               
                var scriptPath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "cluster_wrap.py");
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "cluster_wrap.exe");
                var som = Path.Combine(Model.OutputFolderTimestamped, "som.dictionary");
                ProcessStartInfo myProcessStartInfo;
                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);
                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true; 
                if (usePyExes)
                    myProcessStartInfo.Arguments = "\"" + som + "\"" + " " + Model.KMeans_min + " " + Model.KMeans_max + " " + Model.KMeans_initializations + " " + "\"" + Model.OutputFolderTimestamped + "\"";
                else
                    myProcessStartInfo.Arguments = "\"" + scriptPath + "\"" + " " + som + " " + Model.KMeans_min + " " + Model.KMeans_max + " " + Model.KMeans_initializations + " " + "\"" + Model.OutputFolderTimestamped + "\"";

                myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");

                using (var myProcess = new Process())
                {
                    PythonProcesses.Add(myProcess);
                    myProcess.StartInfo = myProcessStartInfo;
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginErrorReadLine();
                    myProcess.BeginOutputReadLine();
                    myProcess.WaitForExit();
                    myProcess.Close();
                    PythonProcesses.Remove(myProcess);
                };
            });
            
            Model.KMeans_min_last_calculation = Model.KMeans_min;
            Model.KMeans_max_last_calculation = Model.KMeans_max;
            EditRunStatsXml(Path.Combine(Model.OutputFolderTimestamped, "RunStats.xml"), "kmeans_min_last_calculation", Model.KMeans_min_last_calculation.ToString());
            Model.ClusterFilePath = Path.Combine(Model.OutputFolderTimestamped, "cluster.dictionary");
            
        }

        /// <summary>
        /// Run new round of clustering on somoclu result data
        /// </summary>
        public async Task WriteGeotif(SomModel Model, Action<Process> ScriptOutput, Action<Process> ScriptError)
        {
            await Task.Run(() =>
            {


                var scriptPath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "write_geotiff.py");
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "write_geotiff.exe");
                ProcessStartInfo myProcessStartInfo;
                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);
                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true;
                if (usePyExes)
                    myProcessStartInfo.Arguments = "\"" + Model.OutputFolderTimestamped + "\"" + " " + "\""+ Model.OriginalData + "\"";
                else
                    myProcessStartInfo.Arguments = "\"" + scriptPath + "\"" + " " + "\"" + Model.OutputFolderTimestamped + "\"" + " " + "\"" + Model.OriginalData + "\"";

                myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");

                using (var myProcess = new Process())
                {
                    myProcess.StartInfo = myProcessStartInfo;
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginErrorReadLine();
                    myProcess.BeginOutputReadLine();
                    myProcess.WaitForExit();
                    myProcess.Close();
                };
            });


        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="Model"></param>
        /// <param name="ClusterPlotList"></param>
        /// <param name="ScriptOutput"></param>
        /// <param name="ScriptError"></param>
        public async void DrawClusters(SomModel Model, ObservableCollection<ImageSource> ClusterPlotList, Action<Process> ScriptOutput, Action<Process> ScriptError)
        {
            await Task.Run(() =>
            {
                
                var scriptPath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "cluster_draw.py");
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "cluster_draw.exe");
                var cluster_file = Path.Combine(Model.OutputFolderTimestamped, "cluster.dictionary");
                var som = Path.Combine(Model.OutputFolderTimestamped, "som.dictionary");
                ProcessStartInfo myProcessStartInfo;
                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);

                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true;

                if (usePyExes)
                    myProcessStartInfo.Arguments = "\"" + Model.OutputFolderTimestamped + "\"" + " " + "\"" + Model.ClusterFilePath + "\"";
                else
                    myProcessStartInfo.Arguments = "\"" + scriptPath + "\"" + " " + "\"" + Model.OutputFolderTimestamped + "\"" + " " + "\"" + Model.ClusterFilePath + "\"";// "\"" + Model.Output_file_geospace + "\"" + " "

                myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");
                using (var myProcess = new Process())
                {
                    myProcess.StartInfo = myProcessStartInfo;
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginErrorReadLine();
                    myProcess.BeginOutputReadLine();
                    myProcess.WaitForExit();
                    myProcess.Close();
                };


                string ClusterPlotDirectory = Model.OutputFolderTimestamped;
                try
                {
                    //Draw cluster plots
                    App.Current.Dispatcher.Invoke((Action)delegate
                    {
                        ClusterPlotList.Clear();
                    });
                    var d = new DirectoryInfo(ClusterPlotDirectory);
                    var Files = d.GetFiles("*.png");
                    string fullPath;
                    ImageSource imageSrc;
                    foreach (FileInfo file in Files) //Loop through result images: create bitmap, add bitmap to list, delete original file.
                    {
                        if (file.Name == "cluster_plot.png")
                        {
                            fullPath = Path.Combine(ClusterPlotDirectory, file.Name);
                            imageSrc = BitmapFromUri(new Uri(fullPath));
                            App.Current.Dispatcher.Invoke((Action)delegate   //add to list. same thing as previously with the delegate.
                            {
                                ClusterPlotList.Add(imageSrc);
                            });
                            file.Delete();//delete file to reduce clutter.
                        }
                    }

                }
                catch (Exception ex)
                {
                    logger.Error(ex, "Failed to show Cluster plot images");
                }
            });
            
        }

        /// <summary>
        /// Get som results from a spesific folder.
        /// </summary>
        /// <param name="ClusterPlotDirectory"></param>
        /// <param name="ClusterPlotList"></param>
        public void DrawClusterPlots(string ClusterPlotDirectory, ObservableCollection<ImageSource> ClusterPlotList)
        {
            try
            {
                //Draw cluster plots
                App.Current.Dispatcher.Invoke((Action)delegate
                {
                    ClusterPlotList.Clear();
                });
                var d = new DirectoryInfo(ClusterPlotDirectory);
                var Files = d.GetFiles("*.png");
                string fullPath;
                ImageSource imageSrc;
                foreach (FileInfo file in Files) //Loop through result images: create bitmap, add bitmap to list, delete original file.
                {
                    fullPath = Path.Combine(ClusterPlotDirectory, file.Name);
                    imageSrc = BitmapFromUri(new Uri(fullPath));
                    App.Current.Dispatcher.Invoke((Action)delegate   //add to list. same thing as previously with the delegate.
                    {
                        ClusterPlotList.Add(imageSrc);
                    });
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to show Cluster plot images");
            }
        }

        /// <summary>
        /// Save selected clustering result to som calculation result txt files.
        /// </summary>
        public async Task SaveCluster(SomModel Model, int selectedClusterNumber, ObservableCollection<ImageSource> SomImageList, ObservableCollection<ImageSource> GeoSpaceImageList, ObservableCollection<ImageSource> BoxPlotList, ObservableCollection<ImageSource> ScatterPlotList, Action<Process> ScriptOutput, Action<Process> ScriptError)
        {
            await Task.Run(() =>
            {
                //SelectedClusterIndex needs to be converted into selected number of clusters.
                var selectedClusterIndex = selectedClusterNumber - Model.KMeans_min_last_calculation;

                var scaleMinList = new List<double>();
                var scaleMaxList = new List<double>(); //this is not an elegant solution, needs reworking.

                for (int i = 0; i < Model.ColumnDataList.Count(); i++)//in this case exclusion and inclusion is already handed on the data side of things, so take only included cols.
                {
                    if (Model.ColumnDataList[i].IsExcluded == false)
                    {
                        scaleMinList.Add(Model.ColumnDataList[i].NormalizationMin);
                        scaleMaxList.Add(Model.ColumnDataList[i].NormalizationMax);
                    }

                }

                var scriptPath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "cluster_save.py");
                var executablePath = Path.Combine(System.AppDomain.CurrentDomain.BaseDirectory, "scripts", "executables", "cluster_save.exe");
                var cluster_file = Path.Combine(Model.OutputFolderTimestamped, "cluster.dictionary");
                var som = Path.Combine(Model.OutputFolderTimestamped, "som.dictionary");
                Model.InputFile = Path.Combine(Model.OutputFolderTimestamped, "InputData.lrn");
                ProcessStartInfo myProcessStartInfo;
                if (usePyExes)
                    myProcessStartInfo = new ProcessStartInfo(executablePath);
                else
                    myProcessStartInfo = new ProcessStartInfo(pythonPath);

                myProcessStartInfo.UseShellExecute = false;
                myProcessStartInfo.CreateNoWindow = true;
                myProcessStartInfo.RedirectStandardOutput = true;
                myProcessStartInfo.RedirectStandardError = true;

                if (usePyExes)
                    myProcessStartInfo.Arguments = "--n_clusters=" + selectedClusterIndex + " " + "--cluster_file=" + "\"" + cluster_file + "\"" + " " + "--som_dict=" + "\"" + som + "\"" + " " + "--input_file=" + "\"" + Model.InputFile + "\"" + " " + "--outsomfile=" + "\"" + Model.Output_file_somspace + "\"" + " " + "--workingdir=" + "\"" + Model.OutputFolderTimestamped + "\"";
                else
                    myProcessStartInfo.Arguments = "\"" + scriptPath + "\"" + " " + "--n_clusters=" + selectedClusterIndex + " " + "--cluster_file=" + "\"" + cluster_file + "\"" + " " + "--som_dict=" + "\"" + som + "\"" + " " + "--input_file=" + "\"" + Model.InputFile + "\"" + " " + "--outsomfile=" + "\"" + Model.Output_file_somspace + "\"" + " " + "--workingdir=" + "\"" + Model.OutputFolderTimestamped + "\"";

                if (Model.Output_file_geospace.Length > 0)
                    myProcessStartInfo.Arguments += " " + "--outgeofile=" + "\"" + Model.Output_file_geospace + "\"";
                if (Model.InitialCodeBook != "")     //If initial codebook parameter was given, pass it on as a command line variable
                    myProcessStartInfo.Arguments += " " + "--initialcodebook=" + "\"" + Model.InitialCodeBook + "\"";
                if (Model.InputFile.Substring(Model.InputFile.Length - 3) == "tif")
                    myProcessStartInfo.Arguments += " " + "--geotiff_input=" + "\"" + Model.InputFile + "\"";
                if (Model.LabelColumnIndex > -2)
                    myProcessStartInfo.Arguments += " " + "--label=" + "\"" + "true" + "\"";
                if (Model.IsNormalized == true)
                {
                    myProcessStartInfo.Arguments += " " + "--normalized=" + "\"" + "True" + "\"" ;//+"--minN=" +Model.NormalizationMin+ " " +"--maxN="+ Model.NormalizationMax;
                }

                myProcessStartInfo.Arguments = myProcessStartInfo.Arguments.Replace("\\", "/");
                using (var myProcess = new Process())
                {
                    PythonProcesses.Add(myProcess);
                    myProcess.StartInfo = myProcessStartInfo;
                    ScriptOutput(myProcess);
                    ScriptError(myProcess);
                    myProcess.Start();
                    myProcess.BeginErrorReadLine();
                    myProcess.BeginOutputReadLine();
                    myProcess.WaitForExit();
                    myProcess.Close();
                    PythonProcesses.Remove(myProcess);
                };

            });
            
        }
        

        //This is running synchronosly atm. fix or remove altogether. is this necessary?
        public async void AsyncHttpPost(string Uri, string Parameters)
        {
            Task.Run(async () =>
            {
                HttpPost(Uri);//, Parameters);
            });
        }
        /// <summary>
        /// For sending the shutdown message to the interactive plots.
        /// </summary>
        /// <param name="URI"></param>
        public void HttpPost(string URI)// string Parameters, string method = "POST")
        {
            //await Task.Run(async () =>
            //{ HttpWebResponse httpWebResponse
                try
                {
                    System.Net.WebRequest req = System.Net.WebRequest.Create(URI);
                    req.Proxy = WebRequest.DefaultWebProxy;
                    req.Timeout = 10000;
                    req.ContentType = "application/x-www-form-urlencoded";
                    req.Method = "POST";
                    //byte[] bytes; //= System.Text.Encoding.ASCII.GetBytes();
                    //req.ContentLength = bytes.Length;
                    //System.IO.Stream os = req.GetRequestStream();
                    //os.Write(bytes, 0, bytes.Length);
                    



                    using (HttpWebResponse httpWebResponse = (HttpWebResponse)req.GetResponse())
                    {
                    if (httpWebResponse.StatusDescription == "OK")
                    {
                        Debug.Write("Ok");
                        //logger.Trace("Shutting down interactive plot");

                    }
                    //os.Close();
                }         
            }
                catch (Exception e)
                {
                logger.Error(e);
            }
        }

        /// <summary>
        /// Create bitmap from uri
        /// </summary>
        /// <param name="source"></param>
        /// <returns></returns>
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


        //Generic WPF MVVM OnPropertyChanged method. Not sure why this exists though, there is probably some reason.
        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    

        private void ClearFolder(string folderPath)
        {
            DirectoryInfo d;
            FileInfo[] Files;
            try
            {
                d = new DirectoryInfo(folderPath);
                Files = d.GetFiles(); 
                foreach (FileInfo file in Files)
                {
                    file.Delete();
                }
            }
            catch (Exception ex)
            {
                logger.Error(ex, "Failed to clear folder");
            }
        }


        ///Method for editing RunStats.xml document, currently used only for adding q-error after som run? might become deprecated in future versions.
        private void EditRunStatsXml( string xmlPath, string elementName, string elementText)
        {
            XmlDocument doc = new XmlDocument();
            doc.Load(xmlPath);
            XmlNode root = doc.DocumentElement;
            XmlNode myNode = root.SelectSingleNode("descendant::"+ elementName);
            myNode.InnerText = elementText;//
            doc.Save(xmlPath);
        }

        /// <summary>
        /// Method for writing som run parameters and statistics into xml file.
        /// </summary>
        /// <param name="model"></param>
        /// <param name="xmlPath"></param>
        private void WriteRunStatsXml(SomModel model, string xmlPath) 
        {
            XmlWriter xmlWriter = XmlWriter.Create(xmlPath);

            xmlWriter.WriteStartDocument(); 
            xmlWriter.WriteStartElement("som");

            xmlWriter.WriteStartElement("som_x"); //convenience method for writing xml element? xmlwriter, element name and content as parameters? is it necessary?
            xmlWriter.WriteString(model.Som_x.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("som_y");
            xmlWriter.WriteString(model.Som_y.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("spatial");
            xmlWriter.WriteString(model.IsSpatial.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("isSacled");
            xmlWriter.WriteString(model.IsNormalized.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("epochs");
            xmlWriter.WriteString(model.Epochs.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("OutGeoFile");
            xmlWriter.WriteString(model.Output_file_geospace);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("OutSomFile");
            xmlWriter.WriteString(model.Output_file_somspace);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("kmeans_min");
            xmlWriter.WriteString(model.KMeans_min.ToString());
            xmlWriter.WriteEndElement();     

            xmlWriter.WriteStartElement("kmeans_max");
            xmlWriter.WriteString(model.KMeans_max.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("kmeans_init");
            xmlWriter.WriteString(model.KMeans_initializations.ToString()); ;
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("kmeans_min_last_calculation");
            xmlWriter.WriteString(model.KMeans_min_last_calculation.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("kmeans_max_last_calculation");
            xmlWriter.WriteString(model.KMeans_max_last_calculation.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("kmeans");
            xmlWriter.WriteString(model.KMeans);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("neighborhood");
            xmlWriter.WriteString(model.Neighborhood);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("radius0");
            xmlWriter.WriteString(model.InitialNeighborhood.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("radiusN");
            xmlWriter.WriteString(model.FinalNeighborhood.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("maptype");
            xmlWriter.WriteString(model.MapType);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("scalecooling");
            xmlWriter.WriteString(model.KMeans);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("scale0");
            xmlWriter.WriteString(model.TrainingRateFunction.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("scaleN");
            xmlWriter.WriteString(model.TrainingRateFinal.ToString());
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("initialization");
            xmlWriter.WriteString(model.Initialization);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("gridtype");
            xmlWriter.WriteString(model.GridShape);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("dataShape");
            xmlWriter.WriteString(model.DataShape);
            xmlWriter.WriteEndElement();

            string dataType;
            if (model.InputFile.Substring(model.InputFile.Length - 4) == ".tif")
                dataType = "GeoTiff";
            else
                dataType = "CSV";

            xmlWriter.WriteStartElement("dataType");
            xmlWriter.WriteString(dataType);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("output_folder");
            xmlWriter.WriteString(model.OutputFolderTimestamped);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteStartElement("originalData");
            xmlWriter.WriteString(model.InputFile);
            xmlWriter.WriteEndElement();

            xmlWriter.WriteEndElement();

            xmlWriter.WriteEndDocument();
            xmlWriter.Close();
        }
    }
}
