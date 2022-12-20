using System.Threading.Tasks;
using System.Windows.Controls;
using System.Windows.Data;
using Microsoft.Web.WebView2.Core;
using Microsoft.Web.WebView2.Wpf;

namespace SomUI.View
{
    /// <summary>
    /// Interaction logic for DataPreparation.xaml
    /// </summary>
    public partial class DataPreparationView : UserControl
    {
        /// <summary>
        /// Initalizes a new instance of DataPreparationView class
        /// </summary>
        public DataPreparationView()
        {
            
            InitializeComponent();
            //InitializeWebView2(System.IO.Path.GetTempPath());
        }


        private void ToolTip_SourceUpdated(object sender, DataTransferEventArgs e)
        {

            if (this.webView.IsLoaded)
            {
                this.webView.Reload();
            }


        }

        //Initializew WebView2 component with tempfolder for writing cache
        //private void InitializeWebView2(string userDataFolder)
        //{
        //    this.webView.CreationProperties = new CoreWebView2CreationProperties()
        //    {
        //        UserDataFolder = userDataFolder
        //    };
        //    webView.EnsureCoreWebView2Async();
        //}
    }
}
