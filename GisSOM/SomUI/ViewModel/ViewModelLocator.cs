/*
  In App.xaml:
  <Application.Resources>
      <vm:ViewModelLocator xmlns:vm="clr-namespace:SomUI"
                           x:Key="Locator" />
  </Application.Resources>
  
  In the View:
  DataContext="{Binding Source={StaticResource Locator}, Path=ViewModelName}"

  You can also use Blend to do all this with the tool's support.
  See http://www.galasoft.ch/mvvm
*/

using CommonServiceLocator;
using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Ioc;
using NLog;
using SomUI.Service;
//using Microsoft.Practices.ServiceLocation;

namespace SomUI.ViewModel
{
    /// <summary>
    /// This class contains static references to all the view models in the
    /// application and provides an entry point for the bindings.
    /// </summary>
    public class ViewModelLocator
    {
        /// <summary>
        /// Initializes a new instance of the ViewModelLocator class.
        /// </summary>
        public ViewModelLocator()
        {
            ServiceLocator.SetLocatorProvider(() => SimpleIoc.Default);
            SimpleIoc.Default.Register<ILogger>(() => LogManager.GetCurrentClassLogger());          
            SimpleIoc.Default.Register<MainViewModel>();
            SimpleIoc.Default.Register<SomViewModel>();
            SimpleIoc.Default.Register<TabViewModel>();
            SimpleIoc.Default.Register<IDialogService, DialogService>();
            var logger = LogManager.GetCurrentClassLogger();
        }

        /// <summary>
        /// getter for MainViewModel
        /// </summary>
        public MainViewModel Main
        {
            get
            {
                return ServiceLocator.Current.GetInstance<MainViewModel>();
            }
        }

        /// <summary>
        /// Getter for SomViewModel, which contains most core functionality for the UI
        /// </summary>
        public SomViewModel SomViewModel
        {
            get
            {
                return ServiceLocator.Current.GetInstance<SomViewModel>();
            }
        }

        /// <summary>
        /// View model for managing Dragablz dragable and tearable tabs
        /// </summary>
        public TabViewModel TabViewModel
        {
            get
            {
                return CommonServiceLocator.ServiceLocator.Current.GetInstance<TabViewModel>();
            }
        }

        /// <summary>
        /// Clear ViewModels, unimplemented at the moment
        /// </summary>
        public static void Cleanup()
        {
            // TODO Clear the ViewModels
        }
    }
}