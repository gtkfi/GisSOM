using Dragablz;
using MahApps.Metro.Controls;
using SomUI.View;
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Windows;

namespace SomUI.ViewModel
{
    class MyInterTabClient : IInterTabClient
    {
        private TabablzControl tControl;

        /// <summary>
        /// Implementation of InterTabClient.
        /// To open dragged tabs in a different window class than they originated from.
        /// </summary>
        /// <param name="interTabClient">InterTabClient</param>
        /// <param name="partition">Partition</param>
        /// <param name="source">Source</param>
        /// <returns></returns>
        public INewTabHost<Window> GetNewHost(IInterTabClient interTabClient, object partition, TabablzControl source)
        {
            var view = new TabWindow();
            view.Owner = App.Current.MainWindow;
            TControl = source;
            view.Closing += new CancelEventHandler(CloseWindow);
            return new NewTabHost<Window>(view, view.TabablzControl); //TabablzControl is a names control in the XAML
        }

        /// <summary>
        /// Tabablz control of the speific tab.
        /// </summary>
        private TabablzControl TControl
        {
            get
            {
                return tControl;
            }
            set
            {
                tControl = value;
            }
        }

        /// <summary>
        /// Closes the spesific tab window and send tabs back into correct places.
        /// </summary>
        /// <param name="sender">TabWindow object.</param>
        /// <param name="e">Event</param>
        private void CloseWindow(Object sender, CancelEventArgs e)
        {
            try
            {
                TabWindow tab = (TabWindow)sender;
                if (tab.TabablzControl.Items.Count != 0)
                {
                    // Items have to be moved in to separate collection to remove references to parents.
                    ObservableCollection<MetroTabItem> items = new ObservableCollection<MetroTabItem>();
                    foreach (MetroTabItem item in tab.TabablzControl.Items)
                    {
                        items.Add(item);
                    }
                    foreach (MetroTabItem item in items)
                    {
                        var parent = (TabablzControl)item.Parent;
                        if (parent != null)
                        {
                            parent.RemoveFromSource(item);
                        }
                        TControl.RemoveFromSource(item);
                        TControl.AddToSource(item);
                    }
                }
                // Select one of the tabs;  
                MetroTabItem metroItem = (MetroTabItem)TControl.Items.GetItemAt(0);
                metroItem.IsSelected = true;
            }
            catch
            {

            }
        }

        /// <summary>
        /// Handles the tab closing.
        /// </summary>
        /// <param name="tabControl">Tab's tabcontrol.</param>
        /// <param name="window">Tab's window.</param>
        /// <returns>Tab emptied response.</returns>
        public TabEmptiedResponse TabEmptiedHandler(TabablzControl tabControl, Window window)
        {
            if (window is TabWindow)
                return TabEmptiedResponse.CloseWindowOrLayoutBranch;
            return TabEmptiedResponse.DoNothing;
        }
    }
}
