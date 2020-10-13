using System;
using System.Collections.Generic;
using System.ComponentModel;
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
using CommonServiceLocator;
using MahApps.Metro.Controls;
using GalaSoft.MvvmLight.Ioc;
using SomUI.ViewModel;
using System.Threading;
using SomUI.View;
using System.Net.Http;
using System.Net;

namespace SomUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : MetroWindow
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        void MainWindow_Closing(object sender, CancelEventArgs e)
        {
            string response = HttpPost("http://localhost:8050/shutdown", "closing app");//response is not used here
        }



        /// <summary>
        /// Method for sending Http post request, used to send shutdown message to dash app (interactive plot)
        /// </summary>
        /// <param name="URI"></param>
        /// <param name="Parameters"></param>
        /// <returns></returns>
        public static string HttpPost(string URI, string Parameters)
        {
            try { 
            System.Net.WebRequest req = System.Net.WebRequest.Create(URI);
            req.Proxy = WebRequest.DefaultWebProxy;
            //Add these, as we're doing a POST
            req.ContentType = "application/x-www-form-urlencoded";
            req.Method = "POST";
            //We need to count how many bytes we're sending. Params should be name=value&
            byte[] bytes = System.Text.Encoding.ASCII.GetBytes(Parameters);
            req.ContentLength = bytes.Length;
            System.IO.Stream os = req.GetRequestStream();
            os.Write(bytes, 0, bytes.Length); //Push it out there
            os.Close();
            System.Net.WebResponse resp = req.GetResponse();
            if (resp == null) return null;
            System.IO.StreamReader sr = new System.IO.StreamReader(resp.GetResponseStream());
            resp.Close();
            return null;
            }
            catch(Exception)
            {               
                return null;
            }
        }

        //private void ScrollDown(object sender, RoutedEventArgs e)
        //{
        //    var testi = this;
        //    ScrollViewer scrollViewer=(ScrollViewer)this.FindName("PythonLogViewer");
        //    scrollViewer.ScrollToBottom();
        //}

        private void TextBlock_SourceUpdated(object sender, DataTransferEventArgs e)
        {
            var TB = (TextBlock)sender; //Cast sender as textbox (which it is)
            var scrollViewer = (ScrollViewer)TB.Parent; //get parent of the texbox and cast it to scrollviewer(which it is)
            scrollViewer.ScrollToBottom(); //call the ScrollToBottomEvent
        }
    }
}
