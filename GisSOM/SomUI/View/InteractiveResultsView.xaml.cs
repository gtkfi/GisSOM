using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Text;
using System.Threading;
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
using CefSharp;
using CefSharp.Wpf;


namespace SomUI.View
{
    /// <summary>
    /// Interaction logic for InteractiveResultsView.xaml
    /// </summary>
    public partial class InteractiveResultsView : UserControl
    {
        /// <summary>
        /// Initialize a new instance of InteractiveResultsView
        /// </summary>
        public InteractiveResultsView()
        {
            InitializeComponent();          
            this.Browser.PreviewMouseWheel += CefBrowserPreviewMouseWheel;
            this.Browser.KeyUp += CefBrowserKeyUp;                    
        }

        private async void Stop(object sender, RoutedEventArgs e)
        {

            await Task.Run(async () =>
            {
                string s = HttpPost("http://localhost:8050/shutdown", "closing app");
                if (s == null)
                {
                    s = HttpPost("http://localhost:8050/shutdown", "closing app");
                }
                else
                {
                    App.Current.Dispatcher.Invoke((Action)delegate
                  {
                      this.Browser.Visibility = Visibility.Hidden;
                  });
                }

            });
           
        }
        private void RefreshBrowser(object sender, RoutedEventArgs e) {
            if (this.Browser.IsBrowserInitialized && this.Browser.IsLoaded)
            {

                Cef.GetGlobalCookieManager().DeleteCookies("", "");
                CefSharp.WebBrowserExtensions.Reload(this.Browser, true);
            }
        }

        /// <summary>
        /// For whatever reason single refreshes don't seem to do the trick.
        /// </summary>
        private async void DumbMultipleRefresh()
        {
            await Task.Run(() =>
            {
                for (int i = 0; i < 10; i++)
                {
                    Cef.GetGlobalCookieManager().DeleteCookies("", "");
                    CefSharp.WebBrowserExtensions.Reload(this.Browser, true);
                    Thread.Sleep(500);
                }
            });
            }
        private string HttpPost(string URI, string Parameters)
        {
            try
            {
                System.Net.WebRequest req = System.Net.WebRequest.Create(URI);
                req.Proxy = WebRequest.DefaultWebProxy;
                req.Timeout = 10000;
                req.ContentType = "application/x-www-form-urlencoded";
                req.Method = "POST";
                byte[] bytes = System.Text.Encoding.ASCII.GetBytes(Parameters);
                req.ContentLength = bytes.Length;
                System.IO.Stream os = req.GetRequestStream();
                os.Write(bytes, 0, bytes.Length);
                os.Close();
                //WebResponse resp = req.GetResponse();

                using (HttpWebResponse httpWebResponse = (HttpWebResponse)req.GetResponse())
                {
                    if (httpWebResponse.StatusDescription == "OK")
                    {
                        Cef.GetGlobalCookieManager().DeleteCookies("", "");
                        CefSharp.WebBrowserExtensions.Reload(this.Browser, true);
                        httpWebResponse.Close();
                        return "OK";

                    }
                    if (httpWebResponse == null) return null;
                    System.IO.StreamReader sr = new System.IO.StreamReader(httpWebResponse.GetResponseStream());
                    httpWebResponse.Close();
                    return null;
                }
            }
            catch (Exception)
            {
                Cef.GetGlobalCookieManager().DeleteCookies("", "");
                CefSharp.WebBrowserExtensions.Reload(this.Browser, true);
                return null;
            }
        }


        //Thread.Sleep(1000);
        //this.Browser.WebBrowser.Load("http://localhost:8050/");
        //(true);
        //}

        //chromimum version. Spaghetti that enables VM to "command" web browser to refresh.
        private void ToolTip_SourceUpdated(object sender, DataTransferEventArgs e)
        {

            if (this.Browser.IsBrowserInitialized)
            {
                Cef.GetGlobalCookieManager().DeleteCookies("", "");
                CefSharp.WebBrowserExtensions.Reload(this.Browser, true);
                this.Browser.Visibility = Visibility.Visible;
                DumbMultipleRefresh();
                //App.Current.Dispatcher.Invoke((Action)delegate
                //{
                //    this.Browser.Load("http://localhost:8050/");
                //});

                //this.Browser.Visibility = Visibility.Visible;
            }
            

        }
        private void ZoomOut(object sender, RoutedEventArgs e)
        {
            this.Browser.ZoomOutCommand.Execute(null);
        }
        private void ZoomIn(object sender, RoutedEventArgs e)
        {
            this.Browser.ZoomInCommand.Execute(null);
        }

        private void CefBrowserPreviewMouseWheel(object sender, MouseWheelEventArgs e)
        {

            if (Keyboard.Modifiers != ModifierKeys.Control)
                return;

            if (e.Delta > 0)
                this.Browser.ZoomInCommand.Execute(null);
            else
                this.Browser.ZoomOutCommand.Execute(null);
            e.Handled = true;
        }

        private void CefBrowserKeyUp(object sender, KeyEventArgs e)
        {

            if (Keyboard.Modifiers != ModifierKeys.Control)
                return;

            if (e.Key == Key.Add)
                this.Browser.ZoomInCommand.Execute(null);
            if (e.Key == Key.Subtract)
                this.Browser.ZoomOutCommand.Execute(null);
            if (e.Key == Key.NumPad0)
                this.Browser.ZoomLevel = 0;
        }
    }
}
