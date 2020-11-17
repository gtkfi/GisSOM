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
    public class SomModel : ObservableObject
    {
        private string inputFile;
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
        private string interactiveType;
        private string isLogTransformed;
        private string isWinsorized;
        private string winsorMin;
        private string winsorMax;
        private string isExcluded;
        private ImageSource dataHistogram;
        private ImageSource interactiveResultSomPlot;
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

        private bool isSpatial;
        private bool isNormalized;
        private int normalizationMin;
        private int normalizationMax;

        public string NoDataValue
        {
            get { return noDataValue; }
            set { Set<string>(() => this.NoDataValue, ref this.noDataValue, value); }
        }
        public string InitialCodeBook
        {
            get { return initialCodeBook; }
            set
            {
                Set<string>(() => this.InitialCodeBook, ref this.initialCodeBook, value);
            }
        }
        public int EastingColumnIndex
        {
            get { return eastingColumnIndex; }
            set
            {
                Set<int>(() => this.EastingColumnIndex, ref this.eastingColumnIndex, value);
            }
        }

        public int NorthingColumnIndex
        {
            get { return northingColumnIndex; }
            set
            {
                Set<int>(() => this.NorthingColumnIndex, ref this.northingColumnIndex, value);
            }
        }

        public int LabelColumnIndex
        {
            get { return labelColumnIndex; }
            set
            {
                Set<int>(() => this.LabelColumnIndex, ref this.labelColumnIndex, value);
            }
        }

        public string Initialization
        {
            get { return initialization; }
            set
            {
                Set<string>(() => this.Initialization, ref this.initialization, value);
            }
        }

        public string GridShape
        {
            get { return gridShape; }
            set
            {
                Set<string>(() => this.GridShape, ref this.gridShape, value);
            }
        }

        public string TrainingRateFunction
        {
            get { return trainingRateFunction; }
            set
            {
                Set<string>(() => this.TrainingRateFunction, ref this.trainingRateFunction, value);
            }
        }

        public double TrainingRateInitial
        {
            get { return trainingRateInitial; }
            set
            {
                Set<double>(() => this.TrainingRateInitial, ref this.trainingRateInitial, value);
            }
        }

        public double TrainingRateFinal
        {
            get { return trainingRateFinal; }
            set
            {
                Set<double>(() => this.TrainingRateFinal, ref this.trainingRateFinal, value);
            }
        }

        public int InitialNeighborhood
        {
            get { return initialNeighborhood; }
            set
            {
                Set<int>(() => this.InitialNeighborhood, ref this.initialNeighborhood, value);
            }
        }

        public int FinalNeighborhood
        {
            get { return finalNeighborhood; }
            set
            {
                Set<int>(() => this.FinalNeighborhood, ref this.finalNeighborhood, value);
            }
        }

        public string MapType
        {
            get { return maptype; }
            set
            {
                Set<string>(() => this.MapType, ref this.maptype, value);
            }
        }



        public ImageSource InteractiveResultSomPlot
        {
            get { return interactiveResultSomPlot; }
            set
            {
                Set<ImageSource>(() => this.InteractiveResultSomPlot, ref this.interactiveResultSomPlot, value);
            }
        }
        public string Neighborhood
        {
            get { return neighborhood; }
            set
            {
                Set<string>(() => this.Neighborhood, ref this.neighborhood, value);
            }
        }

        public string Output_Folder
        {
            get { return output_folder; }
            set
            {
                Set<string>(() => this.Output_Folder, ref this.output_folder, value);
            }
        }
        public string OutputFolderTimestamped
        {
            get { return outputFolderTimestamped; }
            set
            {
                Set<string>(() => this.OutputFolderTimestamped, ref this.outputFolderTimestamped, value);
            }
        }
        public int KMeans_min
        {
            get { return kmeans_min; }

            set
            {
                Set<int>(() => this.KMeans_min, ref kmeans_min, value);
            }
        }

        public int KMeans_max
        {
            get { return kmeans_max; }

            set
            {
                Set<int>(() => this.KMeans_max, ref kmeans_max, value);
            }
        }
        public int KMeans_min_last_calculation
        {
            get { return kmeans_min_last_calculation; }

            set
            {
                Set<int>(() => this.KMeans_min_last_calculation, ref kmeans_min_last_calculation, value);
            }
        }
        public int KMeans_max_last_calculation
        {
            get { return kmeans_max_last_calculation; }

            set
            {
                Set<int>(() => this.KMeans_max_last_calculation, ref kmeans_max_last_calculation, value);
            }
        }
        public int KMeans_initializations
        {
            get { return kmeans_initializations; }

            set
            {
                Set<int>(() => this.KMeans_initializations, ref kmeans_initializations, value);
            }
        }


        public string KMeans
        {
            get { return kmeans; }

            set
            {
                Set<string>(() => this.KMeans, ref kmeans, value);
            }
        }
        //private List<List<string>> dataPreparationList = new List<List<string>>();

        //public List<List<string>> DataPreparationList
        //{
        //    get { return dataPreparationList; }
        //    set
        //    {
        //        Set<List<List<string>>>(() => this.DataPreparationList, ref dataPreparationList, value);
        //    }
        //}
        public string IsExcluded
        {
            get { return isExcluded; }

            set
            {
                Set<string>(() => this.IsExcluded, ref isExcluded, value);
            }
        }
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

        public string WinsorMin
        {
            get { return winsorMin; }
            set
            {
                Set<string>(() => this.WinsorMin, ref winsorMin, value);
            }
        }
        public string WinsorMax
        {
            get { return winsorMax; }
            set
            {
                Set<string>(() => this.WinsorMax, ref winsorMax, value);
            }
        }
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

        public string Output_file_geospace
        {
            get { return output_file_geospace; }
            set
            {
                Set<string>(() => this.Output_file_geospace, ref output_file_geospace, value);
            }
        }
        public string Output_file_somspace
        {
            get { return output_file_somspace; }
            set
            {
                Set<string>(() => this.Output_file_somspace, ref output_file_somspace, value);
            }
        }
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
        public int Epochs
        {
            get { return epochs; }
            set
            {
                Set<int>(() => this.Epochs, ref epochs, value);
            }

        }

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
        public string InteractiveType
        {
            get { return interactiveType; }
            set
            {
                Set<string>(() => this.InteractiveType, ref interactiveType, value);
            }
        }

        public string ClusterFilePath
        {
            get { return clusterFilePath; }
            set
            {
                Set<string>(() => this.ClusterFilePath, ref clusterFilePath, value);
            }
        }
        public string DataShape
        {
            get { return dataShape; }
            set
            {
                Set<string>(() => this.DataShape, ref dataShape, value);
            }
        }

        public int NormalizationMin
        {
            get { return normalizationMin; }
            set { Set<int>(() => this.NormalizationMin, ref normalizationMin, value); }

        }
        public int NormalizationMax
        {
            get { return normalizationMax; }
            set { Set<int>(() => this.NormalizationMax, ref normalizationMax, value); }

        }
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

    }
    }
