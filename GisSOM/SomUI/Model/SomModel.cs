using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;
using GalaSoft.MvvmLight;
using SomUI.Service;

namespace SomUI.Model
{
    /// <summary>
    /// Initialize new instance of SomModel
    /// </summary>
    public class SomModel : ObservableObject
    {
        private string inputFile;
        private string originalData;
        private string somResultsFolder;
        private string output_file_geospace;
        private string output_file_somspace;
        private string output_folder;
        private string outputFolderTimestamped;
        private int som_x;
        private int som_y;
        private int epochs;
        private List<string> inrasterlist = new List<string> { "" };
        private ObservableCollection<BoolStringHelper> scatterPlotList = new ObservableCollection<BoolStringHelper> { };
        private ObservableCollection<BoolStringHelper> boxPlotList = new ObservableCollection<BoolStringHelper> { };
        private ObservableCollection<DataColumn> columnDataList = new ObservableCollection<DataColumn> { };
        private ObservableCollection<string> interactiveResultColumnList = new ObservableCollection<string> { };
        private string interactiveType;
        private string isLogTransformed;
        private string isWinsorized;
        private string winsorMin;
        private string winsorMax;
        private string isExcluded;
        private ImageSource dataHistogram;
        private ImageSource interactiveResultSomPlot;
        private ImageSource newLabelPlot;
        private ImageSource newLabelLegend;
        private int eastingColumnIndex;
        private int northingColumnIndex;
        private int labelColumnIndex;
        private string clusterFilePath;
        private string initialCodeBook;
        private string kmeans;
        private int kmeans_min;
        private int kmeans_min_last_calculation;
        private int kmeans_max_last_calculation;
        private int kmeans_max;
        private int kmeans_initializations;
        private string noDataValue;
        private string neighborhood;
        private string maptype; //toroid or sheet
        private int initialNeighborhood;
        private int finalNeighborhood;
        private string trainingRateFunction;
        private double trainingRateInitial;
        private double trainingRateFinal;
        private string dataShape;
        private string gridShape; //squqre or hexa
        private string initialization;
        private string runId;
        private bool isSpatial;
        private bool isNormalized;
        private int normalizationMin;
        private int normalizationMax;
        private int selectedInteractiveColumn;
        private string newLabelData;

        /// <summary>
        /// Numeric value used to mark NaN values in input data. This is often something like -9999, or a significantly larger negative number.
        /// </summary>
        public string NoDataValue
        {
            get { return noDataValue; }
            set { Set<string>(() => this.NoDataValue, ref this.noDataValue, value); }
        }

        /// <summary>
        /// Optional parameter for providing an initial codebook used as basis for som calculation
        /// </summary>
        public string InitialCodeBook
        {
            get { return initialCodeBook; }
            set
            {
                Set<string>(() => this.InitialCodeBook, ref this.initialCodeBook, value);
            }
        }

        /// <summary>
        /// Index of X coordinate column in input data
        /// </summary>
        public int EastingColumnIndex
        {
            get { return eastingColumnIndex; }
            set
            {
                Set<int>(() => this.EastingColumnIndex, ref this.eastingColumnIndex, value);
            }
        }

        /// <summary>
        /// Index of Y coordinate column input data
        /// </summary>
        public int NorthingColumnIndex
        {
            get { return northingColumnIndex; }
            set
            {
                Set<int>(() => this.NorthingColumnIndex, ref this.northingColumnIndex, value);
            }
        }

        /// <summary>
        /// Index of label column input data
        /// </summary>
        public int LabelColumnIndex
        {
            get { return labelColumnIndex; }
            set
            {
                Set<int>(() => this.LabelColumnIndex, ref this.labelColumnIndex, value);
            }
        }

        /// <summary>
        /// Initialization for som map, "random" or "pca"
        /// </summary>
        public string Initialization
        {
            get { return initialization; }
            set
            {
                Set<string>(() => this.Initialization, ref this.initialization, value);
            }
        }

        /// <summary>
        /// Shape of som grid (square or hexagonal. square is a regular square where diagonals are not neighbours, hexa is a honeycomb where each node has 6 neighbors.
        /// </summary>
        public string GridShape
        {
            get { return gridShape; }
            set
            {
                Set<string>(() => this.GridShape, ref this.gridShape, value);
            }
        }

        /// <summary>
        /// Trainingrate function for som training, "linear" or "exponential"
        /// </summary>
        public string TrainingRateFunction
        {
            get { return trainingRateFunction; }
            set
            {
                Set<string>(() => this.TrainingRateFunction, ref this.trainingRateFunction, value);
            }
        }

        /// <summary>
        /// Initial learning rate
        /// </summary>
        public double TrainingRateInitial
        {
            get { return trainingRateInitial; }
            set
            {
                Set<double>(() => this.TrainingRateInitial, ref this.trainingRateInitial, value);
            }
        }

        /// <summary>
        /// Final learning rate for som training
        /// </summary>
        public double TrainingRateFinal
        {
            get { return trainingRateFinal; }
            set
            {
                Set<double>(() => this.TrainingRateFinal, ref this.trainingRateFinal, value);
            }
        }

        /// <summary>
        /// Initial neighborhood size
        /// </summary>
        public int InitialNeighborhood
        {
            get { return initialNeighborhood; }
            set
            {
                Set<int>(() => this.InitialNeighborhood, ref this.initialNeighborhood, value);
            }
        }

        /// <summary>
        /// Final neighborhood size
        /// </summary>
        public int FinalNeighborhood
        {
            get { return finalNeighborhood; }
            set
            {
                Set<int>(() => this.FinalNeighborhood, ref this.finalNeighborhood, value);
            }
        }

        /// <summary>
        /// Map type for som, "toroid" or "planar"
        /// </summary>
        public string MapType
        {
            get { return maptype; }
            set
            {
                Set<string>(() => this.MapType, ref this.maptype, value);
            }
        }


        /// <summary>
        /// Interactive result plot image
        /// </summary>
        public ImageSource InteractiveResultSomPlot
        {
            get { return interactiveResultSomPlot; }
            set
            {
                Set<ImageSource>(() => this.InteractiveResultSomPlot, ref this.interactiveResultSomPlot, value);
            }
        }
        /// <summary>
        /// Neighbourhood function used for som training, values "gaussian" or "bubble"
        /// </summary>
        public string Neighborhood
        {
            get { return neighborhood; }
            set
            {
                Set<string>(() => this.Neighborhood, ref this.neighborhood, value);
            }
        }

        /// <summary>
        /// Output folder for the software
        /// </summary>
        public string Output_Folder
        {
            get { return output_folder; }
            set
            {
                Set<string>(() => this.Output_Folder, ref this.output_folder, value);
            }
        }

        /// <summary>
        /// Output folder for a specific som run
        /// </summary>
        public string OutputFolderTimestamped
        {
            get { return outputFolderTimestamped; }
            set
            {
                Set<string>(() => this.OutputFolderTimestamped, ref this.outputFolderTimestamped, value);
            }
        }

        /// <summary>
        /// Minimum number of clusters for k-means clustering
        /// </summary>
        public int KMeans_min
        {
            get { return kmeans_min; }

            set
            {
                Set<int>(() => this.KMeans_min, ref kmeans_min, value);
            }
        }

        /// <summary>
        /// Maximum number of clusters for k-means clustering
        /// </summary>
        public int KMeans_max
        {
            get { return kmeans_max; }

            set
            {
                Set<int>(() => this.KMeans_max, ref kmeans_max, value);
            }
        }

        /// <summary>
        /// Minimum number of clusters for previous k-means calculation
        /// </summary>
        public int KMeans_min_last_calculation
        {
            get { return kmeans_min_last_calculation; }

            set
            {
                Set<int>(() => this.KMeans_min_last_calculation, ref kmeans_min_last_calculation, value);
            }
        }

        /// <summary>
        /// Maximum number of clusters for previous k-means calculation
        /// </summary>
        public int KMeans_max_last_calculation
        {
            get { return kmeans_max_last_calculation; }

            set
            {
                Set<int>(() => this.KMeans_max_last_calculation, ref kmeans_max_last_calculation, value);
            }
        }

        /// <summary>
        /// Number of initialiazations for each number of clusters
        /// </summary>
        public int KMeans_initializations
        {
            get { return kmeans_initializations; }

            set
            {
                Set<int>(() => this.KMeans_initializations, ref kmeans_initializations, value);
            }
        }

        /// <summary>
        /// Whether Kmeans calculation is ran or not
        /// </summary>
        public string KMeans
        {
            get { return kmeans; }

            set
            {
                Set<string>(() => this.KMeans, ref kmeans, value);
            }
        }

        /// <summary>
        /// Whether selected data column is excluded or not
        /// </summary>
        public string IsExcluded
        {
            get { return isExcluded; }

            set
            {
                Set<string>(() => this.IsExcluded, ref isExcluded, value);
            }
        }

        /// <summary>
        /// Histogram for data column value distribution, used in Data Preparation stage for input data columns.
        /// </summary>
        public ImageSource DataHistogram
        {
            get
            {
                return dataHistogram;
            }
            set
            {
                Set<ImageSource>(() => this.DataHistogram, ref dataHistogram, value);
            }
        }

        /// <summary>
        /// Resulting image plot after adding new label data to already calculated som
        /// </summary>
        public ImageSource NewLabelPlot
        {
            get
            {
                return newLabelPlot;
            }
            set
            {
                Set<ImageSource>(() => this.NewLabelPlot, ref newLabelPlot, value);
            }
        }

        /// <summary>
        /// Resulting image legend after adding new label data to already calculated som
        /// </summary>
        public ImageSource NewLabelLegend
        {
            get
            {
                return newLabelLegend;
            }
            set
            {
                Set<ImageSource>(() => this.NewLabelLegend, ref newLabelLegend, value);
            }
        }

        /// <summary>
        /// Lower used for winsorizing
        /// </summary>
        public string WinsorMin
        {
            get { return winsorMin; }
            set
            {
                Set<string>(() => this.WinsorMin, ref winsorMin, value);
            }
        }

        /// <summary>
        /// Upper limit used for winsorizing
        /// </summary>
        public string WinsorMax
        {
            get { return winsorMax; }
            set
            {
                Set<string>(() => this.WinsorMax, ref winsorMax, value);
            }
        }
        
        /// <summary>
        /// Whether data is log transformed or not
        /// </summary>
        public string IsLogTransformed
        {
            get
            {
                return isLogTransformed;
            }
            set
            {
                Set<string>(() => this.IsLogTransformed, ref isLogTransformed, value);
                if (value == "True")
                {
                    IsWinsorized = "False";
                }
            }
        }

        /// <summary>
        /// Whether data is spatial or not.
        /// </summary>
        public bool IsSpatial
        {
            get
            {
                return isSpatial;
            }
            set
            {
                Set<bool>(() => this.IsSpatial, ref isSpatial, value);
            }
        }

        /// <summary>
        /// Whether data is scaled or not.
        /// </summary>
        public bool IsNormalized
        {
            get
            {
                return isNormalized;
            }
            set
            {
                Set<bool>(() => this.IsNormalized, ref isNormalized, value);
            }
        }
        /// <summary>
        /// Minimum value used for scaling data
        /// </summary>
        public int NormalizationMin
        {
            get { return normalizationMin; }
            set { Set<int>(() => this.NormalizationMin, ref normalizationMin, value); }

        }

        /// <summary>
        /// Maximum value used for scaling data
        /// </summary>
        public int NormalizationMax
        {
            get { return normalizationMax; }
            set { Set<int>(() => this.NormalizationMax, ref normalizationMax, value); }

        }
        /// <summary>
        /// Whether data is winsorized or not.
        /// </summary>
        public string IsWinsorized
        {
            get
            {
                return isWinsorized;
            }
            set
            {
                Set<string>(() => this.IsWinsorized, ref isWinsorized, value);
                if (value == "True")
                {
                    IsLogTransformed = "False";
                }

            }
        }

        /// <summary>
        /// Path to input file used in som calculation
        /// </summary>
        public string InputFile
        {
            get
            {
                return inputFile;
            }
            set
            {
                Set<string>(() => this.InputFile, ref inputFile, value);

            }
        }
        /// <summary>
        /// Path to original input data that has not been modified in data preparation stage
        /// </summary>
        public string OriginalData
        {
            get
            {
                return originalData;
            }
            set
            {
                Set<string>(() => this.OriginalData, ref originalData, value);

            }
        }

        /// <summary>
        /// Results folder for som calculation and plots
        /// </summary>
        public string SomResultsFolder
        {
            get
            {
                return somResultsFolder;
            }
            set
            {
                Set<string>(() => this.SomResultsFolder, ref somResultsFolder, value);
            }
        }

        /// <summary>
        /// Output file for som calculation geospace results
        /// </summary>
        public string Output_file_geospace
        {
            get { return output_file_geospace; }
            set
            {
                Set<string>(() => this.Output_file_geospace, ref output_file_geospace, value);
            }
        }

        /// <summary>
        /// Output file for som calculation somspace results
        /// </summary>
        public string Output_file_somspace
        {
            get { return output_file_somspace; }
            set
            {
                Set<string>(() => this.Output_file_somspace, ref output_file_somspace, value);
            }
        }

        /// <summary>
        /// Som X dimension
        /// </summary>
        public int Som_x
        {
            get { return som_x; }
            set
            {
                if (value < 5)
                    value = 5;
                Set<int>(() => this.Som_x, ref som_x, value);
            }
        }

        /// <summary>
        /// Som Y dimension
        /// </summary>
        public int Som_y
        {
            get { return som_y; }
            set
            {
                if (value < 5)
                    value = 5;
                Set<int>(() => this.Som_y, ref som_y, value);
            }
        }

        /// <summary>
        /// Number of epochs used in som training
        /// </summary>
        public int Epochs
        {
            get { return epochs; }
            set
            {
                Set<int>(() => this.Epochs, ref epochs, value);
            }

        }

        /// <summary>
        /// List of input rasters
        /// </summary>
        public List<string> InRasterList
        {
            get
            {
                return inrasterlist;
            }
            set
            {
                Set<List<string>>(() => this.InRasterList, ref inrasterlist, value);
            }
        }

        /// <summary>
        /// Type of interactive plot selection: cluster or som. DEPRECATED?
        /// </summary>
        public string InteractiveType
        {
            get { return interactiveType; }
            set
            {
                Set<string>(() => this.InteractiveType, ref interactiveType, value);
            }
        }

        /// <summary>
        /// Path to kmeans clustering output file
        /// </summary>
        public string ClusterFilePath
        {
            get { return clusterFilePath; }
            set
            {
                Set<string>(() => this.ClusterFilePath, ref clusterFilePath, value);
            }
        }

        /// <summary>
        /// Shape of input data in case of CSV input: Grid, or Scatter.
        /// </summary>
        public string DataShape
        {
            get { return dataShape; }
            set
            {
                Set<string>(() => this.DataShape, ref dataShape, value);
            }
        }

        /// <summary>
        /// List of output scatter plots
        /// </summary>
        public ObservableCollection<BoolStringHelper> ScatterPlotList
        {
            get
            {
                return scatterPlotList;
            }
            set
            {
                Set(() => ScatterPlotList, ref scatterPlotList, value);
            }
        }
        /// <summary>
        /// List of output box plots
        /// </summary>
        public ObservableCollection<BoolStringHelper> BoxPlotList
        {
            get
            {
                return boxPlotList;
            }
            set
            {
                Set(() => BoxPlotList, ref boxPlotList, value);
            }
        }
        public ObservableCollection<DataColumn> ColumnDataList
        {
            get
            {
                return columnDataList;
            }
            set
            {
                Set(() => ColumnDataList, ref columnDataList, value);
            }
        }

        public string RunId
        {
            get { return runId; }
            set
            {
                Set<string>(() => this.RunId, ref runId, value);
            }
        }

        /// <summary>
        /// Path to input file for adding new label data to an existing som result
        /// </summary>
        public string NewLabelData
        {
            get { return newLabelData; }
            set
            {
                Set<string>(() => this.NewLabelData, ref newLabelData, value);
            }
        }

        /// <summary>
        /// Index of selected column for interactive plot. DEPRECATED?
        /// </summary>
        public int SelectedInteractiveColumn
        {
            get { return selectedInteractiveColumn; }
            set
            {
                Set<int>(() => this.SelectedInteractiveColumn, ref selectedInteractiveColumn, value);
            }
        }

        /// <summary>
        /// DEPRECATED?
        /// </summary>
        public ObservableCollection<string> InteractiveResultColumnList
        {
            get
            {
                return interactiveResultColumnList;
            }
            set
            {
                Set (() => InteractiveResultColumnList, ref interactiveResultColumnList, value);
            }
        }

    }
    }
