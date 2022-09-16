using GalaSoft.MvvmLight;
using System.Windows.Controls;
using SomUI.View;
using NLog;
using System.Runtime.CompilerServices;
using System.ComponentModel;
using GalaSoft.MvvmLight.CommandWpf;
using Dragablz;
using CommonServiceLocator;


namespace SomUI.ViewModel
{
    /// <summary>
    /// This class contains properties that the main View can data bind to.
    /// <para>
    /// Use the <strong>mvvminpc</strong> snippet to add bindable properties to this ViewModel.
    /// </para>
    /// <para>
    /// You can also use Blend to data bind with the tool's support.
    /// </para>
    /// <para>
    /// See http://www.galasoft.ch/mvvm
    /// </para>
    /// </summary>
    public class MainViewModel : ViewModelBase, INotifyPropertyChanged
    {
        /// <summary>
        /// Initializes a new instance of the MainViewModel class.
        /// </summary>
        /// 
        //private readonly ILogger logger;       
        //private readonly IDialogService dialogService;
        private readonly ILogger logger;
        public event PropertyChangedEventHandler PropertyChanged;
        private UserControl activeView;
        private UserControl somInputView;
        private UserControl somParameterView;
        private UserControl somResultView;
        private UserControl dataPreparationView;
        private string dialogContentSource;
        public RelayCommand GoToSomParameterView { get; set; }
        public RelayCommand GoToResultView { get; set; }
        public RelayCommand GoToDataPreparationView { get; set; }
        public RelayCommand GoToSomInputView { get; set; }
        private readonly IInterTabClient _interTabClient;
        public MainViewModel()
        {
            Initialize();
            this.logger=NLog.LogManager.GetCurrentClassLogger();
            GoToSomParameterView =new RelayCommand(ChangeToSomParameterView, CanChangeView);
            GoToResultView = new RelayCommand(ChangeToSomResultView, CanChangeView);
            GoToDataPreparationView = new RelayCommand(ChangeToDataPreparationView, CanChangeView);
            GoToSomInputView = new RelayCommand(ChangeToSomInputView, CanChangeView);
            _interTabClient = new MyInterTabClient();
            void Initialize()
            {
                somInputView = new SomInputView();    
                somParameterView = new SomParameterView(); 
                somResultView = new SomResultMenuView();
                dataPreparationView = new DataPreparationView();
                activeView = dataPreparationView;
            }
        }

        /// <summary>
        /// The view that's currently active in the UI
        /// </summary>
        public UserControl ActiveView
        {
            get { return activeView; }
            set
            {
                if (value == activeView) return;
                activeView = value;
                OnPropertyChanged();
            }
        }
        /// <summary>
        /// Whether user is allowed to change view, not yet implemented
        /// </summary>
        /// <returns></returns>
        private bool CanChangeView()
        {
            return true;//TODO: implement this.
        }
       private void ChangeToSomInputView()
        {
            ActiveView = somInputView;
        }
        /// <summary>
        /// Change active UI view to Som Parameter View
        /// </summary>
        public void ChangeToSomParameterView()
        {
            ActiveView = somParameterView;
        }

        /// <summary>
        /// Change active UI view to Som Result View
        /// </summary>
        public void ChangeToSomResultView()
        {
            ActiveView = somResultView;
        }

        /// <summary>
        /// Change active UI view to Data Preparation View
        /// </summary>
        private void ChangeToDataPreparationView()
        {
            if(!ServiceLocator.Current.GetInstance<SomViewModel>().IsBusy)
                ActiveView = dataPreparationView;
        }
        protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
        {
            PropertyChangedEventHandler handler = PropertyChanged;
            if (handler != null) handler(this, new PropertyChangedEventArgs(propertyName));
        }

        /// <summary>
        /// InterTabClient for Dragablz tearable and dockable tabs
        /// </summary>
        public IInterTabClient InterTabClient
        {
            get { return _interTabClient; }
        }

        public string DialogContentSource
        {
            get
            {
                return dialogContentSource;
            }
            set
            {
                if (dialogContentSource == value) return;
                dialogContentSource = value.ToString();
                RaisePropertyChanged("DialogContentSource");
            }
        }
    }
}