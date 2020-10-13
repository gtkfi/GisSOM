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
    /// Interaction logic for InteractiveResultsView.xaml
    /// </summary>
    public partial class InteractiveResultsView : UserControl
    {
        public InteractiveResultsView()
        {
            InitializeComponent();
        }


        private void ToolTip_SourceUpdated(object sender, DataTransferEventArgs e)
        {
            //var TB = (TextBlock)sender; //Cast sender as textbox (which it is)
            try { 
            var wb = (WebBrowser)sender; //exc
            wb.Refresh(true);
            }
            catch (Exception)
            {

            }
            //var scrollViewer = (ScrollViewer)TB.Parent; //get parent of the texbox and cast it to scrollviewer(which it is)
            //scrollViewer.ScrollToBottom(); //call the ScrollToBottomEvent
        }
    }
}
