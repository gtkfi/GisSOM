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
    /// Interaction logic for SomParameterView.xaml
    /// </summary>
    public partial class SomParameterView : UserControl
    {
        public SomParameterView()
        {
            InitializeComponent();
        }

        private void ComboBoxItem_Selected(object sender, RoutedEventArgs e)
        {

        }
        private void TextBlock_SourceUpdated(object sender, DataTransferEventArgs e)
        {
            //TextBlock TB = (TextBlock)sender; //Cast sender as textbox (which it is)
            //ScrollViewer scrollViewer = (ScrollViewer)TB.Parent; //get parent of the texbox and cast it to scrollviewer(which it is)
            //scrollViewer.ScrollToBottom(); //call the ScrollToBottomEvent
        }
    }
}
