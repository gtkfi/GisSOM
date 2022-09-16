using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading.Tasks;

namespace SomUI.Service
{
    ///
    public class BoolStringHelper : INotifyPropertyChanged
    {
        private string name;
        public bool isSelected;
        public event PropertyChangedEventHandler PropertyChanged;
        public BoolStringHelper(string s, bool b)
        {
            Name = s;
            IsSelected = b;
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
            } }
        public bool IsSelected 
        { 
            get 
            { 
                return isSelected; 
            }
            set 
            {
                isSelected = value;
                OnPropertyChanged();
            } 
        }
        protected void OnPropertyChanged([CallerMemberName] string name = null)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }
}
