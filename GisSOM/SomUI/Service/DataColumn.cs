using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace SomUI.Service
{
    /// <summary>
    /// Is this whole thing deprecated now after modifying data preparation stage?
    /// </summary>
    public class DataColumn : INotifyPropertyChanged
    {
        private string name;
        private bool isEasting;
        private bool isNorthing;
        private bool isLabel;
        private bool isExcluded;
        private double normalizationMin;
        private double normalizationMax;
        private bool logTransformed;
        private bool isWinsorized;
        private float winsorMin;
        private float winsorMax;
        public event PropertyChangedEventHandler PropertyChanged;
        public DataColumn(string s, bool isEasting, bool isNorthing, bool isLabel, bool isExlcuded, float normalizationMin, float normalizationMax,bool isLogTransformed, bool isWinsorized ,float winsorMin, float winsorMax)
        {
            Name = s;
            IsEasting = isEasting;
            IsNorthing = isNorthing;
            IsLabel = isLabel;
            IsExcluded = isExlcuded;
            NormalizationMin = normalizationMin;
            NormalizationMax = normalizationMax;
            LogTransformed = logTransformed;
            IsWinsorized = isWinsorized;
            WinsorMin = winsorMin;
            WinsorMax = winsorMax;
        }

        public string Name
        {
            get
            {
                return name;
            }
            set
            {
                name = value;
                OnPropertyChanged();
            }
        }
        public bool IsEasting
        {
            get
            {
                return isEasting;
            }
            set
            {
                isEasting = value;
                OnPropertyChanged();
                if (value == true)
                {
                    IsNorthing = false;
                    IsLabel = false;
                }
            }
        }
        public bool IsNorthing
        {
            get
            {
                return isNorthing;
            }
            set
            {
                isNorthing = value;                
                OnPropertyChanged();
                if (value == true)
                {
                    IsEasting = false;
                    IsLabel = false;
                }
            }
        }
        public bool IsLabel
        {
            get
            {
                return isLabel;
            }
            set
            {
                isLabel = value;
                OnPropertyChanged();
                if (value == true)
                {
                    IsEasting = false;
                    IsNorthing = false;
                }
            }
        }
        public bool IsExcluded
        {
            get
            {
                return isExcluded;
            }
            set
            {
                isExcluded = value;
                OnPropertyChanged();
            }
        }
        public double NormalizationMin
        {
            get
            {
                return normalizationMin;
            }
            set
            {
                normalizationMin = value;
                OnPropertyChanged();
            }
        }
        public double NormalizationMax
        {
            get
            {
                return normalizationMax;
            }
            set
            {
                normalizationMax = value;
                OnPropertyChanged();
            }
        }

        public bool LogTransformed
        {
            get
            {
                return logTransformed;
            }
            set
            {
                logTransformed = value;
                OnPropertyChanged();
            }
        }
        public bool IsWinsorized
        {
            get
            {
                return isWinsorized;
            }
            set
            {
                isWinsorized = value;
                OnPropertyChanged();
            }
        }
        public float WinsorMin 
        {
            get
            {
                return winsorMin;
            }
            set
            {
                winsorMin = value;
                OnPropertyChanged();
            }
        }
        public float WinsorMax 
        {
            get
            {
                return winsorMax;
            }
            set
            {
                winsorMax = value;
                OnPropertyChanged();
            }
        }

        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }
}