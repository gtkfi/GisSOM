using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace SomUI.View
{
    /// <summary>
    /// Interaction logic for DataPreparation.xaml
    /// </summary>
    public partial class DataPreparationView : UserControl
    {
        /// <summary>
        /// Initalizes a new instance of ´DataPreparationView class
        /// </summary>
        public DataPreparationView()
        {
            InitializeComponent();
        }


        private void ToolTip_SourceUpdated(object sender, DataTransferEventArgs e)
        {

            if (this.webView.IsLoaded)
            {
                this.webView.Reload();
            }


        }
    }
}
