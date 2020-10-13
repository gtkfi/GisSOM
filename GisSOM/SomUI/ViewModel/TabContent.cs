using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SomUI.ViewModel
{
    /// <summary>
    /// Class for managing dragablz tab content
    /// </summary>    
    class TabContent
    {
        private readonly string _header;
        private readonly object _content;

        /// <summary>
        /// Setting the tab content
        /// </summary>             
        public TabContent(string header, object content)
        {
            _header = header;
            _content = content;
        }

        /// <summary>
        /// Get tab header
        /// </summary>        
        /// <returns>Returns tab header.</returns>
        public string Header
        {
            get { return _header; }
        }

        /// <summary>
        /// Get tab content
        /// </summary>        
        /// <returns>Returns tab content.</returns>
        public object Content
        {
            get { return _content; }
        }
    }
}
